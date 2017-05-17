from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import yelp_access
import pymysql
import logging
import time
import sys
import os

def imageURL(id):
        auth = yelp_access.access()
        client = Client(auth)
        response = client.get_business(id)
        return response.business.image_url


