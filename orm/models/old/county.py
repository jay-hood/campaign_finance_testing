from base import Base
from association_tables import (
        candidate_municipality_assoc, 
        municipality_county_assoc,
        office_municipality_assoc)
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import relationship

class County(Base):

    __tablename__ = 'counties' 
    id = Column(Integer, primary_key=True)
    #This is problematic because a lot of counties sit on the border between two states.
    state_id = Column(Integer, ForeignKey('state.id'))
    state = relationship('State', secondary=state_county_assoc, back_populates='municipalities')
    candidates = relationship('Candidate', back_populates='county')
    municipalities = relationship('Municipality', secondary=municipality_county_assoc, back_populates='county')
    offices = relationship('Office', secondary=office_county_assoc, back_populates='county')
   #candidates_proxy = association_proxy('candidates', 'id', creator=candidate_find_or_create)
    municipalities_proxy = association_proxy('municipalities', 'name', creator=municipality_find_or_create)
    offices_proxy = association_proxy('offices', 'name', creator=office_find_or_create)
    
