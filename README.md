# New Georgia-Election Money - API Project

## Project Overview

Objective: Provide a web-api that exposes public data on Georgia political candidates and their funding sources.

Sponsor: [New Georgia Project](https://newgeorgiaproject.org/)

Affiliation: [Code for Atlanta](https://www.codeforatlanta.org/)

Project status: Development

**Project Summary**
The purpose of this project is to collect data from public, Georgia goverment webistes, and present the data in a more useful and helpful manner as an API, with the eventual goal of providing input for end-user apps that can easily let non-technical people have clear access to the publicly reported funding sources for Georgia politicians.  This project is what you might call "Phase I" of a longer vision.  Here we are just obtaining and exposing data via a web-api (RESTful interface), that client apps will be able to use.  Once done, this will open several opportunities for using the data, such as mobile apps, reports & data analysis, but all of those are outside the scope of this project.  This project is strictly about obtaining and exposing the data via a web-api, and any steps along the way to achieving that goal.

**Needed Skills**
- Web scraping
- Database
- Web API (REST)
- Data analysis
- Subject matter expect on Georgia government offices
- Security

**Communication:** Slack channel: [Code for Atlanta/#ElectionMoney](https://codeforatlanta.slack.com/messages/CCQMPQQ2X/convo/C048Y4BSP-1527614797.000242/)

**Disclaimer**
This project will be obtaining data from publicly available data sources, in a manner that is consistent with state and federal law.  

# How Can I Help?  
1. Add your contact info to the [Participant signup sheet](https://1drv.ms/x/s!AtPeYaX7I7aauFHgUwXqmtJD1-qE)   *(No commitment required.)*
1. Access [Slack channel (electionmoney)](https://codeforatlanta.slack.com/messages/CCQMPQQ2X/   )
1. Read up on the project (this page) and [architecture](https://github.com/jay-hood/electionmoney/blob/master/Docs/Open%20Access%20Candidate%20Finance%20Data%20-%20Design%20overview%20-%202018.09.11.pdf)
1. Decide on an area you'd like to dig into (web-scraper, DB, data-loader, web-api);  Find the repo (see links pinned to our Slack channel), and fork it.  (Create a GitHub account if you have not already done so.)
1. Get aquainted with [data model](https://github.com/jay-hood/electionmoney/tree/master/Db)
1. Get your component running locally
1. Create Trello account & check out the [Trello board](https://trello.com/b/Svpr07oa/election-money)
1. Find task on Trello board ("Requirements - Ready for Dev" section) and dig in!
1. (Make sure to fully test your code.)
1. Submit Pull Request when ready to submit.



**Need access?** Contact Wayne Schroder at GratefulBayou@gmail.com, or message me on the slack channel.

## Goals
1. Pull data from Georgia Ethics Media website.  Extract/transform/load/store as needed.
1. Aggregate data to identify top contributors per candidate
1. Expose web api providing top contributors for given candidate

## Data Sources

**Georgia Government Transparencyand Campaign Finance Commission (http://media.ethics.ga.gov)**
To see campaign reports:
   1. Go to the [Georgia Campaign reports page](http://media.ethics.ga.gov/Search/Campaign/Campaign_ByName.aspx)
   1. Go to Search Campaign > Search by Office Type
   1. Set "Election Year" to the current year
   1. Select a value for "Office Type" and "Office Name"
   1. Click on [Search for Filer]
   1. When presented with list of candidates, click on "View' for one
   1. Click on "Campaign Contribution Reports - EFiled"
   1. Click on "View Report"
   1. Click on "View Contributions"
   1. Click on "Click here to export the result to Excel"

## Short Term Needs
   
## Project Roadmap
TBD

[fini]
