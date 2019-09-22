from django.shortcuts import render
import datetime
from django.http import JsonResponse
from django import db
from main import models 
#from portia import settings 

# Create your views here.
def create_user(request):
    if request.method != 'POST':
        return throw_err(request, "Wrong request method")
    
    new_user = models.Profile(
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
        return throw_err(request, str(db.Error))
    return success_res(request, {'user_id': new_user.pk})


def get_user_by_id(request, user_id):
    if request.method != 'GET':
        return throw_err(request, "Wrong request method")

    try:
        user = models.User.objects.get(pk=user_id)
    except models.User.DoesNotExist:
        return throw_err(request, "User not found in databases")

    return success_res(request, {
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


def throw_err(req, err_msg):
    return JsonResponse({
        'ok': False,
        'error': err_msg
    })

def success_res(req, res):
    if res:
        return JsonResponse({
            'ok': True,
            'res': res
        })
    else:
        return JsonResponse({
            'ok': True
        })