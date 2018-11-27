# Relevant imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from crawler import Crawler
import logging.config
import os
dirname = os.path.dirname(__file__)
log_path = os.path.join(dirname, 'logging_config.ini')
logging.config.fileConfig(log_path)
logger = logging.getLogger('sLogger')


engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()
logging.info('Initializing crawler.')
crawler = Crawler(session)
logging.info('Crawling...')
crawler.crawl()
logging.info('Crawler exiting.')
crawler.exit()
