import datetime
from django import db
from django.db import IntegrityError
from main import models 
import json

from utils.err_msg_assembler import assemble_err_msg
from utils.res_handler import res_err, res_success


def create_user(request):
    if request.method != 'POST':
        return res_err(assemble_err_msg(-1, "WRONG_REQUEST_METHOD", "POST"))

    new_user = models.User(
        username = request.POST.get('username'), 
        first_name = request.POST.get('first_name'), 
        last_name = request.POST.get('last_name'), 
        email_address = request.POST.get('email_address'), 
        age = request.POST.get('age'),
        gender = request.POST.get('gender'),
        date_joined = datetime.datetime.now(), 
        zipcode = request.POST.get('zipcode'), 
        password = request.POST.get('password')
    )
    
    try:
        new_user.save()
    except (db.Error, IntegrityError) as e:
        return res_err("Create user transaction failed with error " + str(e.args))
    return res_success("New user with user_id " + str(new_user.pk) + " is successfully created!")


def get_user_by_id(request, user_id):
    if request.method != 'GET':
        return res_err(assemble_err_msg(-1, "WRONG_REQUEST_METHOD", "GET"))
    try:
        user = models.User.objects.get(pk=user_id)
    except models.User.DoesNotExist:
        return res_err(assemble_err_msg(user_id, "NOT_FOUND", "User"))
    return res_success({
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'age': user.age,
        'gender': user.gender,
        'email_address': user.email_address,
        'date_joined': user.date_joined,
        'zipcode': user.zipcode,
        'password': user.password
    })




def update_user(request, user_id):
    if request.method != 'POST':
        return res_err(assemble_err_msg(-1, "WRONG_REQUEST_METHOD", "POST"))
    try:
        user = models.User.objects.get(pk=user_id)
    except models.User.DoesNotExist:
        return res_err(assemble_err_msg(user_id, "NOT_FOUND", "User"))
    new_attributes_updated = False 
    if request.POST.get("first_name"):
        user.first_name = request.POST.get("first_name")
        new_attributes_updated = True
    if request.POST.get("last_name"):
        user.last_name = request.POST.get("last_name")
        new_attributes_updated = True
    if request.POST.get("email_address"):
        user.email_address = request.POST.get("email_address")
        new_attributes_updated = True
    if request.POST.get("zipcode"):
        user.zipcode = request.POST.get("zipcode")
        new_attributes_updated = True
    if request.POST.get("password"):
        user.password = request.POST.get("password")
        new_attributes_updated = True 

    if not new_attributes_updated:
        return res_success("No field is updated.")
    else:
        return res_success("User with user_id" + user_id + " is successfully updated.")
    



def delete_user(request, user_id):
    if request.method != "GET":
        return res_err(assemble_err_msg(-1, "WRONG_REQUEST_METHOD", "GET"))
    try:
        user = models.User.objects.get(pk=user_id)
    except models.User.DoesNotExist:
        return res_err(assemble_err_msg(user_id, "NOT_FOUND", "User"))
    user.delete()
    return res_success("User with user_id " + user_id + " is successfully deleted." + str(request.method))




def create_pet(request):
    if request.method != 'POST':
        return res_err(assemble_err_msg(-1, "WRONG_REQUEST_METHOD", "POST"))
    new_pet = models.Pet(
        name = request.POST.get('name'), 
        pet_type = request.POST.get('pet_type'), 
        description = request.POST.get('description'),
        price = request.POST.get('price'),
        date_posted = datetime.datetime.now()
    )
    try:
        new_pet.save()
    except db.Error:
        return res_err(str(db.Error))
    return res_success("New Pet with pet_id " + str(new_pet.pk) + " is successfully created!")




def get_all_pets(request):
    all_pets = []
    if request.method != 'GET':
        return res_err(assemble_err_msg(-1, "WRONG_REQUEST_METHOD", "GET"))
    try:
        # make result list
        for pet in models.Pet.objects.all():
            new_pet = {
                'name': pet.name,
                'pet_type': pet.pet_type,
                'description': pet.description,
                'price': pet.price,
                'date_posted': pet.date_posted
            }
            all_pets.append(new_pet)
    except db.Error:
        return res_err(str(db.Error))
    return res_success(all_pets)




def get_pet_by_id(request, pet_id):
    if request.method != 'GET':
        return res_err(assemble_err_msg(-1, "WRONG_REQUEST_METHOD", "GET"))
    try:
        pet = models.Pet.objects.get(pk=pet_id)
    except models.Pet.DoesNotExist:
        return res_err(assemble_err_msg(pet_id, "NOT_FOUND", "Pet"))
    return res_success({
        'name': pet.name,
        'pet_type': pet.pet_type,
        'description': pet.description,
        'price': pet.price,
        'date_posted': pet.date_posted,
    })




def update_pet(request, pet_id):
    if request.method != 'POST':
        return res_err(assemble_err_msg(-1, "WRONG_REQUEST_METHOD", "POST"))
    try:
        pet = models.Pet.objects.get(pk=pet_id)
    except models.Pet.DoesNotExist:
        return res_err(assemble_err_msg(pet_id, "NOT_FOUND", "Pet"))
    new_attributes_updated = False 
    if request.POST.get("name"):
        pet.name = request.POST.get("name")
        new_attributes_updated = True
    if request.POST.get("pet_type"):
        pet.pet_type = request.POST.get("pet_type")
        new_attributes_updated = True
    if request.POST.get("description"):
        pet.description = request.POST.get("description")
        new_attributes_updated = True
    if request.POST.get("price"):
        pet.price = request.POST.get("price")
        new_attributes_updated = True
    if not new_attributes_updated:
        return res_success("No field is updated.")
    else:
        return res_success("Pet with pet_id " + pet_id + " is successfully updated.")
    



def delete_pet(request, pet_id):
    if request.method != "GET":
        return res_err(assemble_err_msg(-1, "WRONG_REQUEST_METHOD", "GET"))
    try:
        pet = models.Pet.objects.get(pk=pet_id)
    except models.Pet.DoesNotExist:
        return res_err(assemble_err_msg(pet_id, "NOT_FOUND", "Pet"))
    pet.delete()
    return res_success("Pet with pet_id" + pet_id + " is successfully deleted.")

 




