import requests
import json

BASE_URL = "http://entity:8000/api/v1/"

def get_all_pets():
    try:
        res = requests.get(BASE_URL + "pets/get_all_pets")
    except requests.exceptions.Timeout:
        return "Request timed out"
    except requests.exceptions.HTTPError as err:
        return "Request failed with HTTPError " + err.response.text
    return json.loads(res.text)['res']