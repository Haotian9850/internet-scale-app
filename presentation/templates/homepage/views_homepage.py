from django.shortcuts import render
from services.pet_service import get_all_pets
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
