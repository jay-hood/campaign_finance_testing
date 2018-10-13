import requests
from scraper.parser import Parser
from root_url import Url
import driver_config
from driver_config import driver 

class Scraper():
 
    parser = Parser()
   
   def __init__(self, sur_letter):
        self.fetch_url = base_string.format(sur_letter)
    
    def get_base_urls(self):
        res =  driver.get(fetch_url)
        html = res.html
        return self.parser.parse_candidate_profile_view(html)

if __name__ == 'main':
    base_string = 'http://media.ethics.ga.gov/search/Campaign/Campaign_Namesearchresults.aspx?CommitteeName=&LastName={}&FirstName=&Method=0'
    scraper = Scraper('a', base_string)
    scraper.get_base_urls()
