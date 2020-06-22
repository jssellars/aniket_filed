from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from location.handlers.location_handlers import *


def get_all(request):
    if request.method == 'GET':
        results = get_all_handler()
    else:
        return HttpResponse(status=400)

    return HttpResponse(content=json.dumps({'results': results}), status=200, content_type='application/json')


def get_countries(request):
    if request.method == 'GET':
        results = get_countries_handler()
    else:
        return HttpResponse(status=400)

    return HttpResponse(content=json.dumps({'results': results}), status=200,
                        content_type='application/json')


def get_country_groups(request):
    if request.method == 'GET':
        results = get_country_groups_handler()
    else:
        return HttpResponse(status=400)
    return HttpResponse(content=json.dumps({'results': results}), status=200,
                        content_type='application/json')


def get_regions(request):
    if request.method == 'GET':
        results = get_regions_handler()
    else:
        return HttpResponse(status=400)

    return HttpResponse(content=json.dumps({'results': results}), status=200, content_type='application/json')


def get_geo_markets(request):
    if request.method == 'GET':
        results = get_geo_markets_handler()
    else:
        return HttpResponse(status=400)

    return HttpResponse(content=json.dumps({'results': results}), status=200, content_type='application/json')


def get_electoral_districts(request):
    if request.method == 'GET':
        results = get_electoral_districts_handler()
    else:
        return HttpResponse(status=400)

    return HttpResponse(content=json.dumps({'results': results}), status=200, content_type='application/json')


@csrf_exempt
def search_location(request, query_string):
    if request.method == 'GET':
        results = search_location_handler(query_string)
    else:
        return HttpResponse(status=400)

    return HttpResponse(content=json.dumps({'results': results}), status=200, content_type='application/json')


@csrf_exempt
def update_locations(request):
    if request.method == 'PUT':
        errors = update_locations_handler()
    else:
        return HttpResponse(status=400)

    return HttpResponse(content=json.dumps({'results': errors}), status=200, content_type='application/json')


@csrf_exempt
def update_country_groups(request):
    if request.method == 'PUT':
        errors = update_country_groups_handler()
    else:
        return HttpResponse(status=400)

    return HttpResponse(content=json.dumps({'results': errors}), status=200, content_type='application/json')


@csrf_exempt
def match_locations(request):
    if request.method == 'POST':
        results = match_locations_handler(json.loads(request.body.decode()))
    else:
        return HttpResponse(status=400)

    return HttpResponse(content=json.dumps({'results': results}), status=200, content_type='application/json')
