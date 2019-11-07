import time
from bs4 import BeautifulSoup
import sqlite3
import datetime
import re
from enum import Enum


class proc_type(Enum):
    AFFIDAVIT =  1
    AGREEMENT_TO_DISMISS =  2
    AMICUS_BRIEF =  3
    APPELLANT =  4
    APPELLEE =  5
    APPLICATION =  6
    ARGUED =  7
    BLANKET_CONSENT =  8
    BRIEF_AMICI_CURIAE =  9
    BRIEF_AMICUS_CURIAE =  10
    BRIEF_OF_RESPONDENT =  11
    BRIEF_OF =  12
    BRIEF_OPPOSING_MOTION =  13
    CERTIFICATE =  14
    CIRCULATED =  15
    CONSENT =  16
    CORRECTED_PROOF =  17
    CORRECTED =  18
    DISTRIBUTED =  19
    FURTHER =  20
    IMPROVIDENTLY_GRANTED =  21
    JOINT_APPENDIX =  22
    JOINT_LETTER =  23
    JOINT_MOTION =  24
    # JOINT_MOTION =  25
    JOINT_RESPONSE =  26
    JOINT_STIPULATIO =  27
    JUDGMENT_ISSUED =  28
    LETTER =  29
    LODGING =  30
    MANDATE_ISSUED =  31
    MEMORANDUM =  32
    MOTION =  33
    NOTICE =  34
    NOTICE_OF_SUBSTITUTION =  35
    OPPOSITION_TO_APPELLEE =  36
    OPPOSITION_TO_MOTION =  37
    PETITION_DENIED =  38
    PETITION_DISMISSED =  39
    PETITION_FOR_A_WRIT_OF_CERTIORARI_BEFORE_JUDGMENT =  40
    PETITION_FOR_A_WRIT_OF_CERTIORARI =  41
    PETITION_FOR_A_WRIT_OF_HABEAS_CORPUS =  42
    PETITION_FOR_A_WRIT_OF_MANDAMUS =  43
    PETITION_FOR_REHEARING =  44
    PETITION_GRANTED =  45
    PETITIONER_S_RESPONSE =  46
    PROOF_OF_SERVICE =  47
    RECORD =  48
    REHEARING_DENIED =  49
    REPLY_IN_SUPPORT =  50
    REPLY_OF =  51
    REQUEST =  52
    RESCHEDULED =  53
    RESPONDENT_S_SUGGESTION_OF_DEATH =  54
    RESPONSE_IN_OPPOSITION =  55
    RESPONSE_IN_SUPPORT =  56
    RESPONSE_OF =  57
    RESPONSE_REQUESTED =  58
    RESPONSE_TO_APPLICATION =  59
    RESPONSE_TO_MOTION =  60
    RESPONSE_TO_PETITION =  61
    RULE_29_6 =  62
    RULE_34 =  63
    SECOND_SUPPLEMENT =  64
    SET_FOR_ARGUMENT =  65
    STATEMENT =  66
    STAY =  67
    STIPULATION =  68
    SUGGESTION =  69
    SUPPLEMENT =  70
    THE_APPEAL_IS_DISMISSED_FOR_WANT_OF_JURISDICTION =  71
    THE_APPLICATION =  72
    THE_MOTION =  73
    THE_PARTIES =  74
    THE_PETITION_FOR_CERTIORARI_IS_GRANTED__THE_JUDGMENT_IS_REVERSED__AND_THE_CASE_IS_REMANDED =  75
    THE_RECORD =  76
    THE_SOLICITOR_GENERAL =  77
    UPON_CONSIDERATION =  78
    WAIVER =  79


class proceeding_type:



    # thisdict =	{
    # "brand": "Ford",
    # "model": "Mustang",
    # "year": 1964
    # }

    def __init__(self, proceeding_text):
        pass




class proceeding:
    links = None
    date = None
    text = ''
    def __init__(self, date):
        self.date = date
