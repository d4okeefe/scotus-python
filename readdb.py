import sqlite3

if __name__ == '__main__':
    
    cxn = sqlite3.connect('docket.db')

    cxn.text_factory = lambda x: x.decode('latin-1')


    c = cxn.cursor()

    #blah = c.execute('SELECT docket_number from docket')

    query = 'SELECT docket.docket_number, contact.attorney_full_name, contact.party_description, contact.party_name'
    #query = 'SELECT docket.docket_number, proceeding.proceeding_date, proceeding.proceeding_text'
    query += ' FROM docket, contact'
    query += ' WHERE docket.id == contact.docket_id'

    c.execute(query)
    result = c.fetchall()
    for x in result:
        print(x)