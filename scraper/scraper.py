import requests
from root_url import Url
import driver_config
from driver_config import driver 

class Scraper():

    def __init__(self, sur_letter):
        self.fetch_url = base_string.format(sur_letter)
    
    def get_base_urls(self):
        driver.get(fetch_url)
        
    def scrape_base_urls(self):
        pass

if __name__ == 'main':
    base_string = 'http://media.ethics.ga.gov/search/Campaign/Campaign_Namesearchresults.aspx?CommitteeName=&LastName={}&FirstName=&Method=0'
    
