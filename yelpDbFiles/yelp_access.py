from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
def access():
    auth = Oauth1Authenticator(
    consumer_key="EE0eorpPAC1pnOks_6UwiQ",
    consumer_secret="2Ro847QVwq3_xsQnGCMsqgkKdkg",
    token="G1im9LAR9gLLkvG9MU13kN0jgIKPj0Xj",
    token_secret="nD0JslboG_qKU6xR36OVP7w9S5c"
    )
    return auth

