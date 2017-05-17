import pymysql
import logging
import time
import os
import re, collections
import sys, shutil
from imageAdd import imageURL
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
'''
Notes for logs
        - Accept logs records all commits that were accepted into the main table
        - Rejected log records all text files denied by the algorithm
        - Ambiguous logs all text files that could not be verified by the algorithm. These will have to be manually checked.
        - sqllog records all syntax errors that occured during the algorithm
Notes for algorithm
        -This algorithm basically checks whether a store is a board game store or not, more on that in the code itself
        -Their must be a file named store_reviews, that must contain at least 1 file for this to run properly
        -When a file is accepted or rejected, it will delete  those files only, any files that are left afterword are ambiguous and need to be checked manually
        -This file is a completely stand alone algorithm, this can run on its own, or be modified to run as a function within another script.
        -MOST IMPORTANT: Any ambiguous numbers caught Must be checked, these will not be deleted off the store review.
        -Algorithm Relies Primarily on bgs.txt file, words imported here must be tested before putting into the this file, for they may be ambiguous and catch non bgs.
'''
def reject(review,check,rejected):
        check.append(reviews)
        #Note a board game store, if they dont talk about games, we cant determine the merchandise.
        print("%s is not a board game store" % (review))
        name = reviews[i].split("_review")
        printname = name
        name = name[0].replace('\'','\\\'')
        try:
                check.append(review)
                mysql.execute("SELECT * FROM AppDevDB.Yelp WHERE YelpID = '%s'" % (name))
                data = mysql.fetchall()
                result = dict(data[0])
                if result['ApprovedByWebCrawler'] != 0:
                        mysql.execute("UPDATE `AppDevDB`.`Yelp` SET `ApprovedByWebCrawler`='0' WHERE `RowNumberKey`='%d';" % (result['RowNumberKey']))
                        conn.commit()
                        os.remove(review)
                        rejected = rejected + 1;
                        rejectlog.info("%s store rejected at %s" % (printname,timestamp))
                else:
                       os.remove(review)
        except:
                sqllog.error("Syntax error in the rejction sql logic at %s" % (timestamp))
                sys.exit()
        return rejected
        
def setup_log(name, filename, level):
        l = logging.getLogger(name)
        format = logging.Formatter('%(asctime)s : %(message)s')
        fileHandler = logging.FileHandler(filename)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(format)
        l.setLevel(level)
        l.addHandler(fileHandler)
        l.addHandler(streamHandler)
path = os.curdir + "/accepted.log"
move = os.getcwd()
move += "/indeterminate"
setup_log('Accepted',path,logging.INFO)
path = os.curdir + "/sqlForAlgorithm.log"
setup_log('sqlForAlgorithm',path,logging.ERROR)
path = os.curdir + "/rejected.log"
setup_log('Rejected',path,logging.INFO)
path = os.curdir + "/ambiguous.log"
setup_log('Ambiguous',path,logging.INFO)
acceptlog = logging.getLogger('Accepted')
sqllog = logging.getLogger('sqllog')
rejectlog = logging.getLogger('Rejected')
ambiguouslog = logging.getLogger('Ambiguous')
isbgs = open("bgs.txt").readlines()
rejectProd = open("rejectProducts.txt","r")
os.chdir(os.curdir + "/store_reviews")
reviews = []
for root, dirs, files in os.walk(os.curdir):
        for file in files:
                reviews.append(file)
l = list()
try:
        conn = pymysql.connect(user="RemoteUser", passwd="Rem@teMiq3924",host="tabletopfinder.com", port=3306,database="AppDevDB",autocommit=True,connect_timeout=3)
except:
        timestamp = time.strftime("%H:%M:%S on %m %d %Y")
        sqllog.error("SQL did not connect at %s" % (timestamp))
        sys.exit(0)

mysql = conn.cursor(pymysql.cursors.DictCursor)
accepted = 0;
rejected = 0;
ambiguous = 0;
rowNum = 0;
check = []
try:
        mysql.execute("SELECT * FROM AppDevDB.StoreMainTable ORDER BY StoreInternalID DESC LIMIT 1")
        data = mysql.fetchall()
        temp = dict(data[0])
        rowNum = temp["StoreInternalID"] + 1
except:
        timestamp = time.strftime("%H:%M:%S on %m %d %Y")
        sqllog.error("Syntax error in main table execution for sql at %s" % (timestamp))
        sys.exit()
