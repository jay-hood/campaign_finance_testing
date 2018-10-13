from base import Base
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Office(Base):

    __tablename__ = 'offices'
    id = Column(Integer, primary_key=True)
    office_title = Column(String(40), nullable=False)
    office_level = Column(String(40), nullable=False)
