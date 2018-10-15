from sqlalchemy import Table, ForeignKey, String, Integer, Column
from sqlalchemy.orm import relationship 
from base import Base

class Election(Base):

    __tablename__ = 'elections'
    id = Column(Integer, primary_key=True)
    candidates = relationship('Candidate', back_populates='campaign')
    office_id = Column(Integer, ForeignKey('offices.id'), nullable=False)
    year = Column(Integer, nullable=False)

    
