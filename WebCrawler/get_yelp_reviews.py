from bs4 import BeautifulSoup
from urllib import request
import http.cookiejar
import re
import os.path
import time
def get_yelp_reviews (url, store):
    name_of_file = store + "_reviews"
    save_path = "./store_reviews/" 
    completeName = os.path.join(save_path, name_of_file+".txt") 
    store_file = open(completeName, 'w')
    start = time.clock()
    cj = http.cookiejar.CookieJar()
    opener = request.build_opener(request.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-Agent', 'Mozilla/5.0'),]
    req = opener.open(url)
    page = req.read()
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
        except:
            print("error")
    req.close()
    end = time.asctime( time.localtime(time.time()))
    print ("Time loading the page :", time.clock() - start)
    store_file.close()
