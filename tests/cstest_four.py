from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html, etree 
from nameparser import HumanName

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
ris = driver.get('http://media.ethics.ga.gov/search/Campaign/Campaign_Name.aspx?NameID=563')
tbody_xpath = '//*[@id="ctl00_ContentPlaceHolder1_Search_List"]/tbody'
tr_xpath = '//*[@id="ctl00_ContentPlaceHolder1_NameInfo1_dlDOIs"]/tbody/tr'
tree = html.fromstring(driver.page_source)


tbody = tree.xpath(tr_xpath)
for tr in tbody:
    filer_id = tr.xpath('.//td[@class="lblentry"][1]/text()')
    office_sought = tr.xpath('.//td[@class="lblentry"][2]/span/text()')
    status = tr.xpath('.//td[@class="lblentry"][3]/span/text()')
    candidate_information = tr.xpath('.//td/a')
    if filer_id:
        print('filer id',filer_id[0])
    if office_sought:
        print('office sought',office_sought[0])
    if candidate_information:
        print('candidate info',candidate_information[0].get('id'))
    if status:
        print('status',status[0])
    #print(office_sought.text)
    #candidate_information =
    #status = 
    #for td in tds:
    #   try:
    #        print(td.text)
    #    except Exception as e:
    #        print(e)
driver.quit()
