from sqlalchemy import Table, Column, DateTime, Integer, Float, String, ForeignKey
from ..base import Base
from candidate import candidate_donor_assoc

class Donation(Base):

    #Type,LastName,FirstName,Address,City,State,Zip,PAC,Occupation,Employer,Date,Election,Election_Year,Cash_Amount,In_Kind_Amount,
    #In_Kind_Description,Candidate_FirstName,Candidate_MiddleName,Candidate_LastName,Candidate_Suffix,Committee_Name
    __tablename__ = 'donor'
    id = Column(Integer, primary_key=True)
    candidate = relationship('Candidate', secondary=candidate_donor_assoc, back_populates='donors')
    donation_type = Column(String(40), nullable=False)
    donor_firstname = Column(String(40))
    donor_lastname = Column(String(40))
    address = Column(String(40))
    city= Column(String(40))
    state = Column(String(40))
    zipcode = Column(String(40))
    pac = Column(String(40))
    occupation = Column(String(40))
    employer = Column(String(40))
    date_receied = Column(DateTime)
    election = Column(String(40))
    election_year = Column(Integer)
    cash_amount = Column(Float)
    in_kind_amount = Column(Float)
    in_kind_description = Column(String(50)) = Column(String(40))
