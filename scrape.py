from urllib.request import Request, urlopen
from local_libs import parse_scotus_entry
import sqlite3


if __name__ == '__main__':
    
    DATABASE = 'docket.db'

    cxn = sqlite3.connect(DATABASE)
    c = cxn.cursor()
 
    entries = []
    yr = "19-"
    for x in range(5001,5101):
        url = 'https://www.supremecourt.gov/docket/docketfiles/html/public/' + str(yr) + str(x) + '.html'
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        entry = parse_scotus_entry.scotus_entry(str(yr) + str(x), url, webpage)
        entries.append(entry)

    for e in entries:

        print("now saving ... " + e.docket_number)

        c.execute('INSERT INTO docket VALUES(NULL,?,?,?,?,?,?,?,?,?)''', 
        (
            e.docket_number, 
            e.web_address, 
            #e.web_page,
            e.date_retrieved,
            e.case_name,
            e.date_docketed,
            e.lower_court,
            e.lower_court_case_number,
            e.date_rehearing_denied,
            e.date_discretionary_court_decision
        ))
        
        docket_id = c.lastrowid

        for p in e.proceedings:
            c.execute('INSERT INTO proceeding VALUES(NULL,?,?,?)',
            (
                p.date,
                p.text,
                docket_id
            ))
            proceeding_id = c.lastrowid
            for lnk in p.links:
                c.execute('INSERT INTO proceeding_link VALUES(?,?,?)',
                (
                    lnk.title,
                    lnk.link,
                    proceeding_id
                ))
        
        for t in e.contacts:
            c.execute('INSERT INTO contact VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
            (
                t.party_header,
                t.party_description,

                t.name_block,
                t.attorney_full_name,
                t.attorney_surname,
                t.is_counsel_of_record,

                t.address_block,
                t.attorney_email,
                t.attorney_city_state_zip,
                t.is_city_state_zip_valid,
                t.attorney_city,
                t.attorney_state,
                t.attorney_zip,
                t.attorney_office,
                t.attorney_street_address,

                t.phone_number,
                t.phone_number_ten_digit,

                t.party_footer,
                t.party_name,

                docket_id
            ))            

        cxn.commit()