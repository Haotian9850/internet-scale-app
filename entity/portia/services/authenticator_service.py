from base64 import b64encode
import os

def get_new_authenticator(size):
    return b64encode(os.urandom(size)).decode('utf-8')
