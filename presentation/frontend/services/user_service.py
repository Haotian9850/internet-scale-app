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
    if not json.loads(res.text)["ok"]:
        return json.loads(res.text)["res"], -1
    return json.loads(res.text)["res"], 1



def log_out_service(authenticator):
    try:
        res = requests.post(
            url=constants.BASE_URL + "/test/logout",
            data={
                "authenticator": authenticator
            }
        )
    except requests.exceptions.Timeout:
        return "Request timed out", 0
    except requests.exceptions.HTTPError as err:
        return "Request failed with HttpError {}".format(err.response.text), 0
    return json.loads(res.text)["res"], 1


    
    
def register_service(request):
    try:
        res = requests.post(
            url=constants.BASE_URL + "/test/create_user",
            data={
                "username": request.POST["username"],
                "first_name": request.POST["first_name"],
                "last_name": request.POST["last_name"],
                "email_address": request.POST["email_address"],
                "age": request.POST["age"],
                "gender": request.POST["gender"],
                "zipcode": request.POST["zipcode"],
                "password": request.POST["password"]
            }
        )
    except requests.exceptions.Timeout:
        return "Request timed out", 0
    except requests.exceptions.Timeout as err:
        return "Request failed with HttpError {}".format(err.response.text), 0
    if not json.loads(res.text)["ok"]:
        return json.loads(res.text)["res"], -1
    return json.loads(res.text)["res"], 1