for i in range(0,len(reviews)):
        if os.path.getsize(reviews[i]) == 0:
                ambiguous = ambiguous + 1;
                timestamp = time.strftime("%H:%M:%S on %m %d %Y")
                ambiguouslog.info("Empty text file found for  %s at %s" % (reviews[i],timestamp))
                os.remove(reviews[i])
        else:
                r = open("%s" % (reviews[i]), errors='ignore',encoding='utf-8').readlines()
                BGS = False
                #We go through the file first to look for certain key terms in our list
                #If the string of words is found in the file, we automatically call it a bgs
                #and pass it into the store db.
                for c in range(0,len(r)):
                        str = r[c]
                        for j in range(0,len(isbgs)):
                                if isbgs[j] != "\n":
                                        txt = isbgs[j][:-1]
                                        if txt in str.lower():
                                                BGS = True
                                                # pass it into the store db code goes here.
                                                name = reviews[i].split("_review")
                                                exc = name
                                                print("%s found in the %s store" %(txt,exc))
                                                check.append(reviews[i])
                                                name = name[0].replace('\'','\\\'')
                                                timestamp = time.strftime("%H:%M:%S on %m %d %Y")
                                                try:
                                                        mysql.execute("SELECT * FROM AppDevDB.Yelp WHERE YelpID = '%s'" % (name))
                                                        data = mysql.fetchall()
                                                        result = dict(data[0])
                                                        if result["ApprovedByWebCrawler"] != 1:
                                                                mysql.execute("UPDATE `AppDevDB`.`Yelp` SET `ApprovedByWebCrawler`='1' WHERE `RowNumberKey`='%d';" % (result['RowNumberKey']))
                                                                mysql.execute("INSERT INTO `AppDevDB`.`StoreMainTable` (`StoreInternalID`) VALUES ('%d')" % (rowNum))
                                                                storeName = result['StoreName'].replace('\'','\\\'')
                                                                yelpID = result['YelpID'].replace('\'','\\\'')
                                                                imgURL = imageURL(result['YelpID'])
                                                                mysql.execute("UPDATE `AppDevDB`.`StoreMainTable` SET `StoreState`='%s' WHERE `StoreInternalID`='%d';" % (result['StoreState'],rowNum))
                                                                mysql.execute("UPDATE `AppDevDB`.`StoreMainTable` SET `StoreName`='%s' WHERE `StoreInternalID`='%d';" % (storeName,rowNum))
                                                                mysql.execute("UPDATE `AppDevDB`.`StoreMainTable` SET `StoreAddr1`='%s' WHERE `StoreInternalID`='%d';" % (result['StoreAddr1'],rowNum))
                                                                mysql.execute("UPDATE `AppDevDB`.`StoreMainTable` SET `StoreAddr2`='%s' WHERE `StoreInternalID`='%d';" % (result['StoreAddr2'],rowNum))
                                                                mysql.execute("UPDATE `AppDevDB`.`StoreMainTable` SET `StoreCity`='%s' WHERE `StoreInternalID`='%d';" % (result['StoreCity'],rowNum))
                                                                mysql.execute("UPDATE `AppDevDB`.`StoreMainTable` SET `StoreZip`='%s' WHERE `StoreInternalID`='%d';" % (result['StoreZip'],rowNum))
                                                                mysql.execute("UPDATE `AppDevDB`.`StoreMainTable` SET `StoreLat`='%s' WHERE `StoreInternalID`='%d';" % (result['StoreLat'],rowNum))
                                                                mysql.execute("UPDATE `AppDevDB`.`StoreMainTable` SET `StoreLon`='%s' WHERE `StoreInternalID`='%d';" % (result['StoreLon'],rowNum))
                                                                mysql.execute("UPDATE `AppDevDB`.`StoreMainTable` SET `YelpID`='%s' WHERE `StoreInternalID`='%d';" % (yelpID,rowNum))
                                                                mysql.execute("UPDATE `AppDevDB`.`StoreMainTable` SET `StoreImageTable`='%s' WHERE `StoreInternalID`='%d'" % (imgURL,rowNum))
                                                                acceptlog.info("%s store accepted at %s" % (exc,timestamp))
                                                                conn.commit()
                                                                accepted = accepted + 1
                                                                rowNum = rowNum + 1
                                                                os.remove(reviews[i])
                                                        else:
                                                                os.remove(reviews[i])
                                                except:
                                                        sqllog.error("deadlock error for %s store %d in the accepted log at %s", (name,timestamp))
                                if BGS == True:
                                        break;
                        if BGS == True:
                                break;
                if BGS == False:
                        #Next thing we check to see if the name of the shop contains the base word game, e.g. game, gamer, gaming, games, all would be advertisements of the main selling point of games, therefore board games.
                        #Code to check if the name of the store contains the base word game goes here.
                        '''
                        If the initial check fails, we need to create a different method to search for.
                        A game store by definition of reviews will contain at least one of the following items.
                        A list of genre's of games, such as card games, board games, trading card games, Role playing games
                        NOTE: Must be an obscure term within the genre, so adjectives such as physical, mental, exciting, may not refer to an actual board game
                        (E.g: Escape Room store: Exodus Escape Room.txt store)
                         By Definition of a  store as well: this merchandise will be known as a selection, stock, or even "store" as a Verb describing an object.
                         This SELECTION of items must be items that we deem are merchandise of a board game store, therefore a reviewer of a board game store must describe
                         a "Stock" of genres of games that are appropriate
                        A "Community" centered around gaming, so terms such as gaming community
                        Within a community setting we can search for the following items,
                        Tournaments (If the string game is mentioned as a subject within a review) we can assume the types of tournaments are game tournaments)
                        Gaming "Area": Basically an area where people are able to actually play games, this is commonly refered to in reviews as tables, gaming area, etc.
                        It must also be a "store", meaning by definition the only type of description of a store should ever be a "board game store" as a singular noun, or NNS
                        The merchandise of a store must be in consistence with that of the geek culture, meaning we must check the selection of stock the reviewers describe.
                        The stock must contain MAINLY stock in relations to games and maybe comic books. If a stores main attraction by reviewers is noted to be other stock that is not considered secondary
                        E.g, t-shirts, snacks, etc. Then it is not a gaming store.
                        '''
                        checkWords = str
                ##        #After the simple cases above, we need to use multiple conditions in order to determine if a buisness is a store.
                        for a in range(0,len(r)):
                                if r[a] == '\n':
                                        checkWords += " "
                                else:
                                        checkWords += r[a].lower()
                                timestamp = time.strftime("%H:%M:%S on %m %d %Y")
                        if "game" not in checkWords:
                                rejected = reject(reviews[i],check,rejected)
                        else:
                                notRejected = True
                                resWords = ["inventory","selection","sell","stock","products", "variety", "item", "items"]
                                buisness = ["shop", "store"]
                                rejectWords = ["company", "michaels", "gamestop", "toy", "arts", "crafts"]
                                ambiguousWords = ["magic", "board games", "card games", "selection of games", "cards", "selling games"]
                                if any(word in checkWords for word in buisness):
                                        if any(word in checkWords for word in rejectWords):
                                                notRejected = False
                                                rejected = reject(reviews[i],check,rejected)
                                        else:
                                                if any(word in checkWords for word in resWords):
                                                        for j in sent_tokenize(checkWords):
                                                                if notRejected == False:
                                                                        break;
                                                                if any(word in j for word in resWords):
                                                                        tagged = nltk.pos_tag(word_tokenize(j))
                                                                        for x in range(len(tagged)):
                                                                                if notRejected == False:
                                                                                        break;
                                                                                if tagged[x][1] == "NNS" or tagged[x][1] == "NN":
                                                                                        for line in rejectProd:
                                                                                                l = line.split('\n')
                                                                                                #print(tagged[x][0])
                                                                                                if tagged[x][0] in l[0]:
                                                                                                        print(tagged[x][0])
                                                                                                        print()
                                                                                                        notRejected = False
                                                                                                        rejected = reject(reviews[x],check,rejected)
                                                                                                        break
                                                else:
                                                        notRejected = False
                                                        print("game not in store")
                                                        rejected = reject(reviews[i],check,rejected)
                                else:
                                        notRejected = False
                                        print("game not in store")
                                        rejected = reject(reviews[i],check,rejected)
                        if "game" in reviews[i]:
                                if any(word in checkWords for word in ambiguousWords):
                                        notRejected = False
                                        name = reviews[i].split("_review")
                                        exc = name
                                        check.append(reviews[i])
                                        name = name[0].replace('\'','\\\'')
                                        timestamp = time.strftime("%H:%M:%S on %m %d %Y")
                                        try:
                                                mysql.execute("SELECT * FROM AppDevDB.Yelp WHERE YelpID = '%s'" % (name))
                                                data = mysql.fetchall()
                                                result = dict(data[0])
                                                if result["ApprovedByWebCrawler"] != 1:
                                                        mysql.execute("UPDATE `AppDevDB`.`Yelp` SET `ApprovedByWebCrawler`='1' WHERE `RowNumberKey`='%d';" % (result['RowNumberKey']))
                                                        mysql.execute("INSERT INTO `AppDevDB`.`StoreMainTable` (`StoreInternalID`) VALUES ('%d')" % (rowNum))
                                                        storeName = result['StoreName'].replace('\'','\\\'')
                                                        yelpID = result['YelpID'].replace('\'','\\\'')
                                                        imgURL = imageURL(result['YelpID'])
                                                        mysql.execute("UPDATE `AppDevDB`.`StoreMainTable` SET `StoreState`='%s' WHERE `StoreInternalID`='%d';" % (result['StoreState'],rowNum))
                                                        mysql.execute("UPDATE `AppDevDB`.`StoreMainTable` SET `StoreName`='%s' WHERE `StoreInternalID`='%d';" % (storeName,rowNum))
                                                        mysql.execute("UPDATE `AppDevDB`.`StoreMainTable` SET `StoreAddr1`='%s' WHERE `StoreInternalID`='%d';" % (result['StoreAddr1'],rowNum))
                                                        mysql.execute("UPDATE `AppDevDB`.`StoreMainTable` SET `StoreAddr2`='%s' WHERE `StoreInternalID`='%d';" % (result['StoreAddr2'],rowNum))
                                                        mysql.execute("UPDATE `AppDevDB`.`StoreMainTable` SET `StoreCity`='%s' WHERE `StoreInternalID`='%d';" % (result['StoreCity'],rowNum))
                                                        mysql.execute("UPDATE `AppDevDB`.`StoreMainTable` SET `StoreZip`='%s' WHERE `StoreInternalID`='%d';" % (result['StoreZip'],rowNum))
                                                        mysql.execute("UPDATE `AppDevDB`.`StoreMainTable` SET `StoreLat`='%s' WHERE `StoreInternalID`='%d';" % (result['StoreLat'],rowNum))
                                                        mysql.execute("UPDATE `AppDevDB`.`StoreMainTable` SET `StoreLon`='%s' WHERE `StoreInternalID`='%d';" % (result['StoreLon'],rowNum))
                                                        mysql.execute("UPDATE `AppDevDB`.`StoreMainTable` SET `YelpID`='%s' WHERE `StoreInternalID`='%d';" % (yelpID,rowNum))
                                                        mysql.execute("UPDATE `AppDevDB`.`StoreMainTable` SET `StoreImageTable`='%s' WHERE `StoreInternalID`='%d'" % (imgURL,rowNum))
                                                        acceptlog.info("%s store accepted at %s" % (exc,timestamp))
                                                        conn.commit()
                                                        accepted = accepted + 1
                                                        rowNum = rowNum + 1
                                                        os.remove(reviews[i])
                                                else:
                                                        os.remove(reviews[i])
                                        except:
                                                        sqllog.error("deadlock error for %s store %d in the accepted log at %s", (name,timestamp))
                        if notRejected:
                                name = reviews[i].split("_review")
                                name = name[0].replace('\'','\\\'')
                                ambiguouslog.info("%s determined to be ambiguous at %s" % (name,timestamp))
                                ambiguous = ambiguous + 1
                                shutil.move(os.curdir + "/" + reviews[i], move)
