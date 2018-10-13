from lxml import html
from nameparser import HumanName
from scraper.candidate_profile import CandidateProfile as CP 


class Parser():
    
    cpv_xpath = '//*[@id="ctl00_ContentPlaceHolder1_Search_List"]/tbody/tr'    
    crri_xpath = ''
    ccd_xpath = ''
    cr_xpath = ''
    c_xpath = ''
    csv_xpath = ''

    def parse_candidate_profile_views(self, html):
        cpv_list = []
        #where html is driver.page_source
        tbody = html.xpath(tr_xpath)
        for tr in tbody:
            js_anchor_id = tr.xpath('.//td/a/@id')
            candidate_name = tr.xpath('.//td[2]/span/text()')
            try:
                name = candidate_name[0]
                js_id = js_anchor_id[0]
                parsed_name = HumanName(name)
                candidate = CP(js_id, name.first, name.middle, name.last)
                cpv_list.append(candidate)
            except Exception as e:
                print(e)
        return cpv_list

    def parse_campaign_reports_info(self, html):
        return crri_list

    def parse_campaign_contribution_dropdown_id(self, html):
        return ccd_list

    def parse_contribution_report_views(self, html):
        return cr_list

    def parse_contributions_view(self, html):
        return c_id

    def parse_csv_download_id(self, html):
        return csv_id


