from sqlalchemy import Column, Sequence, String, Numeric, Integer, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Candidate(Base):
    __tablename__ = 'Candidate'
    CandidateId = Column(Integer, primary_key=True)
    FilerId = Column(String(20), nullable=False)
    OfficeId = Column(Integer, ForeignKey('Office.OfficeId'), nullable=False)
    CandidateStatus = Column(Integer, nullable=False)
    ElectionType = Column(Integer, nullable=False)
    ElectionYear = Column(Integer, nullable=False)
    Firstname = Column(String(500))
    Middlename = Column(String(500))
    Lastname = Column(String(500))
    Suffix = Column(String(100))
    CommitteeName = Column(String(45))
    CandidateAddress = Column(String(100))
    Party = Column(String(45))


class Contributor(Base):
    __tablename__ = 'Contributor'
    ContributorId = Column(Integer, primary_key=True)
    LastName = Column(String(500))
    FirstName = Column(String(500))
    Address1 = Column(String(500))
    Address2 = Column(String(500))
    City = Column(String(500))
    State = Column(String(2))
    Zip = Column(String(12))
    PAC = Column(String(1000))
    Occupation = Column(String(500))
    Employer = Column(String(1000))


class Contribution(Base):
    __tablename__ = 'Contribution'
    ContributionId = Column(Integer, primary_key=True)
    FilerId = Column(String(20))
    CandidateId = Column(Integer, ForeignKey('Candidate.CandidateId'))
    ScrapeLogId = Column(Integer, ForeignKey('ScrapeLog.ScrapeLogId'))
    ContributorId = Column(Integer, ForeignKey('Contributor.ContributorId'))
    ContributionType = Column(Integer)
    ContributionDate = Column(DateTime)
    Amount = Column(Numeric(10, 2))
    Description = Column(String(1000))


class Log(Base):
    __tablename__ = 'Log'
    LogId = Column(Integer, primary_key=True)
    Application = Column(String(50), nullable=False)
    DateLogged = Column(DateTime, nullable=False)
    Level = Column(String(10), nullable=False)
    Message = Column(String(50), nullable=False)
    UserName = Column(String(250))
    ServerName = Column(String(1000))
    Logger = Column(String(250))
    Callsite = Column(String(50))
    Exception = Column(String(50))


class Office(Base):
    __tablename__ = 'Office'
    OfficeId = Column(Integer, primary_key=True)
    Name = Column(String(250))


class Report(Base):
    __tablename__ = 'Report'
    ReportId = Column(Integer, primary_key=True)
    ReportType = Column(String(100))
    Year = Column(Integer)
    ReportFiledDate = Column(String(100))
    ReportReceivedBy = Column(String(100))
    ReportReceivedDate = Column(String(100))
    CandidateId = Column(Integer, ForeignKey('Candidate.CandidateId'))
    Url = Column(String(200))


class ScrapeLog(Base):
    __tablename__ = 'ScrapeLog'
    ScrapeLogId = Column(Integer, primary_key=True)
    ScrapeDate = Column(DateTime)
    ProcessDate = Column(DateTime)
    RawData = Column(String(10485760))
    PageURL = Column(String(200))
    CandidateId = Column(Integer, ForeignKey('Candidate.CandidateId'))
    ReportId = Column(Integer, ForeignKey('Report.ReportId'))


if __name__ == '__main__':
    try:
        # The below should be changed to suit individual database needs,
        # For example, psycopg2 would need to be replaced by whatever
        # MySQL helper package you installed in order to build the database
        # in a MySQL DB.
        import psycopg2
        from sqlalchemy import create_engine
        engine = create_engine('postgresql+psycopg2:///TestDB')
        # engine = create_engine('sqlite:///database.db')
        Base.metadata.create_all(engine)
    except Exception as e:
        print(e)
