import requests
from parser import Parser
import driver_config
from driver_config import driver, WebDriverWait, EC, By 
import time

class Scraper():
 
    parser = Parser()
   
    def __init__(self, sur_letter, base_string):
        self.fetch_url = base_string.format(sur_letter)
    
    def get_candidate_view_ids(self):
        res =  driver.get(self.fetch_url)
        html = driver.page_source
        return self.parser.parse_candidate_profile_views(html)

    def get_campaign_reports_info(self):
        html = driver.page_source
        return self.parser.parse_campaign_reports_info(html)

    def get_campaign_contribution_report_view_ids(self):
        html = driver.page_source
        return self.parser.parse_contribution_report_views(html)

    def get_ccr_dropdown(self):
        return self.parser.ccr_dropdown_id
    
    def get_contributions_view_id(self):
        return self.parser.parse_contributions_view()

    def get_cv_download_id(self):
        return self.parser.parse_csv_download_id()

if __name__ == '__main__':
    base_string = 'http://media.ethics.ga.gov/search/Campaign/Campaign_Namesearchresults.aspx?CommitteeName=&LastName={}&FirstName=&Method=0'
    download_dir = '/home/jay/projects/python_projects/campaign_finance_scraper/out'
    scraper = Scraper('a', base_string)
    candidate_profile_view_ids = scraper.get_candidate_view_ids()
    candidate_profile_view_ids = [candidate_profile_view_ids[29]]
    for profile in candidate_profile_view_ids:
        try:
            driver.find_element_by_id(profile['id']).click()
            crri_list = scraper.get_campaign_reports_info()
            for crri in crri_list:
                driver.find_element_by_id(crri['candidate_info']).click()
                WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, scraper.get_ccr_dropdown())))
                driver.find_element_by_id(scraper.get_ccr_dropdown()).click()
                time.sleep(5)
                cr_list = scraper.get_campaign_contribution_report_view_ids()
                for cr in cr_list:
                    SAVE_NAME = '{}-{}-{}-{}-{}'.format(crri['filer_id'], crri['office_sought'], profile['firstname'],profile['lastname'],cr['report'])
                    waiter = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.ID, cr['action'])))
                    driver.find_element_by_id(cr['action']).click()
                    print(scraper.get_contributions_view_id())
                    #waiter = WebDriverWait(driver, 10).until(
                     #       EC.presence_of_element_located((By.ID, scraper.get_contributions_view_id())))
                    driver.implicitly_wait(5)
                    driver.find_element_by_id(scraper.get_contributions_view_id()).click()
                    #WebDriverWait(driver, 10). until(
                     #       EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_Campaign_ByContributions_RFResults2_dgContSummary')))
                    driver.implicitly_wait(5)
                    print(scraper.get_cv_download_id())
                    #waiter = WebDriverWait(driver, 10).until(
                     #       EC.presence_of_element_located((By.ID, scraper.get_cv_download_id())))
                    print('attempting to download at ', driver.current_url)
                    
                    #click = driver.find_element_by_id(scraper.get_cv_download_id()).click()
                   # while not os.path.exists('{}/tmp/StateEthicsReport.csv'.format(download_dir)):
                   #     time.sleep(1)
                   # if os.path.isfile('{}/tmp/StateEthicsReport.csv'.format(download_dir)):
                   #     os.rename('{}/tmp/StateEthicsReport.csv'.format(download_dir), '{}/{}'.format(download_dir, SAVE_NAME))
                   # driver.get(current_url)
                   # driver.find_element_by_id(scraper.get_ccr_dropdown()).click()
        #res = driver.get(scraper.fetch_url)
        except Exception as e:
            print(e)
            driver.quit()

