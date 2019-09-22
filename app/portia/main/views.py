import datetime
from django import db
from main import models 

from utils.err_msg_assembler import assemble_err_msg
from utils.res_handler import res_err, res_success



def create_user(request):
    if request.method != 'POST':
        return res_err(assemble_err_msg(-1, "WROUNG_REQUEST_METHOD", "POST"))
    
    new_user = models.User(
        username = request.POST['username'], 
        first_name = request.POST['first_name'], 
        last_name = request.POST['last_name'], email_address = request.POST['email'], 
        age = request.POST['age'],
        gender = request.POST['gender'],
        date_joined = datetime.datetime.now(), location=request.POST['location'],
        zipcode = request.POST['zipcode'], 
        password = request.POST['password']
    )

    try:
        new_user.save()
    except db.Error:
        return res_err(str(db.Error))
    return res_success(new_user.pk)




def get_user_by_id(request, user_id):
    if request.method != 'GET':
        return res_err(assemble_err_msg(-1, "WROUNG_REQUEST_METHOD", "GET"))
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
    if request.method != 'GET':
        return res_err(assemble_err_msg(-1, "WROUNG_REQUEST_METHOD", "GET"))
    try:
        user = models.User.objects.get(pk=user_id)
    except models.User.DoesNotExist:
        return res_err(assemble_err_msg(user_id, "NOT_FOUND", "User"))
    new_attributes_updated = False 
    if request.POST["first_name"]:
        user.first_name = request.POST["first_name"]
        new_attributes_updated = True
    if request.POST["last_name"]:
        user.last_name = request.POST["last_name"]
        new_attributes_updated = True
    if request.POST["email_address"]:
        user.email_address = request.POST["email_address"]
        new_attributes_updated = True
    if request.POST["zipcode"]:
        user.zipcode = request.POST["zipcode"]
        new_attributes_updated = True
    if request.POST["password"]:
        user.password = request.POST["password"]
        new_attributes_updated = True 
    if not new_attributes_updated:
        return res_success("No field is updated.")
    else:
        return res_success("User with user_id" + user_id + " is successfully updated.")
    



def delete_user(request, user_id):
    if request.method != "GET":
        return res_err(assemble_err_msg(-1, "WROUNG_REQUEST_METHOD", "GET"))
    try:
        user = models.User.objects.get(pk=user_id)
    except models.User.DoesNotExist:
        return res_err(assemble_err_msg(user_id, "NOT_FOUND", "User"))
    user.delete()
    return res_success("User with user_id " + user_id + " is successfully deleted.")




def create_pet(request):
    if request.method != 'POST':
        return res_err(assemble_err_msg(-1, "WROUNG_REQUEST_METHOD", "POST"))
    new_pet = models.Pet(
        name = request.POST['name'], 
        pet_type = request.POST['pet_type'], 
        description = request.POST['description'],
        price = request.POST['price'],
        date_joined = datetime.datetime.now(), location=request.POST['location']
    )
    try:
        new_pet.save()
    except db.Error:
        return res_err(str(db.Error))
    return res_success(new_pet.pk)




def get_pet_by_id(request, pet_id):
    if request.method != 'GET':
        return res_err(assemble_err_msg(-1, "WROUNG_REQUEST_METHOD", "GET"))
    try:
        pet = models.Pet.objects.get(pk=pet_id)
    except models.Pet.DoesNotExist:
        return res_err(assemble_err_msg(pet_id, "NOT_FOUND", "Pet"))
    return res_success({
        'name': pet.name,
        'pet_type': pet.pet_type,
        'description': pet.description,
        'price': pet.price,
        'date_joined': pet.date_joined,
    })




def update_pet(request, pet_id):
    if request.method != 'POST':
        return res_err(assemble_err_msg(-1, "WROUNG_REQUEST_METHOD", "POST"))
    try:
        pet = models.Pet.objects.get(pk=pet_id)
    except models.Pet.DoesNotExist:
        return res_err(assemble_err_msg(pet_id, "NOT_FOUND", "Pet"))
    new_attributes_updated = False 
    if request.POST["name"]:
        pet.name = request.POST["name"]
        new_attributes_updated = True
    if request.POST["pet_type"]:
        pet.pet_type = request.POST["pet_type"]
        new_attributes_updated = True
    if request.POST["description"]:
        pet.description = request.POST["description"]
        new_attributes_updated = True
    if request.POST["price"]:
        pet.price = request.POST["price"]
        new_attributes_updated = True
    if request.POST["date_joined"]:
        pet.date_joined = request.POST["date_joined"]
        new_attributes_updated = True 
    if not new_attributes_updated:
        return res_success("No field is updated.")
    else:
        return res_success("Pet with pet_id" + pet_id + " is successfully updated.")
    



def delete_pet(request, pet_id):
    if request.method != "GET":
        return res_err(assemble_err_msg(-1, "WROUNG_REQUEST_METHOD", "GET"))
    try:
        pet = models.Pet.objects.get(pk=pet_id)
    except models.Pet.DoesNotExist:
        return res_err(assemble_err_msg(pet_id, "NOT_FOUND", "Pet"))
    pet.delete()
    return res_success("Pet with pet_id" + pet_id + " is successfully deleted.")

 




