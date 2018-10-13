from base import Base
from association_tables import (
        candidate_municipality_assoc, 
        municipality_county_assoc,
        office_municipality_assoc,
        candidate_find_or_create,
        county_find_or_create,
        office_find_or_create)
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

class Municipality(Base):

    __tablename__ = 'municipalities' 
    id = Column(Integer, primary_key=True)
    #This is problematic because a lot of counties sit on the border between two states.
    state_id = Column(Integer, ForeignKey('state.id'))
    state = relationship('State', back_populates='municipalities')
    candidates = relationship('Candidate', back_populates='municipality')
    counties = relationship('County', secondary=municipality_county_assoc, back_populates='municipality')
    offices = relationship('Office', secondary=office_municipality_assoc, back_populates='municipality')
    candidates_proxy = association_proxy('candidates', 'id', creator=candidate_find_or_create)
    counties_proxy = association_proxy('counties', 'name', creator=county_find_or_create)
    offices_proxy = association_proxy('candidates', 'name', creator=office_find_or_create)
    
