from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class Location(Base):

    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    location_type = Column(String(45), nullable=False)

