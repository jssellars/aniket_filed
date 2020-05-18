# TODO: ADD STATUS CODES TO EVERY RESPONSE
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from staticpreview.request_handlers import *


def get_all(request):
    response = get_all_handler(request)
    response = json.dumps({'response': response})
    return HttpResponse(response)


def get_preview_by_type(request, preview_type):
    response = get_preview_by_type_handler(preview_type)
    response = json.dumps({'response': response})
    return HttpResponse(response)


@csrf_exempt
def generate_static_preview(request):
    if request.method == 'POST':
        request = json.loads(request.body.decode())
    else:
        return HttpResponse(status=400)

    generate_static_preview_handler(request)

    return HttpResponse(status=200)


@csrf_exempt
def generate_preview_by_type(request):
    if request.method == 'POST':
        request = json.loads(request.body.decode())
    else:
        return HttpResponse(status=400)

    response = generate_preview_by_type_handler(request)
    response = json.dumps({'response': response})

    return HttpResponse(response)
