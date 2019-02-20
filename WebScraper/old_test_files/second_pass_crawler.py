from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from navigator import SeleniumNavigator
from models import Report, ScrapeLog
from file_processor import FileProcessor
from parsers import ContributionsViewParser, CSVLinkParser
import attr
import time
import logging.config

loginipath = '/home/jay/projects/python_projects/revised-cfs/logging_config.ini'
logging.config.fileConfig(loginipath)
logger = logging.getLogger('sLogger')


@attr.s
class SecondPassCrawler:
    session = attr.ib()
    navigator = attr.ib(init=False)
    file_processor = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.navigator = SeleniumNavigator(loading_strategy='none')
        self.file_processor = FileProcessor()

    def exit(self):
        self.navigator.close_browser()
        self.session.close()

    def get_urls(self):
        # results = self.session.query(Report).all()
        # return (report.url for report in results)
        return ['http://media.ethics.ga.gov/search/Campaign/Campaign_ReportOptions.aspx?NameID=16067&FilerID=C2012000744&CDRID=59991']

    def add_scrapelog_to_db(self, url, content, dtime):
        slog = ScrapeLog(scrape_date=dtime,
                         raw_data=content,
                         page_url=url)
        try:
            self.session.add(slog)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logging.info(e)

    def crawl_download_link(self):
        parser = CSVLinkParser(self.navigator.page_source())
        parsed_link = parser.parse()
        if parsed_link is not None:
            logging.info(f'Parsed link: {parsed_link}')
            url = self.navigator.get_current_url()
            self.navigator.click_link(parsed_link)
            logging.info('Clicking download link for csv file.')
            content, dtime = self.file_processor.process()
            self.add_scrapelog_to_db(url, content, dtime)
            self.file_processor.delete_csv()

    def crawl_view_contributions_ids(self):
        logging.info(f'Current page: {self.navigator.get_current_url()}')
        parser = ContributionsViewParser(self.navigator.page_source())
        parsed_link = parser.parse()
        if parsed_link is not None:
            logging.info(f'Parsed link: {parsed_link}')
            self.navigator.click_link(parsed_link)
            self.navigator.wait_for_csv_link()
            self.crawl_download_link()

    def crawl(self):
        urls = self.get_urls()
        for url in urls:
            logging.info(f'Current url: {url}')
            self.navigator.navigate(url)
            self.navigator.wait_for_contributions_id() 
            self.crawl_view_contributions_ids()
            

if __name__ == '__main__':
    engine = create_engine('sqlite:///database.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    logging.info('Initializing crawler.')

    crawler = SecondPassCrawler(session)
    crawler.crawl()
    logging.info('Crawler exiting.')
    crawler.exit()
