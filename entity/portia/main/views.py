import datetime
from django import db
from django.db import IntegrityError
from django.db.utils import DatabaseError
from main import models 
from datetime import datetime
import json
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from utils.err_msg_assembler import assemble_err_msg
from utils.res_handler import res_err, res_success
from services.authenticator_service import get_new_authenticator
from services.mailer_service import send, assemble_pwd_reset_link

from smtplib import SMTPException



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
        date_joined = datetime.now(), 
        zipcode = request.POST.get('zipcode'), 
        password = make_password(request.POST.get("password"))
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
    if not is_authenticated(
        request.POST.get("authenticator"), 
        request.POST.get("username"), 
        True):
        return res_err("User is not properly registered / authenticated.")
    new_pet = models.Pet(
        name = request.POST.get('name'), 
        pet_type = request.POST.get('pet_type'), 
        description = request.POST.get('description'),
        price = request.POST.get('price'),
        date_posted = datetime.now(),
        user = models.User.objects.get(username=request.POST.get("username"))
    )
    try:
        new_pet.save()
    except DatabaseError as e:
        return res_err("Creating pet transaction failed with error " + str(e.args))
    return res_success(str(new_pet.pk))




def get_all_pets(request):
    all_pets = []
    if request.method != 'GET':
        return res_err(assemble_err_msg(-1, "WRONG_REQUEST_METHOD", "GET"))
    try:
        # make result list
        for pet in models.Pet.objects.all():
            new_pet = {
                'pet_id': pet.id,
                'name': pet.name,
                'pet_type': pet.pet_type,
                'description': pet.description,
                'price': pet.price,
                'date_posted': pet.date_posted
            }
            all_pets.append(new_pet)
    except db.Error:
        return res_err(str(db.Error))
    if len(all_pets) == 0:
        return res_success("Currently, no pet is available in our inventory")
    return res_success(all_pets)




def get_pet_by_id(request):
    if request.method != 'POST':
        return res_err(assemble_err_msg(-1, "WRONG_REQUEST_METHOD", "POST"))
    try:
        pet = models.Pet.objects.get(pk=request.POST["id"])
    except models.Pet.DoesNotExist:
        return res_err(assemble_err_msg(request.POST["id"], "NOT_FOUND", "Pet"))
    return res_success({
        'pet_id': pet.id,
        'name': pet.name,
        'pet_type': pet.pet_type,
        'description': pet.description,
        'price': pet.price,
        'date_posted': pet.date_posted,
        'user': pet.user.username
    })





def get_pets_by_username(request):
    if request.method != "POST":
        return res_err(assemble_err_msg(-1, "WRONG_REQUEST_METHOD", "POST"))
    try:
        user = models.User.objects.get(username=request.POST["username"])
        all_pets = []
        for pet in models.Pet.objects.all():
            if pet.user_id == user.pk:
                all_pets.append({
                    "name": pet.name,
                    "pet_type": pet.pet_type,
                    "description": pet.description,
                    "price": pet.price,
                    "date_posted": pet.date_posted,
                    "uesr_id": pet.user_id
                })
    except db.Error:
        return res_err(str(db.Error))
    if len(all_pets) == 0:
        return res_success("No pets found for current user!")
    return res_success(all_pets)




def update_pet(request, pet_id):
    if request.method != 'POST':
        return res_err(assemble_err_msg(-1, "WRONG_REQUEST_METHOD", "POST"))
    if not is_authenticated(request.POST.get("authenticator"), request.POST.get("username"), False):
        return res_err("User is not properly registered / authenticated.")
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
        return res_success("Pet with pet_id {} is successfully updated.".format(pet_id))
    



def delete_pet(request):
    if request.method != "POST":
        return res_err(assemble_err_msg(-1, "WRONG_REQUEST_METHOD", "POST"))
    if not is_authenticated(request.POST.get("authenticator"), request.POST.get("username"), False):
        return res_err("User is not properly registered / authenticated.")
    try:
        pet = models.Pet.objects.get(pk=request.POST.get("pet_id"))
    except models.Pet.DoesNotExist:
        return res_err(assemble_err_msg(request.POST.get("pet_id"), "NOT_FOUND", "Pet"))
    pet.delete()
    return res_success("Pet with pet_id {} is successfully deleted.".format(request.POST.get("pet_id")))



def log_in(request):
    if request.method != "POST":
        return res_err(
            assemble_err_msg(-1, "WRONG_REQUEST_METHOD", "POST")
        )
    try:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = models.User.objects.get(username=username)
        # TODO: add hashing to password
        token = get_new_authenticator(16)
        create_authenticator(user.pk, token)

        if check_password(password, user.password):
            return res_success(token)
        else:
            return res_err(
                assemble_err_msg(username, "WRONG_PASSWORD", "User")
            )
    except models.User.DoesNotExist:
        return res_err(
            assemble_err_msg(username, "NOT_FOUND", "User")
        )



