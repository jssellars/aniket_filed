from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from interest.handlers.audience_details_handler import EstimateAudienceSize
from interest.handlers.interest_handlers import *
from interest.handlers.interests_tree_handler import get_interests_tree_handler


def get_all(request):
    if request.method == 'GET':
        response = get_all_handler()
    else:
        return HttpResponse(status=400)

    return HttpResponse(json.dumps({'results': response}), status=200, content_type='application/json')


def get_interest_by_key(request, interest_key):
    if request.method == 'GET':
        response = get_interest_by_key_handler(interest_key)
    else:
        return HttpResponse(status=400)

    return HttpResponse(json.dumps({'results': response}), status=200, content_type='application/json')


@csrf_exempt
def get_interests_tree(request):
    if request.method == 'GET':
        response = get_interests_tree_handler()
    else:
        return HttpResponse(status=400)

    return HttpResponse(json.dumps({'results': response}), status=200, content_type='application/json')


@csrf_exempt
def search_interest(request, query):
    if request.method == 'GET':
        response = search_interest_handler(query)
    else:
        return HttpResponse(status=400)

    return HttpResponse(json.dumps({'results': response}), status=200, content_type='application/json')


@csrf_exempt
def suggest_interests(request, interests):
    if request.method == 'GET':
        response = suggest_interests_handlers(interests)
    else:
        return HttpResponse(status=400)

    return HttpResponse(json.dumps({'results': response}), status=200, content_type='application/json')


@csrf_exempt
def update_interests(request):
    if request.method == 'POST':
        response = update_interests_handler()
    else:
        return HttpResponse(status=400)

    return HttpResponse(json.dumps({'results': response}), status=200, content_type='application/json')


@csrf_exempt
def match_interests(request):
    if request.method == 'POST':
        response = match_interests_handler(json.loads(request.body.decode('utf-8')))
    else:
        return HttpResponse(status=400)

    return HttpResponse(json.dumps({'results': response}), status=200, content_type='application/json')


@csrf_exempt
def get_estimated_audience_size(request):
    if request.method == "POST":
        response = EstimateAudienceSize(json.loads(request.body.decode('utf-8')))
    else:
        return HttpResponse(status=400)

    if response and 'message' not in response.keys():
        return HttpResponse(json.dumps({'results': response}), status=200, content_type='application/json')
    elif response and 'message' in response.keys():
        return HttpResponse(json.dumps({'results': response}), status=500, content_type='application/json')
