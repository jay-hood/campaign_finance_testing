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
res = driver.get('http://media.ethics.ga.gov/Search/Campaign/Campaign_Namesearchresults.aspx?CommitteeName=&LastName=a&FirstName=&Method=0')
tbody_xpath = '//*[@id="ctl00_ContentPlaceHolder1_Search_List"]/tbody'
tr_xpath = '//*[@id="ctl00_ContentPlaceHolder1_Search_List"]/tbody/tr'
tree = html.fromstring(driver.page_source)

tbody = tree.xpath(tr_xpath)
for tr in tbody:
    js_anchor_id = tr.xpath('.//td/a/@id')
    candidate_name = tr.xpath('.//td[2]/span/text()')
    try:
        print(js_anchor_id[0])
        name = candidate_name[0]
        parsed_name = HumanName(name)
        print('firstname: ', parsed_name.first)
        print('middle: ', parsed_name.middle)
        print('lastname: ', parsed_name.last)

    except Exception as e:
        print(e)
        print(js_anchor_id)
        print(candidate_name)
driver.quit()
