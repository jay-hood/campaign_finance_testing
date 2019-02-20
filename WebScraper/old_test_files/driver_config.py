import attr 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import logging.config
loginipath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'logging_config.ini'))
logging.config.fileConfig(loginipath)
logger = logging.getLogger('sLogger')

@attr.s
class DriverConfig:
    """ As much of the Georgia campaign finance website's html
    is javascript generated, we have to set a loading strategy based
    on the requirements of each individual crawler. For the first_pass
    crawler, we need a normal loading strategy. As such we define normal
    as the default. It is only to use the second_pass_cralwer that the
    loading strategy must be set to None. The options below in get_driver
    are used to configure the driver to allow for the downloading of files,
    something that the webdriver normally cannot do for security reasons"""
    loading_strategy = attr.ib(default='normal')
    headless = attr.ib(default=True)
    
    def get_driver(self):
        chrome_options = Options()
        capa = DesiredCapabilities.CHROME
        if isinstance(self.headless, bool):
            if self.headless:
                chrome_options.add_argument('--headless')
        else:
            raise TypeError
        if isinstance(self.loading_strategy, str) and (self.loading_strategy.lower() is 'normal' or 'none'):
            capa['pageLoadStrategy'] = self.loading_strategy.lower()
        else:
            raise ValueError
        download_dir = '/home/jay/projects/python_projects/revised-cfs/csv'
        prefs = {'download.default_directory': download_dir,
                 'download.prompt_for_download': False,
                 'download.directory_upgrade': True,
                 'safebrowsing.enabled': False,
                 'safebrowsing.disable_download_protection': True}
        chrome_options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(desired_capabilities=capa, options=chrome_options)
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        command_result = driver.execute("send_command", params)
        return driver


