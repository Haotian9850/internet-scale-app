from django.shortcuts import render
import datetime
from django import db
from django.db import IntegrityError
from django.http import JsonResponse
from main import models 
import json

from services.services import get_all_pets

def get_pet_list(request):
    return JsonResponse({
        'ok': True,
        'res': get_all_pets()
    })




