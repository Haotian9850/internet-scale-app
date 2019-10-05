from .services.pet_service import get_all_pets, search_pets, sort_pets
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.forms import model_to_dict, ModelForm
import json

def list_pets(request):
    res, status = get_all_pets()
    
    context = {
        'results' : res
    }
    
    return render(request, 'front_end/homepage.html', context)

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