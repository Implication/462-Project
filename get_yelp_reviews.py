from bs4 import BeautifulSoup
from urllib import request
import re
import os.path

def get_yelp_reviews (url, store):
    queries = 0
    term_dic = {}
    name_of_file = store + "_reviews"
    save_path = "./store_reviews/" 
    completeName = os.path.join(save_path, name_of_file+".txt") 
    store_file = open(completeName, 'w')
    #url = 'https://www.yelp.com/biz/dice-house-games-fullerton'
    url_rev = url + '?start='
    while queries <201:
        stringQ = str(queries)
        page = request.urlopen(url_rev + stringQ)

        soup = BeautifulSoup(page,  "html.parser")
        reviews = soup.findAll('p', attrs={'itemprop':'description'})
        authors = soup.findAll('span', attrs={'itemprop':'author'})

        flag = True
        indexOf = 1

        for review in reviews:
            dirtyEntry = str(review)
            while dirtyEntry.index('<') != -1:
                indexOf = dirtyEntry.index('<')
                endOf = dirtyEntry.index('>')
                if flag:
                    dirtyEntry = dirtyEntry[endOf+1:]
                    flag = False
                else:
                    if(endOf+1 == len(dirtyEntry)):
                        cleanEntry = dirtyEntry[0:indexOf]
                        break
                    else:
                        dirtyEntry = dirtyEntry[0:indexOf]+dirtyEntry[endOf+1:]
            try:
                print(cleanEntry, file=store_file)
                term_list = str(cleanEntry).split()
                for term in term_list:
                    regx = re.search('(\w){2,}', term)
                    if(regx):
                        term_cln = regx.group(0)
                        if(term_cln.lower() in term_dic):
                            term_dic[term_cln.lower()] = term_dic[term_cln.lower()] + 1
                        else:
                            term_dic[term_cln.lower()] = 1
            except:
                print("error")
        queries = queries + 20
    
    store_file.close()
    return term_dic