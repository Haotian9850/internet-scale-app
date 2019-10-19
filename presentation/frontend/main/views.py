from services.pet_service import get_all_pets, search_pets, sort_pets
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from main.forms import SearchForm
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
            "all_pets": res
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
    for pet in res: 
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



def search_pets_by_keyword(request):
    if request.method == 'POST':
        if request.POST['keyword'] == '':
            return render(
                request,
                'search.html',
                {
                    'result': [],
                    'keyword': ""
                }
            )
        res, status = search_pets(request.POST['keyword'])
        if status == 0:
            errMsg = 'An issue has occurred while searching in our database...'
            return render(
                request,
                'search.html',
                {
                    errMsg : errMsg
                }
            )
        return render(
            request, 
            'search.html',
            {
                'result': res,
                'keyword': request.POST['keyword']
            }
        )