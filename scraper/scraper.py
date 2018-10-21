import requests
from parser import Parser
from db_classes import Candidate, Report
from driver_config_normal import driver, WebDriverWait, EC, By
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

logging.basicConfig(level=logging.INFO,
                    datefmt='%d-%m-%Y:%H:%M:%S',
                    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')


class Scraper:
 
    parser = Parser()
   
    def __init__(self, sur_letter, base_string):
        self.engine = create_engine('sqlite:///scraper/database.db')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.fetch_url = base_string.format(sur_letter)
        driver.get(self.fetch_url)
    
    def get_candidate_view_ids(self):
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

    def iterate_cpvi(self, cpvi_list):
        for profile in cpvi_list:
            try:
                # Go to candidate page 1
                driver.find_element_by_id(profile['id']).click()
                # get a list of ids linking to tables or candidate reports based on what the candidate has run for
                crri_list = self.get_campaign_reports_info()
                self.iterate_crri(crri_list, profile)
            except Exception as e:
                print(e)

    def iterate_crri(self, crri_list, profile):
        for crri in crri_list:
            driver.find_element_by_id(crri['candidate_info']).click()
            # wait until javascript renders the table
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, self.get_ccr_dropdown())))
                # click on the dropdown to expand the table
                driver.find_element_by_id(self.get_ccr_dropdown()).click()
                # wait until the table becomes visible to selenium
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_Name_Reports1_'
                                                             'TabContainer1_TabPanel1_dgReports')))
                # scrape ids for the report reference page javascript button ids
                cr_list = self.get_campaign_contribution_report_view_ids()
                self.iterate_crlist(cr_list, crri, profile)
            except Exception as e:
                print(e)
                pass

    def iterate_crlist(self, crlist, crri, profile):
        for cr in crlist:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, cr['action'])))
            # Go to page with 'view contributions' page link
            driver.find_element_by_id(cr['action']).click()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, self.get_contributions_view_id())))
            # Save that page's url
            url = driver.current_url
            candidate = Candidate(firstname=profile['firstname'],
                                  lastname=profile['lastname'],
                                  filer_id=crri['filer_id'],
                                  office_sought=crri['office_sought'],
                                  status=crri['status'])
            # Don't know if this query works.
            candidate_instance = self.session.query(Candidate).filter_by(firstname=candidate.firstname,
                                                                         lastname=candidate.lastname,
                                                                         filer_id=candidate.filer_id,
                                                                         office_sought=candidate.office_sought,
                                                                         status=candidate.status).first()
            report = Report(reference_url=url)
            # if self.session.query(Report).filter_by(reference_url=report.reference_url).first():
            #     pass
            # below should be elif and above should be uncommented
            if candidate_instance:
                # Don't know if this syntax is correct.
                candidate_instance.reports.append(report)
                self.session.commit()
            else:
                candidate.reports.append(report)
                self.session.add(candidate)
                self.session.commit()
            self.go_back_to_report_table()
        driver.back()
        logging.info(driver.current_url)

    def close_session(self):
        try:
            self.session.close()
        except Exception as e:
            print(e)

    def go_back_to_report_table(self):
        try:
            driver.back()
            # You have to have all 3 of these WebDriverWait calls or else the entire process will fail.
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, self.get_ccr_dropdown())))
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, self.get_ccr_dropdown())))
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, self.get_ccr_dropdown())))
            # You have to click the element twice. For some reason. I am unsure as to why.
            element.click()
            element.click()
        except Exception as e:
            print(e)



if __name__ == '__main__':
    base_string = 'http://media.ethics.ga.gov/search/Campaign/Campaign_Namesearchresults.aspx?CommitteeName=&LastName={}&FirstName=&Method=0'
    download_dir = '/home/jay/projects/python_projects/campaign_finance_scraper/out'
    scraper = Scraper('a', base_string)
    candidate_profile_view_ids = scraper.get_candidate_view_ids()
    candidate_profile_view_ids = [candidate_profile_view_ids[29]]
    for profile in candidate_profile_view_ids:
        try:
            # Go to candidate page 1
            driver.find_element_by_id(profile['id']).click()
            # get a list of ids linking to tables or candidate reports based on what the candidate has run for
            crri_list = scraper.get_campaign_reports_info()
            for crri in crri_list:
                # Click on the link to the first thing the candidate is running for
                driver.find_element_by_id(crri['candidate_info']).click()
                # wait until javascript renders the table
                WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, scraper.get_ccr_dropdown())))
                # click on the dropdown to expand the table
                driver.find_element_by_id(scraper.get_ccr_dropdown()).click()
                # wait until the table becomes visible to selenium
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_Name_Reports1_'
                                                             'TabContainer1_TabPanel1_dgReports')))
                # scrape ids for the report reference page javascript button ids
                cr_list = scraper.get_campaign_contribution_report_view_ids()
                for cr in cr_list:
                    SAVE_NAME = '{}-{}-{}-{}-{}'.format(crri['filer_id'],
                                                        crri['office_sought'],
                                                        profile['firstname'],
                                                        profile['lastname'],
                                                        cr['report'])
                    waiter = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.ID, cr['action'])))
                    # Go to page with 'view contributions' page link
                    # I think the issue with going back one page is that it closes the table tab
                    driver.find_element_by_id(cr['action']).click()
                    waiter = WebDriverWait(driver, 10).until(
                           EC.presence_of_element_located((By.ID, scraper.get_contributions_view_id())))
                    # Print that page's url
                    print(driver.current_url)
                    try:
                        driver.back()
                        # You have to have all 3 of these WebDriverWait calls or else the entire process will fail.
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.ID, scraper.get_ccr_dropdown())))
                        WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.ID, scraper.get_ccr_dropdown())))
                        element = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.ID, scraper.get_ccr_dropdown())))
                        element.click()
                        try:
                            element = driver.find_element_by_id(scraper.get_ccr_dropdown())
                            element.click()
                        except Exception as e:
                            print(e)
                        # driver.find_element_by_id(scraper.get_ccr_dropdown()).click()
                    except Exception as e:
                        print('cant do it')
                        print(e)
                driver.back()
            # You have to call driver.back here twice because one of the pages is actually a standalone page
            # without the dropdown loaded.
            driver.back()
            driver.back()
                    # Now the driver needs to go back to the previous page
                    # I think you can use driver.back()



                    # driver.find_element_by_id(scraper.get_contributions_view_id()).click()
                    # WebDriverWait(driver, 10).until(
                    #        EC.presence_of_element_located((By.ID, scraper.get_cv_download_id())))
                    # #driver.execute_script("window.stop();")
                    # print(driver.current_url)
                    # print('attempting to download at ', driver.current_url)

                    # click = driver.find_element_by_id(scraper.get_cv_download_id()).click()
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

