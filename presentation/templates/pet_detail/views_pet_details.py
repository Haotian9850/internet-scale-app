from django.shortcuts import render
from services.pet_service import get_all_pets
from django.http import JsonResponse
import json

def show_individual_pet_by_name(request, name):
    res, status = get_all_pets()
    if status == 0:
        return JsonResponse({
            'ok': False,
            'res': res
        })
    result = {}
    for pet in res[0]: 
        if pet['name'] == name:
            result = pet
    if len(result) == 0:
        return JsonResponse({
            'ok': False,
            'res': 'No pet found for given name'
        })
    return JsonResponse({
        'ok': True,
        'res': result
    })    