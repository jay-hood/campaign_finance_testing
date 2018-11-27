from abc import ABC, abstractmethod
import copy
import attr
from nameparser import HumanName
from lxml import html
from models import Candidate, Report, Office
import logging.config
import os

loginipath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'logging_config.ini'))
logging.config.fileConfig(loginipath)
logger = logging.getLogger('sLogger')

# All parsers inherit from this very simple abstract base class.
@attr.s
class AbstractParser(ABC):
    page_content = attr.ib()

    @abstractmethod
    def parse(self):
        pass

"""Most of these parsers return lists of tuples of dictionaries.
The vast majority of what any given parser does is take the html body
of a given webpage, looks for very specific IDs, gets the information
from them, bundles that data into said dictionaries, and then bundles
them further into tuples that are added to lists. There are, of course,
exceptions and specific functionality to each parser that will be defined
in later comments to be added, but that is the general flow of any given
parser."""
class CandidateProfileParser(AbstractParser):

    def status_to_int(self, status):
        if status.lower == r'n\a':
            return 0
        elif status.lower == 'active':
            return 1
        elif status.lower == 'terminated':
            return 2
        else:
            return 3

    def parse(self, candidate):
        xpath_ = "//*[@id='ctl00_ContentPlaceHolder1_NameInfo1_dlDOIs']/tbody/tr[@class!='gridviewheader']"
        tree = html.fromstring(self.page_content)
        # Body being generated with this xpath is empty list.
        body = tree.xpath(xpath_)
        dropdowns_list = []
        candidates_list = []
        offices_list = []
        # This condition is specifically to handle Account,
        # Deleted profiles, etc.
        if not body:
            candidate['FilerId'] = 'No filer ID'
            candidate['CandidateStatus'] = 0
            candidate['ElectionType'] = 0
            candidate['ElectionYear'] = 0
            return [(None, Office(Name='No Office.'), candidate)]
        for tr in body:
            try:
                candidate_copy = copy.copy(candidate)
                filer = tr.xpath('.//td[1]/text()').pop()
                office_name = tr.xpath('.//td[2]/span/text()').pop()
                dropdown = tr.xpath('.//td[3]/a/@id').pop()
                status = tr.xpath('.//td[4]/span/text()').pop()
                dropdowns_list.append(dropdown)
                candidate_copy['FilerId'] = filer
                candidate_copy['CandidateStatus'] = self.status_to_int(status)
                candidates_list.append(candidate_copy)
                office = Office(Name=office_name)
                offices_list.append(office)
            except Exception as e:
                logging.info(e)

        return ((dropdown, office, candidate) for dropdown, office, candidate
                in zip(dropdowns_list, offices_list, candidates_list))


class DropdownParser(AbstractParser):

    def parse(self):
        xpath_ = '//*[@id="ctl00_ContentPlaceHolder1_Name_Reports1_TabContainer1_TabPanel1_Label2"]'
        tree = html.fromstring(self.page_content)
        body = tree.xpath(xpath_)
        if not body:
            return None
        return 1


class SearchResultsParser(AbstractParser):

    def parse(self):
        candidate = {
                'FilerId': 'No filer ID',
                'OfficeId': 0,
                'CandidateStatus': 0,
                'ElectionType': 0,
                'ElectionYear': 0
                }
        xpath_ = "//*[@id='ctl00_ContentPlaceHolder1_Search_List']/tbody/tr[@class!='gridviewheader']"
        # returns a list of parsed links containing the ids of candidate profile links
        tree = html.fromstring(self.page_content)
        body = tree.xpath(xpath_)
        candidates = []
        link_ids = []
        if body is None:
            return [(None, None)]
        for tr in body:
            try:
                js_id = tr.xpath('.//td/a/@id').pop()
                candidate_name = tr.xpath('.//td[2]/span/text()').pop()
                name = HumanName(candidate_name)
                candidate = copy.copy(candidate)
                candidate['Firstname'] = name.first
                candidate['Middlename'] = name.middle
                candidate['Lastname'] = name.last
                candidate['Suffix'] = name.suffix
                candidates.append(candidate)
                link_ids.append(js_id)
            except Exception as e:
                logging.info(e)
        return [(cand, link_id) for cand, link_id in zip(candidates, link_ids)]


