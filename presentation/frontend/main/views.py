from services.pet_service import get_all_pets, search_pets, sort_pets, create_pet_service, get_pets_by_user_service
from services.user_service import log_in_service, log_out_service, register_service
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from main.forms.create_pet_form import CreatePetForm
from main.forms.login_form import LoginForm
from main.forms.register_form import RegisterForm

import json





def list_all_pets(request):
    res, status = get_all_pets()
    if request.session.get("authenticated") == None:
        request.session["authenticatde"] = False
        request.session["username"] = ""
    if request.session.get("showAllPets") == None:
        request.session["showAllPets"] = True
    if status == 0:
        return render(
            request,
            "homepage.html",
            {
                "errMsg": "An issue has occurred when rendering homepage template..."
            }
        )
    # empty database err handling
    if type(res) is str:
        return render(
            request,
            "homepage.html",
            {
                "errMsg": res,
                "authenticated": request.session.get("authenticated"),
                "username": request.session.get("username")
            }
        )
    return render(
        request,
        "homepage.html",
        {
            "all_pets": res,
            "authenticated": request.session.get("authenticated"),
            "username": request.session.get("username")
        }
    )



def list_user_pets(request):
    res, status = get_pets_by_user_service(request.session["username"])
    if status == 0:
        errMsg = "An issue has occurred when rendering homepage template..."
        return render(
            request,
            "homepage.html",
            {
                errMsg : errMsg
            }
        )
    if type(res) is str:
        return render(
            request,
            "homepage.html",
            {
                "all_pets": [],
                "authenticated": request.session.get("authenticated"),
                "username": request.session.get("username")
            }
        )
    return render(
        request,
        "homepage.html",
        {
            "all_pets": res,
            "authenticated": request.session.get("authenticated"),
            "username": request.session.get("username")
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
            'authenticated': request.session['authenticated'],
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



# need to implement cookie-based session authenticator check
def create_new_pet(request):
    # process form input after submission
    if request.method == 'POST':
        if not request.session["authenticator"]:
            return HttpResponseRedirect("/login")
        form = CreatePetForm(request.POST)
        if form.is_valid():
            res, status = create_pet_service(request, request.session["username"], request.session["authenticator"])
            if status == 0:
                return JsonResponse({
                    "ok": False,
                    "errMsg": res
                })
            else:
                return HttpResponseRedirect('/homepage')    # TODO add different redirections for res returned (statusMsg)
    else:
        form = CreatePetForm()
    return render(
        request,
        'create_pet.html',
        {
            'form': form
        }
    )






# need to set request.session
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # log user in
            res, status = log_in_service(request.POST["username"], request.POST["password"])
            if status == 0:
                return JsonResponse({
                    "ok": False,
                    "errMsg": res
                })
            else:
                request.session["username"] = request.POST["username"]
                request.session["authenticator"] = res
                request.session["authenticated"] = True
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




def logout(request):
    # internal, no need to check request.method
    res, status = log_out_service(request.session["authenticator"])
    if status == 0:
        return JsonResponse({
            "ok": False,
            "errMsg": res
        })
    else:
        request.session["authenticated"] = False
        request.session["username"] = ""
        return HttpResponseRedirect("/homepage")    # TODO: add statusMsg to redirect
        
    


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            res, status = register_service(request)
            if status == 0:
                return JsonResponse({
                    "ok": False,
                    "errMsg": res
                })
            else:
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