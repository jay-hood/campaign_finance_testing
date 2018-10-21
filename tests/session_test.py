import sys
sys.path.append('/home/jay/Projects/Python Projects/campaign_finance_testing/scraper')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_classes import Candidate, Report

engine = create_engine('sqlite:///scraper/database.db')
Session = sessionmaker(bind=engine)
session = Session()

candidate = Candidate(filer_id=12345, office_sought="governor", status="active")
# Don't know if this query works.
instance = session.query(Candidate).filter_by(filer_id=candidate.filer_id).first()
report = Report(reference_url='www.test.url.com')
if instance:
    # Don't know if this syntax is correct.
    instance.reports.append(report)
    session.commit()
    print(instance.reports)
else:
    candidate.reports.append(report)
    session.add(candidate)
    session.commit()
session.close()