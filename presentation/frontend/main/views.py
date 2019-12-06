from services.pet_service import get_all_pets, search_pets, sort_pets, create_pet_service, get_pets_by_user_service, get_pet_by_id_service
from services.user_service import log_in_service, log_out_service, register_service, password_reset_service, reset_service
from services.redis_service import get_redis_client, insert_cache, look_up_cache, invalidate_cache
from services.logging_service import log_search_entry


from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from main.forms.create_pet_form import CreatePetForm
from main.forms.login_form import LoginForm
from main.forms.register_form import RegisterForm
from main.forms.reset_password_form import ResetPasswordForm
from main.forms.reset_form import ResetForm
from django.core.exceptions import ValidationError
import json



def list_all_pets(request):
    res, status = get_all_pets()
    if request.session.get("authenticated") is None:
        request.session["authenticated"] = False
        request.session["username"] = "visitor"
    if status == 0:
        return render(
            request,
            "homepage.html",
            {
                "errMsg": res,
                "authenticated": request.session.get("authenticated"),
                "username": request.session.get("username")
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



def show_individual_pet_by_id(request, id):
    redis_client = get_redis_client()
    status = -1
    cache_hit, cache_res = look_up_cache(redis_client, id)
    if cache_hit:
        res = json.loads(json.loads(cache_res.decode("utf-8")))
        status = 1
    else:
        if request.session.get("username") != "visitor":
            res, status = get_pet_by_id_service(id, request.session.get("username"))
        else:
            res, status = get_pet_by_id_service(id, "visitor")
        insert_cache(redis_client, id, json.dumps(res))
    if status == 0:
        return render(
            request,
            "pet_details.html",
            {
                "errMsg": "An issue has occurred while rendering this pet details template...",
                "authenticated": request.session.get("authenticated"),
                "username": request.session.get("username")
            }
        )
    return render(
        request, 
        "pet_details.html", 
        {
            "result": res,
            "recommendations": res["recommendations"],
            "authenticated": request.session.get("authenticated"),
            "username": request.session.get("username")   
        }
    )



def search(request):
    if request.method == "POST":
        log_search_entry(request.POST["keyword"])
        if request.POST["keyword"] == "":
            return render(
                request,
                "search.html",
                {
                    "result": [],
                    "keyword": "",
                    "authenticated": request.session.get("authenticated"),
                    "username": request.session.get("username")
                }
            )
        res, status = search_pets(request.POST["keyword"])
        if status == 0:
            return render(
                request,
                "search.html",
                {
                    "errMsg": "An issue has occurred while searching in our database...",
                    "authenticated": request.session.get("authenticated"),
                    "username": request.session.get("username")
                }
            )
        if len(res) == 0:
            return render(
                request,
                "search.html",
                {
                    "result": res,
                    "keyword": request.POST["keyword"],
                    "errMsg": "No matching pets found in our database.",
                    "authenticated": request.session.get("authenticated"),
                    "username": request.session.get("username")
                }
            )
        return render(
            request,
            "search.html",
            {
                "result": res,
                "keyword": request.POST["keyword"],
                "authenticated": request.session.get("authenticated"),
                "username": request.session.get("username")
            }
        )
    return render(
        request, 
        "search.html",
        {
            "errMsg": "Please enter search keyword first.",
            "authenticated": request.session.get("authenticated"),
            "username": request.session.get("username")
        }
    )
        




# need to implement cookie-based session authenticator check
def create_new_pet(request):
    if request.method == "POST":
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
                #request.session["statusMsg"] = "Pet {} is successfully created!".format(request.POST["name"])
                request.session["statusMsg"] = res
                return HttpResponseRedirect("/homepage") 
        return render(
            request,
            "create_pet.html",
            {
                "errMsg": "Invalid Entry: Please check if information is correct and make sure price has two decimal places.",
                "form": CreatePetForm()
            }
        )
    else:
        return render(
            request,
            "create_pet.html",
            {
                "form": CreatePetForm(),
                "authenticated": request.session.get("authenticated"),
                "username": request.session.get("username")
            }
        )






# need to set request.session
def login(request):
    if request.method == "POST" and request.session.get("authenticator") is None:
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
    elif request.session.get("authenticator") is None:
        return render(
            request, 
            "login.html",
            {
                "errMsg": request.session.get("errMsg"),
                "statusMsg": request.session.get("statusMsg"),
                "form": LoginForm()
            })
    elif request.session.get("authenticator") is not None:
        return HttpResponseRedirect("/homepage")




def logout(request):
    # internal, no need to check request.method
    invalidate_cache(get_redis_client())
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
                    })
            if not validate_pwd(request.POST["password"]):
                return render(
                    request,
                    "register.html",
                    {
                        "form": RegisterForm(),
                        "errMsg": "Password must contain one capital letter and one number"
                    })
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
                return render(
                    request,
                    "login.html",
                    {
                        "form": LoginForm(),
                        "statusMsg": request.session.get("statusMsg")
                    }
                )
        else:
            return render(
                request,
                "register.html",
                {
                    "errMsg": "Registration form input not valid",
                    "form": RegisterForm()
                }
            )
    else:
        return render(
            request, 
            "register.html",
            {
                "errMsg": request.session.get("errMsg"),
                "form": RegisterForm()
            })        


def validate_pwd(password):
    if len(password) < 8:
        return False
    containsUppercase = False 
    containsNumber = False
    for token in password:
        if token.isupper():
            containsUppercase = True 
        if token.isdigit():
            containsNumber = True 
    return containsNumber and containsUppercase


def reset_password(request):
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            res, status = password_reset_service(request.POST["username"])
            if status == 0 or status == -1:
                return render(
                    request,
                    "reset_password.html",
                    {
                        "errMsg": res,
                        "form": ResetPasswordForm()
                    }
                )
            return render(
                request,
                "reset_password.html",
                {
                    "statusMsg": res,
                    "form": ResetPasswordForm()
                })
        else:
            return render(
                request,
                "reset_password.html",
                {
                    "form": ResetPasswordForm()
                })
    else:
        return render(
            request,
            "reset_password.html",
            {
                "form": ResetPasswordForm()
            })

    
def reset(request, authenticator=""):
    if request.method == "GET":
        # set temp authenticator
        request.session["authenticator"] = authenticator
        return render(
            request,
            "reset.html",
            {
                "form": ResetForm()
            })
    else:
        form = ResetForm(request.POST)
        if form.is_valid():
            res, status = reset_service(request.session["authenticator"], request.POST["new_password"])
            request.session.__delitem__("authenticator")
            if status == 0 or status == -1:
                return render(
                    request,
                    "reset.html",
                    {
                        "form": ResetForm(),
                        "errMsg": res
                    })
            else:
                '''
                return JsonResponse({
                    "status": "Password succesfully reset!"
                })
                '''
                return HttpResponseRedirect("/homepage")