from django.shortcuts import render
import datetime
from django.http import JsonResponse
from django import db
from main import models 
from portia import settings 

# Create your views here.
def create_user(request):
    if request.method != 'POST':
        return _error_response(request, "Wrong request method")
    
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
        return _error_response(request, str(db.Error))
    return _success_response(request, {'user_id': new_user.pk})





