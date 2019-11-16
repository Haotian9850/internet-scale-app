from base64 import b64encode
import os

def get_new_authenticator(size):
    result = b64encode(os.urandom(size)).decode('utf-8')
    while result.find("/") != -1:
        result = b64encode(os.urandom(size)).decode('utf-8')
    return result 