def log_out(request):
    # delete authenticator
    if request.method != "POST":
        return res_err(
            assemble_err_msg(-1, "WRONG_REQUEST_METHOD", "POST")
        )
    try:    
        authenticator = models.Authenticator.objects.get(authenticator=request.POST.get("authenticator"))
    except models.Authenticator.DoesNotExist:
        return res_err(
            assemble_err_msg(request.POST.get("authenticator"), "NOT_FOUND", "Authenticator")
        )
    authenticator.delete()
    return res_success("Authenticator {} is successfully deleted.".format(request.POST.get("authenticator")))

    

def reset_password(request):
    if request.POST["reset"] == "yes":
        # update user password
        try:
            user_id = models.Authenticator.objects.get(authenticator=request.POST.get("authenticator")).user_id
            user = models.User.objects.get(id=user_id)
            # updated user password
            user.password = make_password(request.POST.get("new_password"))
            try:
                user.save()
            except db.Error as e:
                return res_success(
                    "Error while saving updated password {}".format(str(e))
                )
            # delete temp authenticator
            models.Authenticator.objects.get(authenticator=request.POST.get("authenticator")).delete()
            return res_success(
                "Password for user with ID {} has been successfully reset!".format(user_id)
            )
        except models.Authenticator.DoesNotExist:
            return res_err("Invalid link. Cannot reset password. Please make sure you are following the correct link!")
    else:
        # insert authenticator_temp + send mail
        try:
            authenticator_temp = get_new_authenticator(16)
            try:
                user = models.User.objects.get(username=request.POST.get("username"))
            except models.User.DoesNotExist:
                return res_err("User is not registered in our database!")
            create_authenticator(
                user.id,
                authenticator_temp
            )
            try:
                send(
                    "Password recovery for user {}".format(request.POST.get("username")),
                    "Please follow this link to reset your password on Portia: {}".format(assemble_pwd_reset_link(
                        authenticator_temp, "localhost", 8003, "reset"
                    )),
                    "portia_team@localhost",
                    models.User.objects.get(username=request.POST.get("username")).email_address
                )
                return res_success("Password recovery email for user {} is successfully sent. Please check your email address {}".format(
                    models.User.objects.get(username=request.POST.get("username")).username,
                    models.User.objects.get(username=request.POST.get("username")).email_address
                ))
            except SMTPException as e:
                return res_err(
                    "There is an issue when sending password recovery email: {}".format(e)
                )
        except db.Error:    
            return res_err(str(db.Error))
        



#################### Authenticator entity APIs ####################

def create_authenticator(user_id, token):
    new_authenticator = models.Authenticator(
        authenticator = token,
        user_id = user_id,
        date_created = datetime.now()
    )
    new_authenticator.save()
    """
    try:
        new_authenticator.save()
    except (db.Error, IntegrityError) as e:
        print(str(e.args))
    print("New authenticator for user with ID {} is successfully saved!".format(user_id))
    """



def delete_authenticator(authenticator):
    try:
        authenticator = models.Authenticator.objects.get(authenticator=authenticator)
    except models.Authenticator.DoesNotExist:
        print("Authenticator {} not found.".format(authenticator))
    authenticator.delete()
    print("Authenticator {} is successfully deleted.".format(authenticator))




# a user can only update / delete a pet he created
def is_authenticated(token, username, isCreate):
    authenticator = ""
    try:
        authenticator = models.Authenticator.objects.get(authenticator=token)
    except models.Authenticator.DoesNotExist:
        return False
    if not isCreate:
        try: 
            user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return False 
        return authenticator.user_id == user.id
    return True 


#################### Recommendation entity APIs ####################
def update_recommendations(request):
    if request.method == "POST":
        recommendations = json.loads(request.POST.get("recommendations"))
        log = []
        for pet_id in recommendations:
            recommendation, created = models.Recommendations.objects.get_or_create(pk=pet_id)
            if created:
                recommendation.co_views = "&".join(recommendations[pet_id])
                recommendation.save()
            else:
                new_recommendation = models.Recommendations(pet_id=pet_id, co_views="&".join(recommendations[pet_id]))
                new_recommendation.save()
                log.append("&".join(recommendations[pet_id]))
        return JsonResponse({
            "ok": True,
            "res": "Recommendations successfully updated!",
            "log": log
        })
        
        

def get_recommendations(request):
    if request.method == "POST":
        result = []
        for pet_id in models.Recommendations.objects.get(pk=request.POST.get("pet_id")).co_views.split("&"):
            '''
            pet = models.Pet.objects.get(pk=int(pet_id))
            result.append({
                'pet_id': pet.id,
                'name': pet.name,
                'pet_type': pet.pet_type,
                'description': pet.description,
                'price': pet.price,
                'date_posted': pet.date_posted,
                'user': pet.user.username
            })
            '''
            result.append(pet_id)
        return JsonResponse({
            "ok": True,
            "res": result
        })
