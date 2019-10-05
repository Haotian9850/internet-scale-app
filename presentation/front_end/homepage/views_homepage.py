from django.shortcuts import render
from services.pet_service import get_all_pets, search_pets, sort_pets
from django.http import JsonResponse

def list_pets(request):
    res, status = get_all_pets()
    if status == 0:
        return JsonResponse({
            'ok': False,
            'res': res
        })
    return JsonResponse({
        'ok': True,
        'res': res
    })


############### design decisions have to be made ###############

def search_pets_by_keyword(request):
    # keyword in request.POST. No need to validate method
    res, status = search_pets(request.POST.get('keyword'))
    if status == 0:
        return JsonResponse({
            'ok': False,
            'res': res
        })
    return JsonResponse({
        'ok': True,
        'res': res
    })



def sort_pets_by_attribute(request):
    # similarly, no need to validate method
    res, status = sort_pets(request.POST.get('sort_by'))
    if status == 0:
        return JsonResponse({
            'ok': False,
            'res': res
        })
    return JsonResponse({
        'ok': True,
        'res': res
    })
