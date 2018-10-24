from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
#ctl00_ContentPlaceHolder1_Name_Reports1_TabContainer1_TabPanel1_Label2
# Selenium uses Firefox to fetch the webpage. Have to install geckodriver in order to use or will throw error.

fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.manager.showAlertOnCompete", False)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
fp.set_preference("browser.download.dir", "/home/jay/projects/python_projects/campaign_finance_scraper/out")

options = Options()
options.add_argument('-headless')
driver = webdriver.Firefox(firefox_profile=fp, options=options)
diver.get('http://media.ethics.ga.gov/search/Campaign/Campaign_Namesearchresults.aspx?CommitteeName=&LastName=a&FirstName=&Method=0')

cn_selector = 'ctl00_ContentPlaceHolder1_Search_List_ctl31_lnkViewID'
ci_selector = 'ctl00_ContentPlaceHolder1_NameInfo1_dlDOIs_ctl02_lnkReportInfo_DOI'
cc_span_selector = 'ctl00_ContentPlaceHolder1_Name_Reports1_TabContainer1_TabPanel1_Label2'
cc_selector = 'ctl00_ContentPlaceHolder1_Name_Reports1_TabContainer1_TabPanel1_dgReports_ctl02_View'
cv_selector = 'ctl00_ContentPlaceHolder1_Name_Reports1_dgReports_ctl02_ViewCont'
dr_selector = 'ctl00_ContentPlaceHolder1_Campaign_ByContributions_RFResults2_Export'
try:
# This clicks the button attached to the javascript doPostBack function 
    click = driver.find_element_by_id(cn_selector).click()
# This follows the resulting chain of links to get to the campaign finance report page
    result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, ci_selector)))
    click = driver.find_element_by_id(ci_selector).click()
    result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, cc_span_selector)))
    click = driver.find_element_by_id(cc_span_selector).click()
    result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, cc_selector)))
    click = driver.find_element_by_id(cc_selector).click()
    result = WebDriverWait(driver,20).until(
            EC.presence_of_element_located((By.ID, cv_selector))) 
    print(driver.current_url)
    click = driver.find_element_by_id(cv_selector).click()
    result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, dr_selector)))
    click = driver.find_element_by_id(dr_selector).click()
    time.sleep(3000)
except Exception as e:
    print(e)

# This iterates through the div, selecting all td elements and printing their text
# for element in result.find_elements_by_tag_name('tr'):
#    print(element)
driver.quit()
