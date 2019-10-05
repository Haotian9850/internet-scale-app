import requests
import json 

from .. import constants

def get_all_pets():
    try:
        res = requests.get(constants.BASE_URL + "get_all_pets")
    except requests.exceptions.Timeout:
        return "Request timed out", 0
    except requests.exceptions.HTTPError as err:
        return "Request failed with HTTPError " + err.response.text, 0
    if type(json.loads(res.text)['res']) is str:
        return "Currently, no pet is available in our inventory", 1
    return json.loads(res.text)['res'], 1


def search_pets(keyword):
    try:
        res = requests.post(
            url = constants.BASE_URL + "search_pets",
            data={
                'keyword': keyword
            }
        )
    except requests.exceptions.Timeout:
        return "Request timed out", 0
    except requests.exceptions.HTTPError as err:
        return "Request failed with HTTPError " + err.response.text, 0
    return json.loads(res.text)['res'], 1



def sort_pets(sort_by):
    try:
        res = requests.post(
            url = constants.BASE_URL + "sort_pets",
            data = {
                "sort_by": sort_by
            }
        )
    except requests.exceptions.Timeout:
        return "Request timed out", 0
    except requests.exceptions.HTTPError as err:
        return "Request failed with HTTPError " + err.response.text, 0
    return json.loads(res.text)['res'], 1