accept_rate = accepted/len(reviews)
reject_rate = rejected/len(reviews)
ambiguous_rate = ambiguous/len(reviews)
timestamp = time.strftime("%H:%M:%S on %m %d %Y")                                       
acceptlog.info("%d stores accepted at %s out of %d, rate of accepted stores is %f percent" % (accepted,timestamp,len(reviews),accept_rate))
rejectlog.info("%d stores rejected at %s out of %d, rate of accepted stores is %f percent" % (rejected,timestamp,len(reviews),reject_rate))
ambiguouslog.info("%d stores determined to be ambiguous at %s out of %d, rate of accepted stores is %f percent" % (ambiguous,timestamp,len(reviews), ambiguous))
'''
POS tag list:
CC      Coordinating conjunction
CD      Cardinal number
DT      Determiner
EX      Existential there
FW      Foreign word
IN      Preposition or subordinating conjunction
JJ      Adjective
JJR     Adjective, comparative
JJS     Adjective, superlative
LS      List item marker
MD      Modal
NN      Noun, singular or mass
NNS     Noun, plural
NNP     Proper noun, singular
NNPS    Proper noun, plural
PDT     Predeterminer
POS     Possessive ending
PRP     Personal pronoun
PRP$    Possessive pronoun
RB      Adverb
RBR     Adverb, comparative
RBS     Adverb, superlative
RP      Particle
SYM     Symbol
TO      to
UH      Interjection
VB      Verb, base form
VBD     Verb, past tense
VBG     Verb, gerund or present participle
VBN     Verb, past participle
VBP     Verb, non-3rd person singular present
VBZ     Verb, 3rd person singular present
WDT     Wh-determiner
WP      Wh-pronoun
WP$     Possessive wh-pronoun
WRB     Wh-adverb
'''
