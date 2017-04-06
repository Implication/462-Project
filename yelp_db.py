import pymysql
import re

# connect to Yelp DB and extract URL and 
# return URLs that are not approved.
def get_yelp_store_url_appr_status():
    store_url = {}
    try:
        conn = pymysql.connect(user="RemoteUser", passwd="Rem@teMiq3924",host="104.236.52.47", port=3306,database="AppDevDB")   
        #conn = pymysql.connect(user="YelpDumpUser", passwd="#&489Wj8!p",host="localhost", port=3306,database="AppDevDB")
    except:
        print("Failed to connect to database")
        #sys.exit(0)
            
    c = conn.cursor()
    #Note: May change later to get number of rows directly from sql itself
    try:
        c.execute("SELECT YelpURL,ApprovedByWebCrawler,StoreName FROM Yelp") #Get all the rows of c,execute
        url_rows = c.fetchall()
        for row in url_rows:
            if(row[1]!=1): #URL not approved
                    store_url[row[2]] = row[0]
            else:
                unapproved = row[0]
    except:
        print("Database error in execute")
        
    finally:
        c.close()

    return store_url 