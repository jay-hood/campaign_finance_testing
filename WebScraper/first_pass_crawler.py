# Relevant imports

import attr
import string
from models import Office, Candidate, Report
from navigator import SeleniumNavigator
from parsers import (SearchResultsParser,
                     DropdownParser,
                     CandidateProfileParser,
                     CandidateRegistrationParser,
                     ReportsTableParser)
import logging.config
import os
loginipath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'logging_config.ini'))
logging.config.fileConfig(loginipath)
logger = logging.getLogger('sLogger')


@attr.s
class FirstPassCrawler:
    session = attr.ib()
    candidate_list = attr.ib(init=False)
    navigator = attr.ib(init=False)
    letter = attr.ib()

    def __attrs_post_init__(self):
        self.search_results_urls = \
            [f'http://media.ethics.ga.gov/search/Campaign/Campaign_Namesearchresults.aspx?CommitteeName=&LastName={self.letter}&FirstName=&Method=0']
        #                            'http://media.ethics.ga.gov/search/Campaign/Campaign_Namesearchresults.aspx?CommitteeName=&LastName=x&FirstName=&Method=0',
        #                            'http://media.ethics.ga.gov/search/Campaign/Campaign_Namesearchresults.aspx?CommitteeName=&LastName=z&FirstName=&Method=0']
        # self.search_results_urls =
        # (f'http://media.ethics.ga.gov/search/Campaign/Campaign\
        # _Namesearchresults.aspx?CommitteeName=&LastName={character}&FirstName=&Method=0'
        # for character in string.ascii_lowercase)
        logging.info(self.letter)
        logging.info(self.search_results_urls)
        self.navigator = SeleniumNavigator(letter=self.letter)

    def exit(self):
        self.session.close()

# 3-1.1
    def get_or_add_candidate(self, candidate):
        try:
            query_result = self.session.query(Candidate).filter_by(FilerId=candidate['FilerId'], Firstname=candidate['Firstname'], Lastname=candidate['Lastname']).first()
            if query_result:
                return query_result.CandidateId
            candidate = Candidate(**candidate)
            self.session.add(candidate)
            self.session.commit()
            return candidate.CandidateId
        except Exception as e:
            self.session.rollback()
            logging.info(e)

# 4.1
    def get_or_add_report(self, report):
        try:
            query_result = self.session.query(Report).filter_by(Url=report['Url']).first()
            if query_result:
                return query_result.ReportId
            report = Report(**report)
            self.session.add(report)
            self.session.commit()
            return report.ReportId
        except Exception as e:
            logging.info(e)
            self.session.rollback()

# 2.1
    def get_or_add_office(self, office):
        try:
            query_result = self.session.query(Office).filter_by(Name=office.Name).first()
            if query_result:
                return query_result.OfficeId
            self.session.add(office)
            self.session.commit()
            return office.OfficeId
        except Exception as e:
            self.session.rollback()
            logging.info(e)

# 3-2
    def crawl_reports_table(self, candidate_id):
        dropdown = DropdownParser(self.navigator.page_source())
        if dropdown.parse() is not None:
            try:
                self.navigator.click_dropdown()
                parser = ReportsTableParser(self.navigator.page_source())
                for report_link, report in parser.parse():
                    if report_link is None:
                        logging.info('No report found.')
                        continue
                    try:
                        self.navigator.wait_for_it(report_link)
                        self.navigator.click_link(report_link)
                        self.navigator.wait_for_contributions_id()
                        report['CandidateId'] = candidate_id
                        report['Url'] = self.navigator.get_current_url()
                        self.get_or_add_report(report)
                        self.navigator.back()
                        self.navigator.click_dropdown()
                    except Exception as e:
                        logging.info(e)
                        logging.info(f'Report link id: {report_link}')
            except Exception as e:
                logging.info(e)

# 3-1
    def crawl_registration_info(self, candidate):
        parser = CandidateRegistrationParser(self.navigator.page_source())
        ret_candidate = parser.parse(candidate)
        return self.get_or_add_candidate(ret_candidate)

# 2
    def crawl_candidate_profile(self, url, candidate):
        parser = CandidateProfileParser(self.navigator.page_source())
        for dropdown, office, current_candidate in parser.parse(candidate):
            if dropdown is None:
                logging.info(f"No dropdown for {current_candidate['Firstname']} "
                             f"{current_candidate['Lastname']}")
                office_id = self.get_or_add_office(office)
                current_candidate['OfficeId'] = office_id
                self.crawl_registration_info(current_candidate)
                continue
            office_id = self.get_or_add_office(office)
            current_candidate['OfficeId'] = office_id
            self.navigator.expose_dropdown(dropdown)
            candidate_id = self.crawl_registration_info(current_candidate)
            try:
                self.crawl_reports_table(candidate_id)
            except Exception as e:
                logging.info(e)
        self.navigator.navigate(url)

# 1
    def crawl_candidate_profile_links(self, url):
        self.navigator.navigate(url)
        parser = SearchResultsParser(self.navigator.page_source())
        for candidate, current_link in parser.parse():
            if current_link is None:
                continue
            logging.info(f"Navigating to {candidate['Firstname']} "
                         f"{candidate['Lastname']}")
            try:
                self.navigator.wait_for_it(current_link)
                self.navigator.click_link(current_link)
                self.crawl_candidate_profile(url, candidate)
            except Exception as e:
                logging.info(e)

# 0
    def crawl(self):
        for url in self.search_results_urls:
            try:
                self.crawl_candidate_profile_links(url)
            except Exception as e:
                logging.info(e)
        self.navigator.close_browser()
