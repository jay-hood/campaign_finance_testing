from base import Base
from association_tables import (
        candidate_state_assoc, 
        state_county_assoc,
        state_municipality_assoc)
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import relationship

class State(Base):

    __tablename__ = 'states' 
    id = Column(Integer, primary_key=True)
    candidates = relationship('Candidate', secondary=candidate_municipality_assoc, back_populates='state')
    counties = relationship('County', back_populates='state')
    municipalities = relationship('Municipality', back_populates='state')
    offices = relationship('Office', secondary=state_office_assoc, backpopulates='state')
    candidates_proxy = association_proxy('candidates', 'id', creator=candidate_find_or_create)
    offices_proxy = association_proxy('offices', 'id', creator=office_find_or_create)
