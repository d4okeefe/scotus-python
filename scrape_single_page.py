import requests
#https://www.theatlantic.com/ideas/archive/2019/09/trump-false-treason/599074/
#https://www.theatlantic.com/ideas/archive/2019/10/harold-bloom-read-everything/600022/
print("running tests !!!")

#url = 'https://www.theatlantic.com/ideas/archive/2019/10/trump-erdogan-letter/600214/'
#url = 'https://www.theatlantic.com/ideas/archive/2019/10/inevitability-impeachment/600559/'
#url = 'https://www.theatlantic.com/ideas/archive/2019/10/how-minneapolis-defeated-nimbyism/600601/'
#url = 'https://www.theatlantic.com/ideas/archive/2019/10/republicans-process-questions-trump-impeachment/600646/'
#url = 'https://www.theatlantic.com/ideas/archive/2019/10/donald-trump-has-senate-problem/600724/'
#url = 'https://www.theatlantic.com/entertainment/archive/2019/10/hbo-mrs-fletcher-kathryn-hahn-fascinating-misfire/600823/'
#url = 'https://www.theatlantic.com/entertainment/archive/2019/11/apple-tv-the-morning-show-is-best-when-it-tackles-metoo/601273/'
#url = 'https://www.theatlantic.com/ideas/archive/2019/11/andy-beshears-win-kentucky-warning-trump/601516/'
url = 'https://www.theatlantic.com/entertainment/archive/2019/11/donald-trump-e-jean-carroll-sexual-assault-defamation-suit/601561/'
r = requests.get(url)

try:
    with open('c:\\scratch\\frum_kentucky.html', 'w', encoding='utf8') as file:
        #print(r.text)
        file.write(r.text)
except:
    print("PROBLEM !!!")