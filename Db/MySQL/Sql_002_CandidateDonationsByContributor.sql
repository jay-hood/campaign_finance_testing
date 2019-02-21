CREATE TABLE IF NOT EXISTS CandidateDonationsByContributor(
	CandidateId int NOT NULL,
	ContributorId int NOT NULL,
	Amount decimal(12,2) NOT NULL,	
	CONSTRAINT PK_ContributionDonationsByContributor PRIMARY KEY CLUSTERED (CandidateId, ContributorId),
    FOREIGN KEY (CandidateId) REFERENCES Candidate(CandidateId), 
    FOREIGN KEY (ContributorId) REFERENCES Contributor(ContributorId) 
);
