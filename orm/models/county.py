from base import Base
from association_tables import (
        candidate_municipality_assoc, 
        municipality_county_assoc,
        office_municipality_assoc)
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import relationship
