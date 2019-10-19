from django.shortcuts import render
import datetime
from django.db import IntegrityError
from django.http import JsonResponse
import json

from services.pet_service import get_all_pets
from services.user_service import log_in, log_out

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


# def create_pet(request):




def search_pets(request):
    # search in pet name, description and pet_type
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
    
    for pet in res:
        if pet['name'].lower().find(keyword.lower()) != -1 or pet['pet_type'].lower().find(keyword.lower()) != -1:
            result.append(pet)
    
    return JsonResponse({
        'ok': True,
        'res': result
    })


def sort_pets(request):
    # sort pet by specified criteria
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
    sort_by = request.POST.get('sort_by')
    if sort_by != "price" and sort_by != "date_posted" and sort_by != "name":
        return JsonResponse({
            'ok': False,
            'res': 'Malformed search criteria'
        })
    sorted(res, key = lambda i : i[sort_by], reverse = True)
    return JsonResponse({
        'ok': True,
        'res': res
    })



def log_in_user(request):
    if request.method != 'POST':
        return JsonResponse({
            'ok': False,
            'res': 'Wrong request method. Request method must be POST.'
        })
    # TODO: add hash here (?)
    res, status = log_in(request.POST.get('username'), request.POST.get('password'))
    if status == 0:
        return JsonResponse({
            'ok': False,
            'res': res
        })
    # return authenticator generated by entity layer
    return JsonResponse({
        'ok': True,
        'res': res
    })




def log_out_user(request):
    if request.method != 'POST':
        return JsonResponse({
            'ok': False,
            'res': 'Wrong request method. Request method must be POST.'
        })
    res, status = log_out(request.POST.get('authenticator'))
    if status == 0:
        return JsonResponse({
            'ok': False,
            'res': res
        })
    return JsonResponse({
        'ok': True,
        'res': res
    })

    



    
    


