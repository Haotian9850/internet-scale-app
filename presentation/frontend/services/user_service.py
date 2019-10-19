import requests
import json  

import constants


def log_in_service(username, password):
    try: 
        res = requests.post(
            url=constants.BASE_URL + "test/login",
            data={
                "username": username,
                "password": password
            }
        )
    except requests.exceptions.Timeout:
        return "Request timed out", 0
    except requests.exceptions.HTTPError as err:
        return "Request failed with HTTPError {}".format(err.response.text), 0
    return json.loads(res.text)["res"], 1





def log_out_service(authenticator):
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

# TODO: add register service call