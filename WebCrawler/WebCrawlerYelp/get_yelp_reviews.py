from bs4 import BeautifulSoup
from urllib import request
import http.cookiejar
import httplib2
import re
import os.path
import time
import sys
def get_yelp_reviews (url, store):
    queries = 0
    term_dic = {}
    name_of_file = store + "_reviews"
    save_path = "/home/pythonUser/WebCrawlerYelp/store_reviews/" 
    completeName = os.path.join(save_path, name_of_file+".txt") 
    store_file = open(completeName, 'w')
    url_rev = url + '?start='
    cj = http.cookiejar.CookieJar()
    opener = request.build_opener(request.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-Agent', 'Mozilla/5.0'),]
    stringQ = str(queries)
    req = opener.open(url_rev + stringQ)
    page = req.read()
    soup = BeautifulSoup(page,  "html.parser")
    reviews = soup.findAll('p', attrs={'itemprop':'description'})
    authors = soup.findAll('span', attrs={'itemprop':'author'})
    soup = BeautifulSoup(page, "html.parser")
    pages = soup.find("div", {"class": "feed"})
    pages = soup.find("div", {"class": "review-pager"})
    pages = soup.find("div", {"class": "page-of-pages arrange_unit arrange_unit--fill"})
    filled = False
    cont = ""
    for i in pages:
        for j in i:
            if j != '\n':
                cont += j
    s = cont.lstrip(' ')
    total = s.split()
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
    localtime = time.asctime( time.localtime(time.time()) )
    print ("Local current time :", localtime)
    req.close()
    print(total[3])
    time.sleep(30)
    if int(total[3]) > 1:
        for i in range(1,int(total[3])):
            stringQ = str(queries)
            opener = request.build_opener(request.HTTPCookieProcessor(cj))
            opener.addheaders = [('User-Agent', 'Mozilla/5.0'),]
            req = opener.open(url_rev + stringQ)
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
            queries = queries + 20
            localtime = time.asctime( time.localtime(time.time()) )
            print ("Local current time :", localtime)
            req.close()
            time.sleep(30)
    store_file.close()
