# Web-Scraper

A python based web-scraper that predominantly crawls candidate profile pages on the media.ethics.ga.gov website, collecting candidate information and information regarding campaign finance reports.

## Prerequisites
Because of the extensive use of f-strings, this scraper requires the use of Python 3.6+. Specific Python packages are listed in requirements.txt.

## To Run
Please execute the following steps in order:
1. Install python and its package manager, pip, to your system.
1. Install the packages in requirements.txt.
You can do this manually, simply by going into a terminal and typing "pip install PACKAGE_NAME"
where PACKAGE_NAME is one of the packages listed in requirements.txt
Or, you can navigate to the WebScraper subdirectory of the electionmoney project and install
the packages by typing "pip install -r requirements.txt"
1. Download and install geckodriver for your system (system specific releases found here: https://github.com/mozilla/geckodriver/releases).  
   - If installing in Unix/Linux, copy the file to /usr/local/bin.
   - If installing in Windows, copy the file to a folder that is in your Windows path.
1. Download [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
1. Build the database.
You can do this by first modifying a line towards the bottom of the models.py file in the WebScraper subdirectory. SQLAlchemy has to create a engine specifically confifured for certain kinds of databases. 
    - **For MySQL**, the basic structure is "engine = create_engine('mysql://user:password@servername')" where servername would be localhost if running locally and user is the user name in MySQL and password is that user's password for the database you intend to use.
Other engine configuration options can be viewed [here](https://docs.sqlalchemy.org/en/latest/core/engines.html). Assuming this is properly configured, then running "python models.py" should create the database in the designated MySQL database.
1. Change the create_engine configuration in app.py (found a few lines after the import statements) to use the MySQL database, 
providing the same credentials as you did in models.py
1. To designate a candidate name to scrape, edit the "letters" variable in app.py to simply be a comma delimited list of characters
enclosed by single quotes, for example letters = ['y', 'z'] to scrape all candidates whose last name starts with y or z. 
Failure to do this will scrape all candidate data from the campaign finance website, a process which might take several dozen hours.
1. Finally, run "python app.py." This will begin navigating through the designated candidates and aggregating their data.