class contact:
        def __init__(self):
            pass

        party_header = ''
        party_description = ''

        name_block = ''
        attorney_full_name = ''
        attorney_surname = ''
        is_counsel_of_record = ''

        address_block = ''
        attorney_email = ''
        attorney_city_state_zip = ''
        is_city_state_zip_valid = False
        attorney_city = ''
        attorney_state = ''
        attorney_zip = ''
        attorney_office = ''
        attorney_street_address = ''

        phone_number = ''
        phone_number_ten_digit = ''

        party_footer = ''
        party_name = ''

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
        self.soup.encode("utf-8")

        self.get_case_name()
        self.get_date_docketed()
        self.get_lower_court()
        self.get_lower_court_case_number()
        self.get_date_rehearing_denied()
        self.get_date_discretionary_court_decision()
        #self.get_analyst()

        self.get_links_docketinfo()

        self.get_proceedings()

        self.get_contacts()

    def ends_with_zipcode(self, str):
        number_splits = re.split(r'[^\d]', str)
        if len(number_splits[-1]) == 5:
            return True
        if len(number_splits[-1]) == 4 and len(number_splits[-2]) == 5:
            return True
        return False

    def parse_city_state_zip(self, cntct, str):
        test = re.findall(r'^(([A-Z][a-z]+\s?)+),\s([A-Z]{2})\s(\d{5}-?(\d{4})?)$', str)
        cntct.attorney_city_state_zip = str
        try:
            cntct.attorney_city = test[0][0]
            cntct.attorney_state = test[0][2]
            cntct.attorney_zip = test[0][3]
            cntct.is_city_state_zip_valid = True
        except:
            cntct.attorney_city = ''
            cntct.attorney_state = ''
            cntct.attorney_zip = ''
            cntct.is_city_state_zip_valid = False
        finally:
            return cntct

    def parse_contact_address(self, cntct, cols):
        #cntct = contact()

        col = cols[1]
        cntct.address_block = col.get_text('\n')
        split_address_by_break = cntct.address_block.split('\n')

        start_pos = 0
        end_pos = -1

        # get office
        if self.are_no_digits(split_address_by_break[0]):
            cntct.attorney_office = split_address_by_break[0]
            start_pos = 1

        # get email address
        if '@' in split_address_by_break[-1]:
            cntct.attorney_email = split_address_by_break[-1]
            end_pos = -2

        # get city state zip
        test_city_state_zip = ''
        if cntct.attorney_email == '':
            test_city_state_zip = split_address_by_break[-1]
            end_pos = -1
        else:
            test_city_state_zip = split_address_by_break[-2]
            end_pos = -2
        
        cntct = self.parse_city_state_zip(cntct, test_city_state_zip)

        cntct.attorney_street_address = '\n'.join(split_address_by_break[start_pos:end_pos]).strip()
        #print(cntct.attorney_street_address)

        return cntct

    def are_no_digits(self, str):
        for i in range(0, len(str)):
            if str[i].isdigit():
                return False
        return True

    def is_all_digits(self, str):
        for i in range(0, len(str)):
            if not str[i].isdigit():
                return False
        return True

    def get_contacts(self):
          #  var outer_node = html.GetElementbyId("Contacts")
          #  var cells = outer_node.Descendants("td")

        self.contacts = []
        cntct = None
        rows = self.soup.find('table', { 'id' : 'Contacts' }).find_all('tr')
        row_cnt = len(rows)
        contact_subheader_rows = []

        # get row index of each new contact entry
        for r in range(0, row_cnt):
            cols = rows[r].find_all('td')
            if cols[0].has_attr('class') and cols[0].attrs['class'][0] == 'ContactSubHeader':
                   contact_subheader_rows.append(r)

        # create contact objects
        for r in range(contact_subheader_rows[0], row_cnt):

            # collect header info
            if r in contact_subheader_rows:
                cntct = None
                curr_party_header = rows[r].get_text('\n')
                curr_party_description = curr_party_header.replace('Attorneys for', '').strip()
                continue

            cols = rows[r].find_all('td')

            # capture name & address block (creating contact object)
            if cols[0].has_attr('class') and cols[0].attrs['class'][0] == 'ContactData2':

                cntct = contact()

                cntct.party_header = curr_party_header
                cntct.party_description = curr_party_description

                cntct.is_counsel_of_record = 'Counsel of Record' in cols[0].get_text('\n')
                if cntct.is_counsel_of_record:
                    cntct.attorney_full_name = cols[0].get_text('\n').replace('Counsel of Record', '').strip()
                else:
                    cntct.attorney_full_name = cols[0].get_text('\n').strip()
                cntct.attorney_surname = cntct.attorney_full_name.split()[-1]

                cntct = self.parse_contact_address(cntct, cols)

                # parse phone number
                temp_phone_number = cols[2].get_text()
                if not self.is_all_digits(temp_phone_number):
                    temp_phone_number = ''.join(re.findall(r'\d+', temp_phone_number))
                cntct.phone_number = temp_phone_number
                cntct.phone_number_ten_digit = len(cntct.phone_number) == 10
                
                

            # capture party name (saving contact object to collection, and setting cntct to None)
            elif cols[0].has_attr('class') and cols[0].attrs['class'][0] == 'ContactParty' \
                or cols[0].get_text().startswith('Party name:'):

                cntct.party_footer = rows[r].get_text('\n')
                cntct.party_name = cntct.party_footer.replace('Party name:', '').strip()
                self.contacts.append(cntct)
                cntct = None
            else:
                #print('no id')
                pass
    
    def parse_proceeding_text(self, proc_text):

        pass

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

                            # parse proceeding text -- this will become very important for ordering
                            self.parse_proceeding_text(proc.text)


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
                    #        print(str(itm_num) + ': ' +
                    #        str(len(self.proceedings[itm_num].links)))
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

    def get_lower_court_case_number(self):
        self.lower_court_case_number = self.soup.find('td', text=re.compile(r'Case Numbers:')).find_next('td').text

    def get_date_rehearing_denied(self):
        self.date_rehearing_denied = self.soup.find('td', text=re.compile(r'Rehearing Denied:')).find_next('td').text

    def get_date_discretionary_court_decision(self):
        self.date_discretionary_court_decision = self.soup.find('td', text=re.compile(r'Discretionary Court Decision Date:')).find_next('td').text

    #def get_analyst(self):
    #    self.analyst = self.soup.find('td',
    #    text='Analyst:').find_next('td').text

    def print_entry(self):
        pass
        #print(self.docket_number)
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
