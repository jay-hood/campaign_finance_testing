# Relevant imports
import psycopg2
import string
from multiprocessing import Pool
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from first_pass_crawler import FirstPassCrawler as FPC
import logging.config
import os

loginipath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'logging_config.ini'))
logging.config.fileConfig(loginipath)
logger = logging.getLogger('sLogger')

# Creates the engine with postgresql and the psycopg2 postgres package.
# For MySQL, install a relevant MySQL package.
engine = create_engine('postgresql+psycopg2:///TestDB')
# engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()


def make_crawler(letter):
    try:
        crawler = FPC(session, letter)
        crawler.crawl()
    except Exception as e:
        logging.info(e)


if __name__ == '__main__':
    try:
        # Create a list of all lowercase letters and then map those to
        # The above make_cralwer function.
        letters = [char for char in string.ascii_lowercase]
        p = Pool(4)
        logging.info('Initializing crawlers.')
        p.map(make_crawler, letters)
        logging.info('Crawlers exiting.')
    except Exception as e:
        logging.info(e)
