/*
!!!!! WARNING !!!!!!   This script will drop your existing ElectionFunding database, causing the loss of any existing data.
This script should only be run when a new DB is neeeded.
*/

DROP TABLE IF EXISTS Contribution;
DROP TABLE IF EXISTS Contributor;
DROP TABLE IF EXISTS Candidate;
DROP TABLE IF EXISTS Office;
DROP TABLE IF EXISTS ScrapeLog;
DROP TABLE IF EXISTS Log;

CREATE TABLE Log (
	LogId int NOT NULL,
	Application nvarchar(50) NOT NULL,
	DateLogged datetime NOT NULL,
	Level nvarchar(10) NOT NULL,
	Message nvarchar(5000) NOT NULL,
	UserName nvarchar(250) NULL,
	ServerName nvarchar(1000) NULL,
	Logger nvarchar(250) NULL,
	Callsite nvarchar(5000) NULL,
	Exception nvarchar(5000) NULL,
    CONSTRAINT PK_Log PRIMARY KEY CLUSTERED (LogId ASC)     
);

CREATE TABLE ScrapeLog(
	ScrapeLogId int NOT NULL,
	ScrapeDate DateTime NULL,
	ProcessDate DateTime NULL,
	RawData Text NULL,
	PageUrl nvarchar(1000) NULL,
	CandidateId int NULL,
	CONSTRAINT PK_ScrapeLog PRIMARY KEY CLUSTERED (ScrapeLogId) 
); 

CREATE TABLE Office(
	OfficeId int NOT NULL,
	Name nvarchar(250) NULL,
	CONSTRAINT PK_Office PRIMARY KEY CLUSTERED (OfficeId) 
); 

CREATE TABLE Candidate(
	CandidateId int NOT NULL,
	FilerId	nvarchar(20) NULL,
	OfficeId int NOT NULL,
	CandidateStatus int NOT NULL,
	ElectionType int NULL,
	ElectionYear int NOT NULL,
	FirstName nvarchar(500) NULL,
	MiddleName nvarchar(500) NULL,
	LastName nvarchar(500) NULL,
	Suffix nvarchar(100) NULL,
	CommitteeName nvarchar(1000) NULL,
	CandidateAddress nvarchar(1000) NULL,
	Party nvarchar(500) NULL,
	CandidatePageUrl nvarchar(1000) NULL,
	CONSTRAINT PK_Candidate PRIMARY KEY CLUSTERED (CandidateId),
    FOREIGN KEY (OfficeId) REFERENCES Office(OfficeId) 
); 


CREATE TABLE Contributor(
	ContributorId int NOT NULL,
	LastName nvarchar(500) NULL,
	FirstName nvarchar(500) NULL,
	Address1 nvarchar(500) NULL,
	Address2 nvarchar(500) NULL,
	City nvarchar(500) NULL,
	State char(2) NULL,
	Zip nvarchar(12) NULL,
	PAC nvarchar(1000) NULL,
	Occupation nvarchar(500) NULL,
	Employer nvarchar(1000) NULL,
	CONSTRAINT PK_Contributor PRIMARY KEY CLUSTERED (ContributorId) 
); 

CREATE TABLE Contribution(
	ContributionId int NOT NULL,
	FilerId nchar(20) NULL,
	CandidateId int NULL,
	ScrapeLogId int NULL,
	ContributorId int NULL,
	ContributionType int NULL,
	ContributionDate datetime NULL,
	Amount decimal(8,2) NULL,	
	Description nvarchar(1000) NULL,
	CONSTRAINT PK_Contribution PRIMARY KEY CLUSTERED (ContributionId),
    FOREIGN KEY (CandidateId) REFERENCES Candidate(CandidateId), 
    FOREIGN KEY (ScrapeLogId) REFERENCES ScrapeLog(ScrapeLogId),
    FOREIGN KEY (ContributorId) REFERENCES Contributor(ContributorId) 
);

CREATE TABLE Report(
    ReportId int NOT NULL,
    CandidateId int NOT NULL,
    ReportType nvarchar(100) NULL,
    Year int NULL,
    ReportFileDate DateTime NULL,
    ReportReceivedBy nvarchar(50) NULL,
    ReportReceivedDate DateTime NULL,
    Url nvarchar(500) NULL,
    CONSTRAINT PK_Contribtuor PRIMARY KEY CLUSTERED(ReportId),
    FOREIGN KEY (CandidateId) REFERENCES Candidate(CandidateId)
);
