import requests
import json

from kafka_service import send_new_pet

import constants

# check HTTP-related errors only (other error msgs should be passed from entity)
def get_all_pets_service():
    try:
        res = requests.get(constants.BASE_URL + "pets/get_all_pets")
    except requests.exceptions.Timeout:
        return "Request timed out", 0
    except requests.exceptions.HTTPError as err:
        return "Request failed with HTTPError " + err.response.text, 0
    if type(json.loads(res.text)['res']) is str:
        return "Currently, no pet is available in our inventory", 1
    return json.loads(res.text)['res'], 1


def get_pets_by_user_service(request):
    try: 
        res = requests.post(
            url=constants.BASE_URL + "pets/get_by_user",
            data={
                "username": request.POST["username"]
            }
        )
    except requests.exceptions.Timeout:
        return "Request timed out", 0
    except requests.exceptions.HTTPError as err:
        return "Request failed with HTTPError {}".format(err.response.text), 0
    return json.loads(res.text)["res"], 1



def create_pet_service(request):
    try:
        res = requests.post(
            constants.BASE_URL + "pets/create",
            data={
                "name": request.POST.get("name"),
                "pet_type": request.POST.get("pet_type"),
                "description": request.POST.get("description"),
                "price": request.POST.get("price"),
                "authenticator": request.POST.get("authenticator"),
                "username": request.POST.get("username")
            }
        )
        send_new_pet(request)
    except request.exceptions.Timeout:
        return "Request timed out", 0
    except request.exceptions.HTTPError as err:
        return "Request failed with HTTPError {}".format(err.response.text), 0
    return json.loads(res.text)['res'], 1 