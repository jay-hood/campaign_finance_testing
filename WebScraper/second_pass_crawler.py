import psycopg2
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from navigator import SeleniumNavigator
from models import Report, ScrapeLog, Candidate
from file_processor import FileProcessor
from parsers import ContributionsViewParser, CSVLinkParser
import attr
import time
import logging.config

loginipath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'logging_config.ini'))
logging.config.fileConfig(loginipath)
logger = logging.getLogger('sLogger')


@attr.s
class SecondPassCrawler:
    session = attr.ib()
    navigator = attr.ib(init=False)
    file_processor = attr.ib(init=False)
    letter = attr.ib()

    def __attrs_post_init__(self):
        logging.info('attrs post init called')
        self.navigator = SeleniumNavigator(loading_strategy='none',
                                           letter=self.letter)
        self.file_processor = FileProcessor(letter=self.letter)

    def exit(self):
        self.navigator.close_browser()
        self.session.close()

    def get_urls(self):
        _ids = self.session.query(Candidate).filter(Candidate.Lastname.ilike('zorn')).all()
        #ids_ = \
        #self.session.query(Candidate).filter(Lastname.like("%z%")).all()
        reports = []
        for _id in _ids:
            results = \
            self.session.query(Report).filter_by(CandidateId=_id.CandidateId).all()
            logging.info(results)
            for result in results:
                reports.append((result.CandidateId, result.Url))
        return reports
        #return ['http://media.ethics.ga.gov/search/Campaign/Campaign_ReportOptions.aspx?NameID=16067&FilerID=C2012000744&CDRID=59991']

    def add_scrapelog_to_db(self, _id, url, content, dtime):
        slog = ScrapeLog(CandidateId=_id,
                         ScrapeDate=dtime,
                         RawData=content,
                         PageURL=url)
        try:
            self.session.add(slog)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logging.info(e)

    def crawl_download_link(self, _id):
        parser = CSVLinkParser(self.navigator.page_source())
        parsed_link = parser.parse()
        if parsed_link is not None:
            logging.info(f'Parsed link: {parsed_link}')
            url = self.navigator.get_current_url()
            self.navigator.click_link(parsed_link)
            logging.info('Clicking download link for csv file.')
            content, dtime = self.file_processor.process()
            logging.info('Adding scrapelog to database')
            self.add_scrapelog_to_db(_id, url, content, dtime)
            self.file_processor.delete_csv()

    def crawl_view_contributions_ids(self, _id):
        logging.info(f'Current page: {self.navigator.get_current_url()}')
        parser = ContributionsViewParser(self.navigator.page_source())
        parsed_link = parser.parse()
        if parsed_link is not None:
            logging.info(f'Parsed link: {parsed_link}')
            self.navigator.click_link(parsed_link)
            self.navigator.wait_for_csv_link()
            self.crawl_download_link(_id)

    def crawl(self):
        for _id, url in self.get_urls():
            logging.info(f'Current url: {url}')
            self.navigator.navigate(url)
            self.navigator.wait_for_contributions_id()
            self.crawl_view_contributions_ids(_id)
            

if __name__ == '__main__':
    engine = create_engine('postgresql+psycopg2:///TestDB')
    Session = sessionmaker(bind=engine)
    session = Session()
    logging.info('Initializing crawler.')

    crawler = SecondPassCrawler(session, 'z')
    crawler.crawl()
    logging.info('Crawler exiting.')
    crawler.exit()
