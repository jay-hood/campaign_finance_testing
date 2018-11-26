# Relevant imports
import attr
import time
import string
from models import Candidate, Report, Office
from navigator import SeleniumNavigator
from parsers import (SearchResultsParser, 
                     DropdownParser, 
                     CandidateProfileParser, 
                     ReportsTableParser)
import logging.config
import os
dirname = os.path.dirname(__file__)
log_path = os.path.join(dirname, 'logging_config.ini')
logging.config.fileConfig(log_path)
logger = logging.getLogger('sLogger')


@attr.s
class Crawler:
    session = attr.ib()
    candidate_list = attr.ib(init=False)
    navigator = attr.ib(init=False)
    
    def __attrs_post_init__(self):
        self.search_results_urls = ['http://media.ethics.ga.gov/search/Campaign/Campaign_Namesearchresults.aspx?CommitteeName=&LastName=a&FirstName=&Method=0']
        # self.search_results_urls = (f'http://media.ethics.ga.gov/search/\
        #        Campaign/Campaign_Namesearchresults.aspx?CommitteeName=&LastName=\
        #        {character}&FirstName=&Method=0' for character in string.ascii_lowercase)
        self.navigator = SeleniumNavigator()

    def exit(self):
        self.session.close()

    def add_candidate_to_db(self, candidate):
        try:
            self.session.add(candidate)
            self.session.commit()
        except Exception as e:
            logging.info(e)
        return candidate.id

    def add_office_to_db(self, office):
        try:
            self.session.add(office)
            self.session.commit()
        except Exception as e:
            logging.info(e)
            self.session.rollback()
        return office.id
    
    def add_report_to_db(self, report):
        try:
            self.session.add(report)
            self.session.commit()
        except Exception as e:
            logging.info(e)
            self.session.rollback()
        return report.id

    def crawl_reports_table(self, office_id):
        dropdown = DropdownParser(self.navigator.page_source())
        if dropdown.parse() is not None:
            try:
                self.navigator.click_dropdown_initial()
                parser = ReportsTableParser(self.navigator.page_source())
                res = parser.parse()
                for report_link, report in res:
                    try:
                        self.navigator.click_link(report_link)
                        self.navigator.wait_for_contributions_id()
                        report.url = self.navigator.get_current_url()
                        report.office_id = office_id
                        self.add_report_to_db(report)
                        self.navigator.back()
                        self.navigator.click_dropdown_subsequent()
                    except Exception as e:
                        logging.info(e)
            except Exception as e:
                logging.info(e)
    
    def crawl_candidate_profile(self, url, candidate):
        parser = CandidateProfileParser(self.navigator.page_source())
        logging.info(f'Crawling page for {candidate.firstname} {candidate.lastname}')
        for dropdown_link, office in parser.parse():
            if dropdown_link is None:
                continue
            candidate_id = self.add_candidate_to_db(candidate)
            office.candidate_id = candidate_id
            office_id = self.add_office_to_db(office)
            self.navigator.expose_dropdown(dropdown_link)
            try:
                self.crawl_reports_table(office_id)
            except Exception as e:
                logging.info(e)
        self.navigator.navigate(url)
    
    def crawl_candidate_profile_links(self, url):
        self.navigator.navigate(url)
        parser = SearchResultsParser(self.navigator.page_source())  
        for candidate, current_link in parser.parse():
            self.navigator.click_link(current_link)
            try:
                self.crawl_candidate_profile(url, candidate)
            except Exception as e:
                logging.info(e)

    def crawl(self):
        for url in self.search_results_urls:
            logging.info(f'Crawling {url}')
            try:
                self.crawl_candidate_profile_links(url)
            except Exception as e:
                logging.info(e)
        self.navigator.close_browser()
