from services.pet_service import get_all_pets, search_pets, sort_pets, create_pet_service, get_pets_by_user_service
from services.user_service import log_in_service, log_out_service, register_service, password_reset_service
from services.password_service import validate_pwd
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from main.forms.create_pet_form import CreatePetForm
from main.forms.login_form import LoginForm
from main.forms.register_form import RegisterForm
from main.forms.reset_password_form import ResetPasswordForm
from django.core.exceptions import ValidationError
import json



def list_all_pets(request):
    res, status = get_all_pets()
    if request.session.get("authenticated") == None:
        request.session["authenticated"] = False
        request.session["username"] = ""
    if status == 0:
        return render(
            request,
            "homepage.html",
            {
                "errMsg": res
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
            "statusMsg": request.session.get("statusMsg"),
            "all_pets": res,
            "authenticated": request.session.get("authenticated"),
            "username": request.session.get("username")
        }
    )



def list_user_pets(request):
    if request.session.get("username") is None:
        # session timed out
        return HttpResponseRedirect("/homepage")
    if request.session.get("authenticator") is None:
        # not authenticated
        return HttpResponseRedirect("/login")
    res, status = get_pets_by_user_service(request.session["username"])
    if status == 0:
        return render(
            request,
            "homepage.html",
            {
                "errMsg" : "An issue has occurred when rendering homepage template..."
            }
        )
    if type(res) is str:
        return render(
            request,
            "homepage.html",
            {
                "all_pets": [],
                "errMsg": "No pet found for current user",
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
        if len(res) == 0:
            return render(
                request,
                "search.html",
                {
                    "result": res,
                    "keyword": request.POST["keyword"],
                    "errMsg": "No pets found in our database."
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
    if request.method == 'POST':
        if not request.session.get("authenticator"):
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
                request.session["statusMsg"] = "Pet {} is successfully created!".format(request.POST["name"])
                return HttpResponseRedirect("/homepage") 
        form = CreatePetForm()
        return render(
            request,
            "create_pet.html",
            {
                "errMsg": "Invalid Entry: Please check if information is correct and make sure price has two decimal places.",
                "form": form
            }
        )
    else:
        form = CreatePetForm()
    return render(
        request,
        "create_pet.html",
        {
            "form": form,
            "authenticated": request.session.get("authenticated"),
            "username": request.session.get("username")
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
            elif status == -1:
                request.session["errMsg"] = res
                if request.session.get("statusMsg") is not None:
                    request.session.__delitem__("statusMsg")
                return HttpResponseRedirect("/login")
            else:
                request.session["username"] = request.POST["username"]
                request.session["authenticator"] = res
                request.session["authenticated"] = True
                request.session["statusMsg"] = "Successfully logged in for user {}".format(request.session["username"])
                if request.session.get("errMsg") is not None:
                    request.session.__delitem__("errMsg")
                
            return HttpResponseRedirect("/homepage")
    else:
        form = LoginForm()
    return render(
        request, 
        "login.html",
        {
            "errMsg": request.session.get("errMsg"),
            "statusMsg": request.session.get("statusMsg"),
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
        #request.session["statusMsg"] = "Successfully logged out for user {}".format(request.session["username"])
        #request.session["authenticated"] = False
        #request.session["username"] = ""
        request.session.flush()
        return HttpResponseRedirect("/homepage")

        
    



def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            if request.POST["password"] != request.POST["confirm_password"]:
                return render(
                    request,
                    "register.html",
                    {
                        "form": RegisterForm(),
                        "errMsg": "Password does not match"
                    }
                )
            if not validate_pwd(request.POST["password"]):
                return render(
                    request,
                    "register.html",
                    {
                        "form": RegisterForm(),
                        "errMsg": "Password must contain one capital letter and one number"
                    }
                )
            res, status = register_service(request)
            if status == 0:
                return JsonResponse({
                    "ok": False,
                    "errMsg": res
                })
            elif status == -1:
                request.session["errMsg"] = res
                if request.session.get("statusMsg") is not None:
                    request.session.__delitem__("statusMsg") 
                return HttpResponseRedirect("/register")
            else:
                request.session["statusMsg"] = res 
                if request.session.get("errMsg") is not None:
                    request.session.__delitem__("errMsg") 
                return HttpResponseRedirect("/login")
    else:
        form = RegisterForm()
    return render(
        request, 
        "register.html",
        {
            "errMsg": request.session.get("errMsg"),
            "form": form
        }
    )        


def reset_password(request):
    if request.method == "POST":
        res, status = password_reset_service(request.POST["username"], False)
        if status == 0 or status == -1:
            return JsonResponse({
                "ok": False,
                "res": res
            })
        return render(
            request,
            "reset_password.html",
            {
                "statusMsg": res,
                "form": ResetPasswordForm()
            }
        )
    else:
        return render(
            request,
            "reset_password.html",
            {
                "form": ResetPasswordForm()
            }
        )