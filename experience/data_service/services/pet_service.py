import requests
import json

from services.kafka_service import get_kafka_producer

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


def get_pet_by_id_service(request):
    # no need for exception handling
    try: 
        res = requests.post(
            url=constants.BASE_URL + "pets/get_by_id",
            data={
                "id": request.POST.get("id")
            }
        )
        

    except requests.exceptions.Timeout:
        return "Request timed out", 0
    except requests.exceptions.HTTPError as err:
        return "Request failed with HTTPError {}".format(err.response.text), 0
    return json.loads(res.text)["res"], 1

    '''
    if kafka_status is True:
        return json.loads(res.text)["res"], 1
    else:
        return json.loads(res.text)["res"], 2   # msg not send
        '''



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
        name = request.POST.get("name"),
        pet_type = request.POST.get("pet_type"),
        description = request.POST.get("description"),
        price = request.POST.get("price"),
        authenticator = request.POST.get("authenticator"),
        username = request.POST.get("username")

        res = requests.post(
            constants.BASE_URL + "pets/create",
            data={
                "name": name,
                "pet_type": pet_type,
                "description": description,
                "price": price,
                "authenticator": authenticator,
                "username": username
            }
        )

        producer = get_kafka_producer()
        kafka_status = send_new_pet(
            producer,
            {
                "name": name,
                "pet_type": pet_type,
                "description": description,
                "price": price,
                "pet_id": json.loads(res.text)["res"]
            }
        )

    except requests.exceptions.Timeout:
        return "Request timed out", 0
    except requests.exceptions.HTTPError as err:
        return "Request failed with HTTPError {}".format(err.response.text), 0
    if kafka_status is True:
        return "New pet with pet_id {} is successfully created and put on Kafka queue.".format(json.loads(res.text)["res"]), 1 
    else:
        return "New pet with pet_id {} is successfully created but not put on Kafka queue.".format(json.loads(res.text)["res"]), 1 