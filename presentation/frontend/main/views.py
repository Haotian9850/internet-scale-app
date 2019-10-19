from services.pet_service import get_all_pets, search_pets, sort_pets
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from main.forms.create_pet_form import CreatePetForm
from main.forms.login_form import LoginForm
from main.forms.register_form import RegisterForm

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
    return render(
        request, 
        'pet_details.html', 
        {
            'result': result        
        }
    )






def search(request):
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




def create_new_pet(request):
    # process form input after submission
    if request.method == 'POST':
        form = CreatePetForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/homepage')
    else:
        form = CreatePetForm()
    return render(
        request,
        'create_pet.html',
        {
            'form': form
        }
    )




def login(request):
    if request.method == "POST":
        form = LoginForm()
        if form.is_valid():
            return HttpResponseRedirect("/homepage")
    else:
        form = LoginForm()
    return render(
        request, 
        "login.html",
        {
            "form": form
        }
    )


def register(request):
    if request.method == "POST":
        form = RegisterForm()
        if form.is_valid():
            return HttpResponseRedirect("/login")
    else:
        form = RegisterForm()
    return render(
        request, 
        "register.html",
        {
            "form": form
        }
    )        