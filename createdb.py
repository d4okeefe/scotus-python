import sqlite3

if __name__ == '__main__':
    
    cxn = sqlite3.connect('docket.db')
    c = cxn.cursor()
    c.execute('''CREATE TABLE docket
             (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 docket_number text not null,
                 web_address text,
                 
                 date_retrieved datetime,
                 case_name text,
                 date_docketed text,
                 lower_court text,
                 lower_court_case_number text,
                 date_rehearing_denied text,
                 date_discretionary_court_decision text
                 )''')
    c.execute('''CREATE TABLE proceeding
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proceeding_date text,
                proceeding_text text,
                docket_id int,                
                FOREIGN KEY(docket_id) REFERENCES docket(id)
            )''')
    c.execute('''CREATE TABLE proceeding_link
            (
                title text,
                link text,
                proceeding_id int,                
                FOREIGN KEY(proceeding_id) REFERENCES proceeding(id)
            )''')
    c.execute('''CREATE TABLE contact
            (
                party_header text,
                party_description text,
                name_block text,
                attorney_full_name text,
                attorney_surname text,
                is_counsel_of_record text,
                address_block text,
                attorney_emailtext,
                attorney_city_state_zip text,
                is_city_state_zip_valid text,
                attorney_city text,
                attorney_state text,
                attorney_zip text,
                attorney_office text,
                attorney_street_address text,
                phone_number text,
                phone_number_ten_digit text,
                party_footer text,
                party_name text,
                docket_id int,
                FOREIGN KEY(docket_id) REFERENCES docket(id)
            )''')            