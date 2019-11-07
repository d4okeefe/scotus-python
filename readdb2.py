import sqlite3

if __name__ == '__main__':
    
    cxn = sqlite3.connect('docket.db')

    cxn.text_factory = lambda x: x.decode('latin-1')


    c = cxn.cursor()

    query = 'SELECT docket.docket_number, proceeding.proceeding_date, proceeding.proceeding_text,'
    query += ' proceeding_link.title, proceeding_link.link'
    query += ' FROM docket, proceeding, proceeding_link'
    query += ' WHERE docket.id == proceeding.docket_id'
    query += ' AND proceeding.id == proceeding_link.proceeding_id'
    c.execute(query)
    result = c.fetchall()
    for x in result:
        print(x)