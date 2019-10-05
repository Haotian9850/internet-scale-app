import requests 
import json 

import constants

def get_all_users():
    try:
        res = requests.get(constants.BASE_URL + "users/get_all_users")
    except requests.exceptions.Timeout:
        return "Request timed out", 0
    except requests.exceptions.HTTPError as err:
        return "Request failed with HttpError " + err.response.text, 0
    return json.loads(res.text)['res'], 1