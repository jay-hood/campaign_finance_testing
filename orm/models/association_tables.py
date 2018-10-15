from sqlalchemy import Table, Column, ForeignKey, Integer
from base import Base

candidate_election_assoc = Table('candidate_election_assoc', Base.metadata,
        Column('candidate.id', Integer, ForeignKey('candidates.id')),
        Column('election.id', Integer, ForeignKey('elections.id')))
"""
candidate_donation_assoc = Table('candidate_donation_assoc', Base.metadata,
        Column('candidate.id', Integer, ForeignKey('candidates.id')),
        Column('donation.id', Integer, ForeignKey('donations.id')))
candidate_office_assoc = Table('candidate_office_assoc', Base.metadata,
        Column('candidate.id', Integer, ForeignKey('candidates.id')),
        Column('office.id', Integer, ForeignKey('offices.id')))
candidate_county_assoc = Table('candidate_county_assoc', Base.metadata,
        Column('candidate.id', Integer, ForeignKey('candidates.id')),
        Column('county.id', Integer, ForeignKey('counties.id')))
candidate_municipality_assoc = Table('candidate_municipality_assoc', Base.metadata,
        Column('candidate.id', Integer, ForeignKey('candidates.id')),
        Column('municipality.id', Integer, ForeignKey('municipalities.id')))
candidate_state_assoc = Table('candidate_state_assoc', Base.metadata,
        Column('candidate.id', Integer, ForeignKey('candidates.id')),
        Column('state.id', Integer, ForeignKey('states.id')))
municipality_county_assoc = Table('municipality_county_assoc', Base.metadata,
        Column('municipality.id', Integer, ForeignKey('municipalities.id')),
        Column('county.id', Integer, ForeignKey('counties.id')))
office_municipality_assoc = Table('office_municipality_assoc', Base.metadata,
        Column('office.id', Integer, ForeignKey('offices.id')),
        Column('municipality.id', Integer, ForeignKey('municipalities.id')))
office_county_assoc = Table('office_county_assoc', Base.metadata,
        Column('office.id', Integer, ForeignKey('offices.id')),
        Column('county.id', Integer, ForeignKey('counties.id')))
state_county_assoc = Table('state_county_assoc', Base.metadata,
        Column('state.id', Integer, ForeignKey('states.id')),
        Column('county.id', Integer, ForeignKey('counties.id')))
state_municipality_assoc = Table('state_municipality_assoc', Base.metadata,
        Column('state.id', Integer, ForeignKey('states.id')),
        Column('municipality.id', Integer, ForeignKey('municipalities.id')))
state_office_assoc = Table('state_office_assoc', Base.metadata,
        Column('state.id', Integer, ForeignKey('states.id')),
        Column('office.id', Integer, ForeignKey('offices.id')))


def candidate_find_or_create(candidate_id):
    candidate = Candidate.find_candidate(candidate_id)
    return candidate or Candidate() 

def office_find_or_create(office_name):
    office = Office.find_office(office_name)
    return office or Office(office_name)

def municipality_find_or_create(municipality_name):
    municipality = Municipality.find_municipality(municipality_name)
    return municipality or Municipality(municipality_name)

def county_find_or_create(county_name):
    county = County.find_county(county_name)
    return county or County(county_name)

def state_find_or_create(state_name):
    state = State.find(state_name)
    return state or State(state_name)
"""
