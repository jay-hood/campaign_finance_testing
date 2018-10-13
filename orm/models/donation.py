from sqlalchemy import Table, Column, DateTime, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class Donation(Base):

    #Type,LastName,FirstName,Address,City,State,Zip,PAC,Occupation,Employer,Date,Election,Election_Year,Cash_Amount,In_Kind_Amount,
    #In_Kind_Description,Candidate_FirstName,Candidate_MiddleName,Candidate_LastName,Candidate_Suffix,Committee_Name
    __tablename__ = 'donations'
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'))
    candidate = relationship('Candidate', back_populates='donors')
    donation_type = Column(String(40), nullable=False)
    election_id = Column(Integer, ForeignKey('election.id'))
    donor_firstname = Column(String(40))
    donor_lastname = Column(String(40))
    date_received = Column(DateTime)
    pac = Column(String(40))
    occupation = Column(String(40))
    employer = Column(String(40))
    cash_amount = Column(Float)
    in_kind_amount = Column(Float)
