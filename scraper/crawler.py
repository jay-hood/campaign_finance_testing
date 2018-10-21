from scraper import Scraper
from parser import Parser
from driver_config_normal import driver, WebDriverWait, EC, By

if __name__ == '__main__':
    base_string = 'http://media.ethics.ga.gov/search/Campaign/Campaign_Namesearchresults.aspx?' \
                  'CommitteeName=&LastName={}&FirstName=&Method=0'
    scraper = Scraper('a', base_string)
    candidate_profile_view_ids = scraper.get_candidate_view_ids()
    candidate_profile_view_ids = [candidate_profile_view_ids[29]]
    scraper.iterate_cpvi(candidate_profile_view_ids)
    scraper.close_session()
