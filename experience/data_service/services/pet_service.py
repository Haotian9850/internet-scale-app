import requests
import json

BASE_URL = "http://entity:8000/api/v1/"

def get_all_pets():
    try:
        res = requests.get(BASE_URL + "pets/get_all_pets")
    except requests.exceptions.Timeout:
        return "Request timed out", 0
    except requests.exceptions.HTTPError as err:
        return "Request failed with HTTPError " + err.response.text, 0
    return json.loads(res.text)['res'], 1
