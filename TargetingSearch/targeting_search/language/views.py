import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from language.handlers.language_handlers import *


def get_all(request):
    if request.method == 'GET':
        results = get_all_handler()
    else:
        return HttpResponse(status=400)

    return HttpResponse(json.dumps({'results': results}), status=200, content_type='application/json')


def update_languages(request):
    if request.method == 'PUT':
        errors = update_languages_handler()
    else:
        return HttpResponse(status=400)

    if not errors:
        return HttpResponse(status=200)
    else:
        return HttpResponse(json.dumps({'results': errors}), status=200, content_type='application/json')


@csrf_exempt
def match_languages(request):
    if request.method == 'POST':
        results = match_languages_handler(json.loads(request.body.decode('utf-8')))
    else:
        return HttpResponse(status=400)

    return HttpResponse(json.dumps({'results': results}), status=200, content_type='application/json')
