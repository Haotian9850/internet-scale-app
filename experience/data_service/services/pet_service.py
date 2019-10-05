import requests
import json

import constants

def get_all_pets():
    try:
        res = requests.get(constants.BASE_URL + "pets/get_all_pets")
    except requests.exceptions.Timeout:
        return "Request timed out", 0
    except requests.exceptions.HTTPError as err:
        return "Request failed with HTTPError " + err.response.text, 0
    if type(json.loads(res.text)['res']) is str:
        return "Currently, no pet is available in our inventory", 1
    return json.loads(res.text)['res'], 1