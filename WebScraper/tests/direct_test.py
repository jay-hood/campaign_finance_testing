from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os.path 
#ctl00_ContentPlaceHolder1_Name_Reports1_TabContainer1_TabPanel1_Label2
# Selenium uses Firefox to fetch the webpage. Have to install geckodriver in order to use or will throw error.

fp = webdriver.FirefoxProfile()

#fp.set_preference("browser.download.dir", '/home/jay/Downloads')
#fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.manager.showAlertOnCompete", False)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain, application/octet-stream,\
        application/binary, text/csv, application/csv, application/excel, text/comma-separated-values, text/xml, application/xml")

options = Options()
options.add_argument('-headless')
#driver = webdriver.Firefox(firefox_profile=fp)
driver = webdriver.Firefox(firefox_profile=fp, options=options)
#driver = webdriver.Firefox(options=options)
driver.get('http://media.ethics.ga.gov/Search/Campaign/Campaign_ByContributions_RFR.aspx?NameID=27792&FilerID=C2017001358&CDRID=130153&Name=Abbott,%20David%20&Year=2017&Report=Final%20Report%20and%20Termination%20Statement')

selector = 'ctl00_ContentPlaceHolder1_Campaign_ByContributions_RFResults2_Export'
try:
    result = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.ID, selector)))
    click = driver.find_element_by_id(selector).click()
    while not os.path.exists('/home/jay/Downloads/StateEthicsReport.csv'):
        time.sleep(1)
    if os.path.isfile('/home/jay/Downloads/StateEthicsReport.csv'):
        f = open('/home/jay/Downloads/StateEthicsReport.csv')
        print(f.name)
        print(f.read())
except Exception as e:
    print(e)

# This iterates through the div, selecting all td elements and printing their text
# for element in result.find_elements_by_tag_name('tr'):
#    print(element)
driver.quit()
