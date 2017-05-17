import pymysql
import re
import sys

# connect to Yelp DB and extract URL and 
# return URLs that are not approved.
def get_yelp_store_url_appr_status():
    file = open("/home/pythonUser/WebCrawlerYelp/count.txt", "r+")
    row = int(file.read())
    store_url = str
    approved = True
    try:
        conn = pymysql.connect(user="RemoteUser", passwd="Rem@teMiq3924",host="tabletopfinder.com", port=3306,database="AppDevDB")
    except:
        print("Failed to connect to database")
        sys.exit(0)
    c = conn.cursor()
    while(approved):
        try:
            c.execute("SELECT `YelpURL`,`ApprovedByWebCrawler` FROM `AppDevDB`.`Yelp` WHERE `RowNumberKey` = '%d'" % (row)) #Get all the rows of c,execute
            url_rows = c.fetchall()
            if(url_rows[0][1]!= 1 and url_rows[0][1] != 0): #URL not approved
                store_url = url_rows[0][0]
                approved = False
            else:
                approved = True
                row = row + 1
        except:
            print("Database error in execute")
            sys.exit(0)
    c.close()
    conn.close()
    file.close()
    file = open("count.txt", "w")
    file.write(str(row + 1))
    file.close()
    return store_url
