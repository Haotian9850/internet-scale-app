import requests
from pprint import pprint

BASE_URL = "http://localhost:8001/api/v1/"

def get_all_pets():
    res = requests.post(BASE_URL + "pets/get_all_pets")
    pprint(res.json())

get_all_pets()