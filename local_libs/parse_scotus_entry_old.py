import re
import datetime
from bs4 import BeautifulSoup

class contact:
    def __init(self):
        pass

class proceeding:
    links = None
    date = None
    text = ''
    def __init__(self, date):
        self.date = date
        

class docket_info_link:
    def __init__(self, title, link):
        self.title = title
        self.link = link

class scotus_entry:
    def __init__(self, docket, address, html):
        self.docket_number = docket
        self.web_address = address
        self.web_page = html
        self.date_retrieved = datetime.date.today()

        self.soup = BeautifulSoup(self.web_page, 'html.parser')

        self.get_case_name()
        self.get_date_docketed()
        self.get_lower_court()
        self.get_case_number()
        self.get_date_rehearing_denied()
        self.get_date_discretionary_court_decision()
        #self.get_analyst()

        self.get_links_docketinfo()

        self.get_proceedings()

        self.get_contacts()

    def get_contacts(self):
        self.contacts = []
        conts = self.soup.find('table', { 'id' : 'Contacts' }).find_all('tr')
        # row_num = 0
        # for r in conts:
        #     if row_num == 0:
        #         pass
        #     else:
        #         if row_num % 2 == 1:
        #             cont = None
        #             col_num = 0
        #             for c in r:
        #                 if col_num == 0:
        #                     cont = contact(c.text)
        #                 if col_num == 1:
        #                     cont.text = c.text
        #                 col_num += 1
        #         else:
        #             links = r.find_all('a')
        #             proc.links = []
        #             for i in links:
        #                 if not i['href'] == '':
        #                     link = docket_info_link(i.text, i['href'])
        #                     proc.links.append(link)
        #             self.proceedings.append(proc)
        #             proc = None
                    #if len(self.proceedings) > 0:
                    #    itm_num = (row_num-1) // 2
                    #    if self.proceedings[itm_num].links == None:
                    #        print(str(itm_num) + ': ' + str(0))
                    #    else:.
                    #        print(str(itm_num) + ': ' + str(len(self.proceedings[itm_num].links)))
            # row_num += 1


    def get_proceedings(self):
        self.proceedings = []
        procs = self.soup.find('table', { 'id' : 'proceedings' }).find_all('tr')
        row_num = 0
        for r in procs:
            if row_num == 0:
                pass
            else:
                if row_num % 2 == 1:
                    proc = None
                    col_num = 0
                    for c in r:
                        if col_num == 0:
                            proc = proceeding(c.text)
                        if col_num == 1:
                            proc.text = c.text
                        col_num += 1
                else:
                    links = r.find_all('a')
                    proc.links = []
                    for i in links:
                        if not i['href'] == '':
                            link = docket_info_link(i.text, i['href'])
                            proc.links.append(link)
                    self.proceedings.append(proc)
                    proc = None
                    #if len(self.proceedings) > 0:
                    #    itm_num = (row_num-1) // 2
                    #    if self.proceedings[itm_num].links == None:
                    #        print(str(itm_num) + ': ' + str(0))
                    #    else:.
                    #        print(str(itm_num) + ': ' + str(len(self.proceedings[itm_num].links)))
            row_num += 1


            

      

    def get_links_docketinfo(self):
        #links = self.soup.select('#docketinfo').find_all('a')
        links = self.soup.find('table', { 'id' : 'docketinfo' }).find_all('a')
        self.links_docketinfo = []
        for i in links:
            if not i['href'] == '':
                link = docket_info_link(i.text, i['href'])
                self.links_docketinfo.append(link)

    def get_case_name(self):
        self.case_name = self.soup.select_one('.title').text

    def get_date_docketed(self):
        self.date_docketed = self.soup.find('td', text='Docketed:').find_next('td').text

    def get_lower_court(self):
        self.lower_court = self.soup.find('td', text='Lower Ct:').find_next('td').text

    def get_case_number(self):
        self.case_number = self.soup.find('td', text=re.compile(r'Case Numbers:')).find_next('td').text

    def get_date_rehearing_denied(self):
        self.date_rehearing_denied = self.soup.find('td', text=re.compile(r'Rehearing Denied:')).find_next('td').text

    def get_date_discretionary_court_decision(self):
        self.date_discretionary_court_decision = self.soup.find('td', text=re.compile(r'Discretionary Court Decision Date:')).find_next('td').text

    #def get_analyst(self):
    #    self.analyst = self.soup.find('td', text='Analyst:').find_next('td').text

    def print_entry(self):
        print(self.docket_number)
        #print(self.web_address)        

        #print(self.date_discretionary_court_decision)
        #print(self.case_name)
        #print(self.case_number)
        #print(self.lower_court)
        #print(self.date_docketed)

        #print(self.web_page)
        #print(self.date_retrieved)
        #for i in self.links_docketinfo:
        #    print(i.title + ' ' + i.link)
        #for i in self.proceedings:
        #    print(i.date)
        #    print(i.text)
        #    for j in i.links:
        #        print('\t' + j.title)