class CandidateRegistrationParser(AbstractParser):

    def parse(self, candidate):
        base = 'ctl00_ContentPlaceHolder1_Name_Reports1_TabContainer1_TabPanel2_lbl'
        tree = html.fromstring(self.page_content)
        street = base+'Address'
        csz = base+'CSZ'
        party = base+'PartyAffiliation'
        committee = base+'ComName'
        committee_info = tree.xpath(f'//*[@id="{committee}"]/text()')
        party_info = tree.xpath(f"//*[@id='{party}']/text()")
        street_info = tree.xpath(f"//*[@id='{street}']/text()")
        csz_info = tree.xpath(f"//*[@id='{csz}']/text()")
        party_text = 'No party given.'
        street_text = 'No street given.'
        csz_text = 'No city, state, or zip given.'
        committee_text = 'No committee name given.'
        try:
            if party_info:
                party_text = party_info.pop()
            if street_info:
                street_text = street_info.pop()
            if csz_info:
                csz_text = csz_info.pop()
            if committee_info:
                committee_text = committee_info.pop()
        except Exception as e:
            logging.info(e)
        candidate['Party'] = party_text
        candidate['CandidateAddress'] = street_text + ' ' + csz_text
        candidate['CommitteeName'] = committee_text
        return candidate


class ReportsTableParser(AbstractParser):

    def parse(self):
        report = {
                'ReportType': 'No report type listed',
                'Year': 0,
                'ReportFiledDate': 'No date listed.',
                'ReportReceivedDate': 'No date listed.',
                'CandidateId': None,
                'Url': 'No url listed.'
                }
        xpath_ = "//*[@id='ctl00_ContentPlaceHolder1_Name_Reports1_TabContainer1_TabPanel1_dgReports']/tbody/tr[@class!='gridviewheader']"
        tree = html.fromstring(self.page_content)
        body = tree.xpath(xpath_)
        links = []
        reports = []
        if not body:
            return [(None, None)]
        for tr in body:
            try:
                link = tr.xpath('.//td[1]/a/@id').pop()
                report_type = tr.xpath('.//td[2]/span/text()').pop()
                year = tr.xpath('.//td[3]/text()').pop()
                report_filed_date = tr.xpath('.//td[4]/text()').pop()
                report_received_by = tr.xpath('.//td[5]/span/text()').pop()
                report_received_date = tr.xpath('.//td[6]/span/text()').pop()
                links.append(link)
                # replace report with dict and do the same thing as with
                # the candidate class
                report = copy.copy(report)
                report['ReportType'] = report_type
                report['Year'] = year
                report['ReportFiledDate'] = report_filed_date
                report['ReportReceivedDate'] = report_received_date
                reports.append(report)
            except Exception as e:
                logging.info(e)
        return ((link, report) for link, report in zip(links, reports))


class ContributionsViewParser(AbstractParser):
    
    def parse(self):
        id_ = 'ctl00_ContentPlaceHolder1_Name_Reports1_dgReports_ctl02_ViewCont'
        xpath_ = "//*[@id='ctl00_ContentPlaceHolder1_Name_Reports1_dgReports_ctl02_ViewCont']"
        tree = html.fromstring(self.page_content)
        body = tree.xpath(xpath_)
        if not body:
            return None
        return id_


class CSVLinkParser(AbstractParser):
    
    def parse(self):
        id_ = "ctl00_ContentPlaceHolder1_Campaign_ByContributions_RFResults2_Export"
        xpath_ = "//*[@id='ctl00_ContentPlaceHolder1_Campaign_ByContributions_RFResults2_Export']"
        tree = html.fromstring(self.page_content)
        body = tree.xpath(xpath_)
        if not body:
            return None
        return id_

