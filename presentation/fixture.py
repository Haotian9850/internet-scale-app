import requests
import json 

import constants

def create_pet(pet_data, username, authenticator):
    try:
        res = requests.post(
            url=constants.BASE_URL + "test/create_pet",
            data={
                "name": pet_data["name"],
                "pet_type": pet_data["pet_type"],
                "description": pet_data["description"],
                "price": pet_data["price"],
                "username": username,
                "authenticator": authenticator
            }
        )
    except requests.exceptions.Timeout:
        print("Error: fixture.py - create_pets() timeout")
    except requests.exceptions.HTTPError as err:
        print("Error: fixture.py - create_pets() Request failed with HttpError {}".format(err.response.text))
    return json.loads(res.text)['res']

def login(username, password):
    try:
        res = requests.post(
            url=constants.BASE_URL + "test/login",
            data={
                "username": username,
                "password": password
            }
        )
    except requests.exceptions.Timeout:
        print("Error: fixture.py - login() timeout")
    except requests.exceptions.HTTPError as err:
        print("Error: fixture.py - login() Request failed with HttpError {}".format(err.response.text))
    if not json.loads(res.text)["ok"]:
        print("Error: fixture.py - login() cannot load response for requests.post()")
    return json.loads(res.text)["res"]

def logout(authenticator):
    try:
        res = requests.post(
            url=constants.BASE_URL + "test/logout",
            data={
                "authenticator": authenticator
            }
        )
    except requests.exceptions.Timeout:
        print("Error: fixture.py - logout() timeout")
    except requests.exceptions.HTTPError as err:
        print("Error: fixture.py - logout() Request failed with HttpError {}".format(err.response.text))
    return json.loads(res.text)["res"]

def register(user_data):
    try:
        res = requests.post(
            url=constants.BASE_URL + "test/create_user",
            data=user_data
        )
    except requests.exceptions.Timeout:
        print("Error: fixture.py - register() timeout")
    except requests.exceptions.HTTPError as err:
        print("Error: fixture.py - register() Request failed with HttpError {}".format(err.response.text))
    #if not json.loads(res.text)["ok"]:
     #   print("Error: fixture.py - register() cannot load response for requests.post()")
    
    print(res.text)
    return json.loads(res.text)["res"]

def view_pet_by_id(username, id):
    try: 
        res = requests.post(
            url=constants.BASE_URL + "get_pet_by_id",
            data={
                "id": id,
                "username": username
            }
        )
    except requests.exceptions.Timeout:
        print("Error: fixture.py - view_pet_by_id() timeout")
    except requests.exceptions.HTTPError as err:
        print("Error: fixture.py - view_pet_by_id() Request failed with HttpError {}".format(err.response.text))

    print(res.text)
    return json.loads(res.text)["res"]

def main():
    username = "fixture_script_user"
    user_data = {
        "username": username,
        "first_name": "Mamma",
        "last_name": "Mia",
        "email_address": "MammaMia@abba.com",
        "age": 32,
        "gender": "None",
        "zipcode": 22904,
        "password": "DanielSmells1962"
    }

    register(user_data)
    authenticator = login(username, user_data["password"])

    pet1_data = {
        "name": "dog1",
        "pet_type": "dog",
        "description": "dog1 description",
        "price": 13.00,
    }

    pet2_data = {
        "name": "cat1",
        "pet_type": "cat",
        "description": "cat1 description",
        "price": 14.00,
    }

    pet3_data = {
        "name": "cat2",
        "pet_type": "cat",
        "description": "cat2 description",
        "price": 15.00,
    }

    pet1_id = create_pet(pet1_data, username, authenticator)
    pet2_id = create_pet(pet2_data, username, authenticator)
    pet3_id = create_pet(pet3_data, username, authenticator)

    view_pet_by_id(username, 1)
    view_pet_by_id(username, 2)
    view_pet_by_id(username, 3)

    logout(authenticator)


main()