from django.shortcuts import render
import datetime
from django import db
from django.db import IntegrityError
from django.http import JsonResponse
from main import models 
import json

from services.pet_service import get_all_pets

def get_pet_list(request):
    if request.method != 'GET':
        return JsonResponse({
            'ok': False,
            'res': 'Wrong request method. Request method must be GET.'
        })
    res, status = get_all_pets()
    if status == 0:
        return JsonResponse({
            'ok': False,
            'res': res
        })
    return JsonResponse({
        'ok': True,
        'res': get_all_pets()
    })


def search_pets(request):
    #search in pet name, description and pet_type
    if request.method != 'POST':
        return JsonResponse({
            'ok': False,
            'res': 'Wrong request method. Request method must be POST.'
        })
    res, status = get_all_pets()
    if status == 0:
        return JsonResponse({
            'ok': False,
            'res': res
        })
    result = []
    keyword = request.POST.get('keyword')
    for pet in json.loads(str(res[0])):
        if pet['name'].lower().find(keyword.lower()) != -1 or pet['description'].lower().find(keyword.lower()) != -1 or pet['pet_type'].lower().find(keyword.lower()) != -1:
            result.append(pet)
    return JsonResponse({
        'ok': True,
        'res': result
    })
    


