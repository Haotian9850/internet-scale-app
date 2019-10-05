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
    print (res.text)
    return json.loads(res.text)['res'], 1
