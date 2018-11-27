# Meeting Notes from 11/27/2018

## Status Update (by component)

* Scraper
    - Convert to hosted MySql db
    - Document structure saved
    - Secondary ScrapeLog table needed?
    - Document hosting needs / call triggers
    - Testing / validation

* Data loader (*new*)
    - Load raw CSV data
    - Normalize
    - Save to tables
    - Testing / validation

* Web API
    - Switch to hosted MySql db
    - Script for loading test data?
    - Testing / validation (Postman?)

* Infrastructure
    - Cron-jobs
    - Deployment script
    - Security (e.g. cert, token, ...?)
    
    
## Questions for Product Owner / Sponsor

* Validation of endpoint needs:  Top (3) contributors (PACS) for candidate

* Will top contributors always be PACs?

* Validate definition of candidate (Person + Election).  e.g. Stacy Abrams was in two elections, so can we refer to that as TWO candidates?

* Confirm:  Single contributor can make multiple contributions
