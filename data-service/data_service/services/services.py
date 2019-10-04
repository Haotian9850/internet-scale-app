import requests
from pprint import pprint
from django.core import serializers
import json

BASE_URL = "http://models:8000/api/v1/"

def get_all_pets():
    res = requests.get("http://models:8000/api/v1/pets/get_all_pets")
    #pprint(res)
    #return serializers.serialize('json', res.encode('utf-8'))
    return json.loads(res.text)['res']