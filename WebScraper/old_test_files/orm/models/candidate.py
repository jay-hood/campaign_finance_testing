from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from base import Base
from models.association_tables import candidate_election_assoc

class Candidate(Base):

    __tablename__ = 'candidates'
    id = Column(Integer, primary_key=True)
    #name = Column(String(50), nullable=False)
    firstname = Column(String(50), nullable=False)
    middlename = Column(String(50))
    lastname = Column(String(50), nullable=False)
    crri_page = relationship('CRRI', uselist=False, back_populates='candidate')
    cfr_pages = relationship('CFR', back_populates='candidate')
    elections = relationship('Election', secondary=candidate_election_assoc, back_populates='candidate')
    donations_received = relationship('Donation', back_populates='candidate')
