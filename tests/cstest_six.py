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
res = driver.get('http://media.ethics.ga.gov/search/Campaign/Campaign_Name.aspx?NameID=563')

#print(driver.page_source)
table_xpath = '//*[@id="ctl00_ContentPlaceHolder1_NameInfo1_dlDOIs"]/tbody/tr[@class!="gridviewheader"]'
tree = html.fromstring(driver.page_source)


tbody = tree.xpath(table_xpath)
for tr in tbody:
    filer_id = tr.xpath('.//td[1]/text()').pop()
    office_sought = tr.xpath('.//td[2]/span/text()').pop()
    candidate_info =  tr.xpath('.//td[3]/a/@id').pop()
    status = tr.xpath('.//td[4]/span/text()').pop()
    print(filer_id)
    print(office_sought)
    print(candidate_info)
    print(status)
driver.quit()
