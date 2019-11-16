from django.http import JsonResponse

def res_err(err_msg):
    return JsonResponse({
        'ok': False,
        'res': err_msg
    })

def res_success(res):
    if res:
        return JsonResponse({
            'ok': True,
            'res': res
        })
    else:
        return JsonResponse({
            'ok': True
        })