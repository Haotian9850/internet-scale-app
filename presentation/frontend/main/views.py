from services.pet_service import get_all_pets, search_pets, sort_pets
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.forms import model_to_dict, ModelForm
import json

def list_pets(request):
    res, status = get_all_pets()
    
    if status == 0:
        errMsg = "An issue has occurred when rendering homepage template..."
        return render(
            request,
            "homepage.html",
            {
                errMsg : errMsg
            }
        )
    return render(
        request,
        "homepage.html",
        {
            "all_pets": res[0]
        }
    )

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
    context = {
        'result': result
    }
    return render(request, 'pet_details.html', context)