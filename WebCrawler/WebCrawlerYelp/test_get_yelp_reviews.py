from get_yelp_reviews import get_yelp_reviews
from yelp_db import get_yelp_store_url_appr_status
import re
import os
import time


store_url = get_yelp_store_url_appr_status()

s = store_url.split('/',4)
store_name = s[4]

localtime = time.asctime( time.localtime(time.time()) )
print("###################################################Start of Script############################################################")
print ("Local current time :", localtime, " Store name: ", store_name, " With store URL: ", store_url)
get_yelp_reviews(store_url,store_name)

##max_print_file_count = 5
##term_str = ""

##save_path = "./store_reviews/" 
 
##file_count = 0
##if(store_url):
##    for store in store_url:
##        if('/' in store):
##            store_t = store.replace("/", "")
##        else:
##            store_t = store            
##        store_name = os.path.join(save_path, store_t+".txt") 
##        print(store, ": ", file_count)
##        if(file_count < max_print_file_count):
##            f1 = open(store_name, 'w')
##            print(store_url[store])
##            terms_dic = get_yelp_reviews(store_url[store], store)
##            if(file_count < max_print_file_count):
##                for term in terms_dic:               
##                    try:
##                        print(term, ": ", terms_dic[term], file= f1)
##                    except:
##                        print("UnicodeEncodeError")
##                f1.close()
##        file_count = file_count + 1
