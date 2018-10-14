from lxml import html
from nameparser import HumanName

class Parser():
    
    cpv_xpath = '//*[@id="ctl00_ContentPlaceHolder1_Search_List"]/tbody/tr[@class!="gridviewheader"]'    
    crri_xpath = '//*[@id="ctl00_ContentPlaceHolder1_NameInfo1_dlDOIs"]/tbody/tr[@class!="gridviewheader"]'
    cr_xpath = '//*[@id="ctl00_ContentPlaceHolder1_Name_Reports1_TabContainer1_TabPanel1_Panel9"]/tbody/tr[@class!="gridviewehader"]'
    ccr_dropdown = 'ctl00_ContentPlaceHolder1_Name_Reports1_TabContainer1_TabPanel1_Label2'

    def parse_candidate_profile_views(self, html):
        cpv_list = []
        #where html is driver.page_source
        tbody = html.xpath(cpv_xpath)
        if tbody is none:
            return None
        for tr in tbody:
            js_anchor_id = tr.xpath('.//td/a/@id')
            candidate_name = tr.xpath('.//td[2]/span/text()')
            try:
                name = candidate_name.pop()
                js_id = js_anchor_id.pop()
                parsed_name = HumanName(name)
                candidate = {
                        'id': js_anchor_id,
                        'firstname': name.first,
                        'lastname': name.last,
                        'middlename': name.middle
                        }
                cpv_list.append(candidate)
            except Exception as e:
                print(e)
        return cpv_list

    def parse_campaign_reports_info(self, html, candidate):
        crri_list = []
        tbody = tree.xpath(table_xpath)
        for tr in tbody:
            try:
                filer_id = tr.xpath('.//td[1]/text()').pop()
                office_sought = tr.xpath('.//td[2]/span/text()').pop()
                candidate_info =  tr.xpath('.//td[3]/a/@id').pop()
                status = tr.xpath('.//td[4]/span/text()').pop()
                cri_dict = {'filer_id': filer_id,
                    'office_sought': office_sought,
                    'candidate_info': candidate_info,
                    'status': status
                    }
                cr_list.append(cri_dict)
            except Exception as e:
                print(e)
        return crri_list

    def parse_contribution_report_views(self, html):
        #Note: HTML has to be from driver AFTER contribution report tab has been clicked.
        cr_list = []
        tbody = html.xpath(cr_xpath)
        for tr in tbody:
            try:
                action = tr.xpath('.//td[1]/a/@id').pop()
                report_type = tr.xpath('.//td[2]/span/text()').pop()
                year = tr.xpath('.//td[3]/text()').pop()
                report = tr.xpath('.//td[4]/text()').pop()
                received_by = tr.xpath('.//td[5]/span/text()').pop()
                received_date = tr.xpath('.//td[6]/span/text()').pop()
                #Yeah, there's no reason to use a custom data model here. Change to dict.
                cr = {'action': action,
                      'report_type': report_type,
                      'year': year,
                      'report': report,
                      'received_by': received_by,
                      'received_date': received_date}       
                cr_list.append(cr)    
        return cr_list

    def parse_contributions_view(self, html):
        # This doesn't actually parse anything, this is just the id of the link selenium needs to click
        return 'ctl00_ContentPlaceHolder1_Name_Reports1_dgReports_ctl02_ViewCont'

    def parse_csv_download_id(self, html):
        return 'ctl00_ContentPlaceHolder1_Campaign_ByContributions_RFResults2_Export'


