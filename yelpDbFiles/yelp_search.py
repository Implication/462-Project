from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import os
import yelp_access
import pymysql
import logging
import time
import sys
import os

# Authenticate our yelp keys
# with io.open('yelp_config.json') as cred:
#        creds = json.load(cred)
#        auth = Oauth1Authenticator(**creds)
#        client = Client(auth)

# TEMPORARY - Allows developer access to yelp api
auth = yelp_access.access()
client = Client(auth)

# Factory method to implement multiple logs based on the information


def setup_log(name, filename, level):
    l = logging.getLogger(name)
    format = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = logging.FileHandler(filename)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(format)
    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)

cwd = os.getcwd()
path = os.curdir + "/log_file"
print(cwd)
logfile = path + "/commits.log"
setup_log('commited',logfile , logging.INFO)
logfile = path + "/sql.log"
setup_log('sqllog',logfile, logging.ERROR)
logfile = path +  "/zip.log"
setup_log('ziplog',logfile, logging.ERROR)
logfile = path + "/value.log"
setup_log('valuelog', logfile, logging.ERROR)
ziplog = logging.getLogger('ziplog')
valuelog = logging.getLogger('valuelog')
commitlog = logging.getLogger('commited')
sqllog = logging.getLogger('sqllog')

# We can now use client to search parameters
# optional paramaters:
# Term: is the search term, if this is not included if searches everything, it also accepts buisness names
# limit: is the  number of buisness results to return
# offset: offsets teh list of returned buisnesses by the amount specified here
# sort: sorts by a number, 0 is best matches, 1 is distance, and 2 is highest rated
# category_filler filter search results with a category, all categories
# supported can be found here
# https://www.yelp.com/developers/documentation/v2/all_category_list


params = {
    'term': "board games",
    'lang': 'fr',
    'offset': 0,
    'limit': 40,
    'sort': 0,
    'category_filter': "tabletopgames"
}

# Client Search Function:
# Can be used to search by location which can by specified by neighborhood, address or city.
# Can be used to search by a bounding box, which takes a southwest and a northwest lat/long for values
# Can be used to search also by geographic coordinates, which requires a lat/long
# Optional parameters are accuracy, altitude, and altitude_accuracy

# Documentation can be found at
# https://www.yelp.com/developers/documentation/v2/search_api

try:
    conn = pymysql.connect(user="RemoteUser", passwd="Rem@teMiq3924",
                           host="tabletopfinder.com", port=3306, database="AppDevDB")
except:
    timestr = time.strftime("%H:%M:%S on %m %d %Y")
    sqllog.error("SQL did not connect at %s" % (timestr))
    sys.exit(0)

c = conn.cursor()
# Note: May change later to get number of rows directly from sql itself
num = 0
try:
    # Get all the rows of c,execute
    c.execute("SELECT * FROM `AppDevDB`.`Yelp`")
except:
	c.close()
	conn.close()
	sqllog.error("Database error in execute")
	sys.exit(0)
for i in list(c):
    num = num + 1
# Iterate and increment num by 1 for each row
# Increment num by one more, to specify the next row.
num = num + 1
numofcommits = num
badzips = open(os.curdir + "/badzips.txt", "a+")
counter = open(os.curdir + "/counter.txt", 'r')
zip = int(counter.read())
if zip >= 99999:
    zip = 10000
badidr = open(os.curdir + "/badids.txt", "r")
for area in range(zip, zip + 30):
    print("Area is %d" % (area))
    apiExists = True
    for j in badzips:
        if j == (str(area) + "\n"):
            apiExist = False
            break
    if apiExists:
        try:
            r = client.search(area, **params)
        except:
            ziplog.error(
                "Search failed for  %d, does not exist in the API" % (area))
            badzips.write(str(area) + "\n")
            print("Area is not in API %d" % (area))
            continue
        for i in range(len(r.businesses)):
            isDuplicate = False
            c.execute("SELECT `YelpID` FROM `AppDevDB`.`Yelp`")
            for b in list(c):
                s = str(b)
                yelpID = s[2:len(s) - 3]
                if r.businesses[i].id == yelpID:
                    isDuplicate = True
                    break
            if isDuplicate == False and r.businesses[i].location.country_code == "US":
                noa = 0
                a1 = ""
                a2 = ""
                name = ""
                addr1 = ""
                addr2 = ""
                yelpID = r.businesses[i].id
                for k in r.businesses[i].name:
                    if k == '\'':
                        name += "\\'"
                    else:
                        name += k
                for j in r.businesses[i].location.address:
                    if noa == 0:
                        a1 = j
                    if noa == 1:
                        a2 = j
                    noa = noa + 1
                for j in a1:
                    if j == '\'':
                        addr1 += "\\'"
                    else:
                        addr1 += j
                for j in a2:
                    if j == '\'':
                        addr2 += "\\'"
                    else:
                        addr2 += j
                lat = int(r.businesses[i].location.coordinate.latitude * 10000)
                long = int(
                    r.businesses[i].location.coordinate.longitude * 10000)
                url = "https://www.yelp.com/biz/" + r.businesses[i].id
                try:
                    c.execute("INSERT INTO `AppDevDB`.`Yelp` (`RowNumberKey`, `StoreName`, `StoreAddr1`, `StoreAddr2`, `StoreCity`, `StoreState`, `StoreZip`, `YelpID`, `YelpURL`, `StoreLat`, `StoreLon`) VALUES ('%d', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%s', '%d', '%d');"
                              % (num, name, addr1, addr2, r.businesses[i].location.city, r.businesses[i].location.state_code, int(r.businesses[i].location.postal_code), yelpID, url, lat, long))
                    num = num + 1
                    conn.commit()
                except:
                    newID = True
                    for j in badidr:
                        if j == r.businesses[i].id + "\n":
                            newID = False
                            break
                    if newID:
                        badidw = open(
                            os.curdir + "/badids.txt", "a")
                        valuelog.error(
                            """Value could not be entered into the query,
				 either a character could not be read or theirs a
				 single quote. Id is %s, at %s""" % (yelpID, time))
                        valuelog.error("id %s" % (yelpID))
                    continue
replace = open(os.curdir + "/counter.txt", 'w')
replace.write(str(zip + 20))
replace.close()
badidr.close()
badzips.close()
time = time.strftime("%H:%M:%S on %m %d %Y")
if num - numofcommits > 0:
	commitlog.info("Program ran successfully on %s, number of commits is %d" % (
    	time, (num - numofcommits)))
logging.shutdown()
c.close()
conn.close()

