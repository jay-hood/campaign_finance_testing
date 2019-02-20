import attr
import os
import collections
import psycopg2
import csv
from io import StringIO
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import ScrapeLog, CSV, Candidate
import logging.config
loginipath = os.path.join(os.path.dirname(__file__), 'logging_config.ini')
logging.config.fileConfig(loginipath)
logger = logging.getLogger('sLogger')


@attr.s
class Loader:
    candidate_id = attr.ib(init=False)
    session = attr.ib(init=False)
    letter = attr.ib()

    def __attrs_post_init__(self):
        engine = create_engine('postgresql+psycopg2:///TestDB')
        Session = sessionmaker(bind=engine)
        self.session = Session()
        
    def load_csv(self):
        result = \
        self.session.query(Candidate).filter(Candidate.Lastname.ilike(f'%{self.letter}%')).all()
        # self.session.query(Candidate).filter(Candidate.Lastname.like(f'%{self.letter}%')).all()
        # Iterate through list of candidate objects.
        for cand in result:
            logs = \
            self.session.query(ScrapeLog).filter_by(CandidateId=cand.CandidateId).all()
            # Get all ScrapeLogs for the given Candidate, based on their
            # CandidateId. At most this should be a coupe of dozen.
            for log in logs:
                #Load RawData from the ScrapeLog, convert to an ordered dict
                # and then load that data into the CSV table
                # we can probably get rid of Contributions, and add a ScrapeLog
                # column to CSV if we want to keep track of that.
                try:
                    reader = csv.DictReader(StringIO(log.RawData))
                except Exception as e:
                    logging.info(e)
                try:
                    for row in reader:
                        temp = CSV(**row)
                        self.session.add(temp)
                except Exception as e:
                    logging.info(e)
                try:
                    self.session.commit()
                except Exception as e:
                    logging.info(e)
                    self.session.rollback()
    
    def process_csv_data(self):
        ids = [_csv.FilerID for _csv in\
               self.session.query(CSV).distinct(CSV.FilerID)]
        print("IDS: ", ids)
        for _id in ids:
            results = self.session.query(func.sum(CSV.Cash_Amount),\
                                         CSV.FirstName, CSV.LastName).\
                                     group_by(CSV.Address, CSV.FirstName,\
                                              CSV.Cash_Amount,\
                                              CSV.LastName).filter_by(FilerID=_id).order_by(CSV.Cash_Amount.desc()).all()
            for result in results:
                pass
                #put top 3 results in some reworked
                #Contribution/Aggregate/Top-3-Donors table.
        
if __name__ == '__main__':
    try:
        loader = Loader(letter='z')
        loader.load_csv()
        loader.process_csv_data()
    except Exception as e:
        logging.info(e)
