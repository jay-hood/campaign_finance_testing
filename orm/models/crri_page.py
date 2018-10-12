from base import Base
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class CRRI(Base):

    __tablename__ = 'crri_page_urls'
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'))
    candidate = relationship('Candidate', back_populates='crri_page')
    url = Column(String(75), nullable=False)
