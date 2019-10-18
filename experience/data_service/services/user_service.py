import requests 
import json 

import constants

def get_all_users():
    try:
        res = requests.get(constants.BASE_URL + "users/get_all_users")
    except requests.exceptions.Timeout:
        return "Request timed out", 0
    except requests.exceptions.HTTPError as err:
        return "Request failed with HttpError {}".format(err.response.text), 0
    return json.loads(res.text)["res"], 1


# TODO: add err handling when user not found
def log_in(username, password):
    try:
        res = requests.post(
            url=constants.BASE_URL + "login",
            data={
                "username": username,
                "password": password
            }
        )
    except requests.exceptions.Timeout:
        return "Request timed out", 0
    except requests.exceptions.HTTPError as err:
        return "Request failed with HttpError {}".format(err.response.text), 0
    return json.loads(res.text)["res"], 1



def log_out(authenticator):
    try:
        res = requests.post(
            url=constants.BASE_URL + "logout",
            data={
                "authenticator": authenticator
            }
        )
    except requests.exceptions.Timeout:
        return "Request timed out", 0
    except requests.exceptions.HTTPError as err:
        return "Request failed with HttpError {}".format(err.response.text), 0
    return json.loads(res.text)["res"], 1
