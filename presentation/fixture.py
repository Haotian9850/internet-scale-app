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
        print("ERROR: fixture.py - create_pets() timeout")
    except requests.exceptions.HTTPError as err:
        print("ERROR: fixture.py - create_pets() Request failed with HttpError {}".format(err.response.text))
    print("SUCCESS: {}".format(json.loads(res.text)['res']))


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
        print("ERROR: fixture.py - login() timeout")
    except requests.exceptions.HTTPError as err:
        print("ERROR: fixture.py - login() Request failed with HttpError {}".format(err.response.text))
    if not json.loads(res.text)["ok"]:
        print("ERROR: fixture.py - login() cannot load response for requests.post()")
    print("SUCCESS: logged in for user {}".format(username))
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
        print("ERROR: fixture.py - logout() timeout")
    except requests.exceptions.HTTPError as err:
        print("ERROR: fixture.py - logout() Request failed with HttpError {}".format(err.response.text))
    print("SUCCESS: logged out with authenticator {}".format(authenticator))
    return json.loads(res.text)["res"]


def register(user_data):
    try:
        res = requests.post(
            url=constants.BASE_URL + "test/create_user",
            data=user_data
        )
    except requests.exceptions.Timeout:
        print("ERROR: fixture.py - register() timeout")
    except requests.exceptions.HTTPError as err:
        print("ERROR: fixture.py - register() Request failed with HttpError {}".format(err.response.text))    
    print("SUCCESS: user registered")
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
        print("ERROR: fixture.py - view_pet_by_id() timeout")
    except requests.exceptions.HTTPError as err:
        print("ERROR: fixture.py - view_pet_by_id() Request failed with HttpError {}".format(err.response.text))
    print("SUCCESS: viewing pet with id {}".format(id))
    return json.loads(res.text)["res"]




if __name__ == "__main__":
    username = "test_user"

    user_data = {
        "username": "test_user",
        "first_name": "Team",
        "last_name": "Portia",
        "email_address": "MammaMia@abba.com",
        "age": 32,
        "gender": "None",
        "zipcode": 22904,
        "password": "ABC123456789"
    }

    pet1_data = {
        "name": "samoyed",
        "pet_type": "dog",
        "description": "Description for samoyed",
        "price": 13.00
    }

    pet2_data = {
        "name": "lab",
        "pet_type": "dog",
        "description": "Description for lab",
        "price": 14.00
    }

    pet3_data = {
        "name": "persian cat",
        "pet_type": "cat",
        "description": "Description for Persian cat",
        "price": 15.00
    }

    register(user_data)

    authenticator = login(username, user_data["password"])

    create_pet(pet1_data, username, authenticator)
    create_pet(pet2_data, username, authenticator)
    create_pet(pet3_data, username, authenticator)
    
    logout(authenticator)

    for i in range(5):
        authenticator = login(username, user_data["password"])
        view_pet_by_id(username, 1)
        view_pet_by_id(username, 2)
        view_pet_by_id(username, 3)
        
        logout(authenticator)
