from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class Office(Base):

    __tablename__ = 'offices'
    id = Column(Integer, primary_key=True)
    office_type = Column(String(45), nullable=False)
    office_name = Column(String(45), nullable=False)
    location_id = Column(Integer, ForeignKey('locations.id'))
    location = relationship('Location', back_populates='offices')

