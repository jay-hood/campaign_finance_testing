/***************************************************************************************************************
  File name:  ElectionMoney_baseline_DB.sql
  Description:  Script to create baseline DB
  Author: Wayne Schroder
  Date:  10/17/18
***************************************************************************************************************/

IF OBJECT_ID ('Contribution', 'U') IS NOT NULL  
   DROP TABLE Contribution;  
GO  

IF OBJECT_ID ('Contributor', 'U') IS NOT NULL  
   DROP TABLE Contributor;  
GO  

IF OBJECT_ID ('Candidate', 'U') IS NOT NULL  
   DROP TABLE Candidate;  
GO  

IF OBJECT_ID ('Office', 'U') IS NOT NULL  
   DROP TABLE Office;  
GO  

IF OBJECT_ID ('ScrapeLog', 'U') IS NOT NULL  
   DROP TABLE ScrapeLog;  
GO  

IF OBJECT_ID ('Log', 'U') IS NOT NULL  
   DROP TABLE [Log];  
GO  


CREATE TABLE [dbo].[Log] (
	[LogId] [int] IDENTITY(1,1) NOT NULL,
	[Application] [nvarchar](50) NOT NULL,
	[DateLogged] [datetime] NOT NULL,
	[Level] [nvarchar](10) NOT NULL,
	[Message] [nvarchar](max) NOT NULL,
	[UserName] [nvarchar](250) NULL,
	[ServerName] [nvarchar](1000) NULL,
	[Logger] [nvarchar](250) NULL,
	[Callsite] [nvarchar](max) NULL,
	[Exception] [nvarchar](max) NULL,
    CONSTRAINT [PK_Log] PRIMARY KEY CLUSTERED ([LogId] ASC)
      ON [PRIMARY]
) ON [PRIMARY]
GO

CREATE TABLE dbo.ScrapeLog(
	ScrapeLogId int IDENTITY(1000,1) NOT NULL,
	ScrapeDate DateTime NULL,
	ProcessDate DateTime NULL,
	RawData Text NULL,
	PageURL nvarchar(1000) NULL,
	CandidateId int NULL,
	CONSTRAINT PK_ScrapeLog PRIMARY KEY CLUSTERED (ScrapeLogId) 
) ON [PRIMARY]
GO

CREATE TABLE dbo.Office(
	OfficeId int IDENTITY(1000,1) NOT NULL,
	[Name] nvarchar(250) NULL,
	CONSTRAINT PK_Office PRIMARY KEY CLUSTERED (OfficeId) 
) ON [PRIMARY]
GO

CREATE TABLE dbo.Candidate(
	CandidateId int IDENTITY(1000,1) NOT NULL,
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
	CONSTRAINT PK_Candidate PRIMARY KEY CLUSTERED (CandidateId),
    FOREIGN KEY (OfficeId) REFERENCES Office(OfficeId), 
) ON [PRIMARY]
GO


CREATE TABLE dbo.Contributor(
	ContributorId int IDENTITY(1000,1) NOT NULL,
	LastName nvarchar(500) NULL,
	FirstName nvarchar(500) NULL,
	Address1 nvarchar(500) NULL,
	Address2 nvarchar(500) NULL,
	City nvarchar(500) NULL,
	[State] char(2) NULL,
	Zip nvarchar(12) NULL,
	PAC nvarchar(1000) NULL,
	Occupation nvarchar(500) NULL,
	Employer nvarchar(1000) NULL,
	CONSTRAINT PK_Contributor PRIMARY KEY CLUSTERED (ContributorId) 
) ON [PRIMARY]
GO


CREATE TABLE dbo.Contribution(
	ContributionId int IDENTITY(1000,1) NOT NULL,
	FilerId nchar(20) NULL,
	CandidateId int NULL,
	ScrapeLogId int NULL,
	ContributorId int NULL,
	ContributionType int NULL,
	ContributionDate datetime NULL,
	Amount money NULL,
	Description nvarchar(1000) NULL,
	CONSTRAINT PK_Contribution PRIMARY KEY CLUSTERED (ContributionId),
    FOREIGN KEY (CandidateId) REFERENCES Candidate(CandidateId), 
    FOREIGN KEY (ScrapeLogId) REFERENCES ScrapeLog(ScrapeLogId),
    FOREIGN KEY (ContributorId) REFERENCES Contributor(ContributorId) 
) ON [PRIMARY]
GO
