from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options 
import os
import time

capa = DesiredCapabilities.CHROME
capa['pageLoadStrategy'] = 'none'
chrome_options = Options()
download_dir = '/home/jay/Projects/Python Projects/campaign_finance_testing/out'
prefs = {'download.default_directory': download_dir,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': False,
        'safebrowsing.disable_download_protection': True}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(desired_capabilities=capa, options=chrome_options)
driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
command_result = driver.execute("send_command", params)
# driver.get('http://media.ethics.ga.gov/Search/Campaign/Campaign_ByContributions_RFR.aspx?NameID=563&FilerID='
#            'C2017000285&CDRID=134611&Name=Abrams,%20Stacey%20Yvonne&Year=2018&Report=September%2030th%20-%'
#            '20Election%20Year')
driver.get('http://media.ethics.ga.gov/search/Campaign/Campaign_ReportOptions.aspx?'
           'NameID=563&FilerID=C2017000285&CDRID=134611')
view_contrib = 'ctl00_ContentPlaceHolder1_Name_Reports1_dgReports_ctl02_ViewCont'
selector = 'ctl00_ContentPlaceHolder1_Campaign_ByContributions_RFResults2_Export'
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, view_contrib)))
    driver.find_element_by_id(view_contrib).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
    driver.execute_script("window.stop();")
    #result = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.ID, selector)))
    click = driver.find_element_by_id(selector).click()
    while not os.path.exists('{}/StateEthicsReport.csv'.format(download_dir)):
        time.sleep(1)
    if os.path.isfile('{}/StateEthicsReport.csv'.format(download_dir)):
        f = open('{}/StateEthicsReport.csv'.format(download_dir))
        print(f.name)
        print(f.read())
except Exception as e:
    print(e)

