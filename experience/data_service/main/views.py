from django.shortcuts import render
import datetime
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from services.pet_service import get_all_pets_service, create_pet_service, get_pets_by_user_service, get_pet_by_id_service
from services.user_service import log_in_service, log_out_service, create_user_service, password_reset_service, reset_service

def get_pet_list(request):
    if request.method != 'GET':
        return JsonResponse({
            'ok': False,
            'res': 'Wrong request method. Request method must be GET.'
        })
    res, status = get_all_pets_service()
    if status == 0:
        return JsonResponse({
            'ok': False,
            'res': res
        })
    return JsonResponse({
        'ok': True,
        'res': res
    })


def get_pet_by_id(request):
    # internal, no need to check request.method
    res, status = get_pet_by_id_service(request)
    if status == 0:
        return JsonResponse({
            "ok": False,
            "res": res
        })
    return JsonResponse({
            "ok": True,
            "res": res
    })



def get_pets_by_user(request):
    # internal, no need to check request.method
    res, status = get_pets_by_user_service(request)
    if status == 0:
        return JsonResponse({
            "ok": False,
            "res": res
        })
    return JsonResponse({
            "ok": True,
            "res": res
    })




def create_pet(request):
    if request.method != 'POST':
        return JsonResponse({
            'ok': False,
            'res': 'Wrong request method. Request method must be {}'.format("POST")
        })
    res, status = create_pet_service(request)
    if status == 0:
        return JsonResponse({
            'ok': False,
            'res': res
        })
    elif status == -1:
        return JsonResponse({
            'ok': False,
            'res': res  # err msg str
        })
    return JsonResponse({
        'ok': True,
        'res': res
    })    



def search_pets(request):
    # search in pet name, description and pet_type
    if request.method != 'POST':
        return JsonResponse({
            'ok': False,
            'res': 'Wrong request method. Request method must be POST.'
        })
    res, status = get_all_pets_service()
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
    res, status = get_all_pets_service()
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


@csrf_exempt
def log_in(request):
    if request.method != 'POST':
        return JsonResponse({
            'ok': False,
            'res': 'Wrong request method. Request method must be POST.'
        })
    # TODO: add hash here (?)
    res, status = log_in_service(request.POST.get('username'), request.POST.get('password'))
    if status == 0:
        return JsonResponse({
            'ok': False,
            'res': res
        })
    elif status == -1:
        return JsonResponse({
            'ok': False,
            'res': res  # err msg str
        })
    return JsonResponse({
        'ok': True,
        'res': res
    }) 


def log_out(request):
    if request.method != 'POST':
        return JsonResponse({
            'ok': False,
            'res': 'Wrong request method. Request method must be POST.'
        })
    res, status = log_out_service(request.POST.get('authenticator'))
    if status == 0:
        return JsonResponse({
            'ok': False,
            'res': res
        })
    return JsonResponse({
        'ok': True,
        'res': res
    })


def create_user(request):
    if request.method != "POST":
        return JsonResponse({
            "ok": False,
            "res": "Wrong request method. Request method must be {}".format("POST")
        })
    res, status = create_user_service(request)
    if status == 0 or status == -1:
        return JsonResponse({
            "ok": False,
            "res": res
        })
    return JsonResponse({
        "ok": True,
        "res": res
    })
    
    

def reset_password(request):
    if request.method == "POST":
        res, status = password_reset_service(request.POST["username"])
    if status == 0 or status == -1:
        return JsonResponse({
            "ok": False,
            "res": res
        })
    return JsonResponse({
        "ok": True,
        "res": res
    })




def reset(request):
    if request.method == "POST":
        res, status = reset_service(request.POST["authenticator"], request.POST["new_password"])
    if status == 0 or status == -1:
        return JsonResponse({
            "ok": False,
            "res": res
        })
    return JsonResponse({
        "ok": True,
        "res": res
    })    
    


