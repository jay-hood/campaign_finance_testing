import attr
import os
from driver_config import DriverConfig
import logging.config
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

loginipath = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'logging_config.ini'))

logging.config.fileConfig(loginipath)
logger = logging.getLogger('sLogger')


@attr.s
class SeleniumNavigator():
    loading_strategy = attr.ib(default='normal')
    driver = attr.ib(init=False)

    def __attrs_post_init__(self):
        try:
            DC = DriverConfig(self.loading_strategy, headless=True)
            self.driver = DC.get_driver()
        except Exception as e:
            logging.info(e)

    def wait_for_it(self, element_id):
        try:
            (WDW(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, element_id))))
            (WDW(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, element_id))))
        except Exception as e:
            logging.debug(e)
            logging.info(f'Element id: {element_id}')

    def click_link(self, element_id):
        try:
            self.wait_for_it(element_id)
            self.driver.find_element_by_id(element_id).click()
        except Exception as e:
            logging.debug(e)
            logging.info(f'Element id: {element_id}')

    def wait_for_contributions_id(self):
        contributions_id = ("ctl00_ContentPlaceHolder1_Name_"
                            "Reports1_dgReports_ctl02_ViewCont")
        self.wait_for_it(contributions_id)

    def wait_for_csv_link(self):
        link_id = ("ctl00_ContentPlaceHolder1_Campaign_"
                   "ByContributions_RFResults2_Export")
        self.wait_for_it(link_id)

    def expose_dropdown(self, element_id):
        try:
            (WDW(self.driver, 10).until(EC.presence_of_element_located(
                (By.ID, element_id))))
            self.click_link(element_id)
        except Exception as e:
            logging.debug(e)
            logging.info(f'Element id: {element_id}')

    def click_dropdown(self):
        element_id = ('ctl00_ContentPlaceHolder1_Name_'
                      'Reports1_TabContainer1_TabPanel1_Panel8')
        table_id = ('ctl00_ContentPlaceHolder1_Name_'
        'Reports1_TabContainer1_TabPanel1_dgReports')
        for _ in range(10):
            try:
                self.driver.find_element_by_id(element_id).click()
                time.sleep(1)
                element = self.driver.find_element_by_id(table_id)
                if element.is_displayed():
                    time.sleep(1)
                    return
            except NoSuchElementException:
                logging.debug('No such element. Breaking.')
                return
            except Exception as e:
                logging.info('Dropdown not exposed. Retrying.')
                logging.debug(e)

    def get_current_url(self):
        return self.driver.current_url

    def page_source(self):
        return self.driver.page_source

    def navigate(self, url):
        self.driver.get(url)

    def back(self):
        self.driver.back()

    def close_browser(self):
        self.driver.quit()
