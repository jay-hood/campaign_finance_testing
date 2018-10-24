from sqlalchemy import Column, Table, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Candidate(Base):
    __tablename__ = 'candidates'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(45))
    middlename = Column(String(45))
    lastname = Column(String(45))
    filer_id = Column(Integer, nullable=False)
    office_sought = Column(String(45), nullable=False)
    status = Column(String(45), nullable=False)
    reports = relationship('Report', back_populates='candidate')


class Report(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    candidate = relationship('Candidate', back_populates='reports')
    candidate_id = Column(Integer, ForeignKey('candidates.id'))
    report_type = Column(String(45))
    report_date = Column(String(45))
    received_by = Column(String(45))
    received_date = Column(String(45))
    reference_url = Column(String(120), nullable=False)


if __name__ == '__main__':
    engine = create_engine('sqlite:///scraper/database.db')
    Base.metadata.create_all(engine)
