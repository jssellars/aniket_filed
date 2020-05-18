from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from interest.handlers.audience_details_handler import estimate_audiece_size
from interest.handlers.interest_handlers import *
from interest.handlers.interests_tree_handler import get_interests_tree_handler


def get_all(request):
    if request.method == 'GET':
        results = get_all_handler()
    else:
        return HttpResponse(status=400)

    return HttpResponse(json.dumps({'results': results}), status=200, content_type='application/json')


def get_interest_by_key(request, interest_key):
    if request.method == 'GET':
        results = get_interest_by_key_handler(interest_key)
    else:
        return HttpResponse(status=400)

    return HttpResponse(json.dumps({'results': results}), status=200, content_type='application/json')


@csrf_exempt
def get_interests_tree(request):
    if request.method == 'GET':
        results = get_interests_tree_handler()
    else:
        return HttpResponse(status=400)

    return HttpResponse(json.dumps({'results': results}), status=200, content_type='application/json')


@csrf_exempt
def search_interest(request, query):
    if request.method == 'GET':
        results = search_interest_handler(query)
    else:
        return HttpResponse(status=400)

    return HttpResponse(json.dumps({'results': results}), status=200, content_type='application/json')


@csrf_exempt
def suggest_interests(request, interests):
    if request.method == 'GET':
        results = suggest_interests_handlers(interests)
    else:
        return HttpResponse(status=400)

    return HttpResponse(json.dumps({'results': results}), status=200, content_type='application/json')


@csrf_exempt
def update_interests(request):
    if request.method == 'POST':
        results = update_interests_handler()
    else:
        return HttpResponse(status=400)

    return HttpResponse(json.dumps({'results': results}), status=200, content_type='application/json')


@csrf_exempt
def match_interests(request):
    if request.method == 'POST':
        results = match_interests_handler(json.loads(request.body.decode('utf-8')))
    else:
        return HttpResponse(status=400)

    return HttpResponse(json.dumps({'results': results}), status=200, content_type='application/json')


@csrf_exempt
def get_estimated_audience_size(request):
    if request.method == "POST":
        results = estimate_audiece_size(json.loads(request.body.decode('utf-8')))
    else:
        return HttpResponse(status=400)

    return HttpResponse(json.dumps({'results': results}), status=200, content_type='application/json')
