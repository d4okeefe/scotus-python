from urllib.request import Request, urlopen
from local_libs import parse_scotus_entry



if __name__ == '__main__':
    
    DATABASE = 'docket.db'
    
    dest = "c:\\scratch\\pdf_files\"
        
    entries = []
    for x in range(1,100):
        url = 'https://www.supremecourt.gov/docket/docketfiles/html/public/19-' + str(x) + '.html'
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        entry = parse_scotus_entry.scotus_entry('19-' + str(x), url, webpage)
        entry = parse_scotus_entry.scotus_entry('19-' + str(x), url, webpage)




        entries.append(entry)

