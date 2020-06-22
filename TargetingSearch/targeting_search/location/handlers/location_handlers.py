import json
from copy import deepcopy
from queue import Queue
from threading import Thread

from django.core import serializers

from algorithms.string_matching import match_strings
from app_config.app_config import FACEBOOK_CONFIG
from location.models import *
from tools.facebook_worker import FacebookLocationsWorker

locations_factory = {
    'country': Country,
    'country_group': CountryGroup,
    'region': Region,
    'geo_market': GeoMarket,
    'electoral_district': ElectoralDistrict
}

CONTINENTS = ['africa', 'asia', 'caribbean', 'central_america', 'europe',
              'north_america', 'oceania', 'south_america', 'worldwide']
FREE_TRADE_AREAS = ['afta', 'mercosur', 'cisfta', 'eea', 'nafta', 'gcc', 'apec']
APP_STORE_REGIONS = ['android_free_store', 'android_paid_store', 'itunes_app_store']
EMERGING_MARKETS = ['emerging_markets']
EURO_AREA = ['euro_area']

COUNTRY_GROUPS_LEGEND = {
    'continent': CONTINENTS,
    'free_trade_areas': FREE_TRADE_AREAS,
    'app_store_regions': APP_STORE_REGIONS,
    'emerging_markets': EMERGING_MARKETS,
    'euro_area': EURO_AREA
}


def serialize_country_groups(raw_results):
    results = []
    for result in raw_results:
        try:
            result['country_codes'] = json.loads(result['country_codes'])
        except Exception as e:
            pass
        results.append(result)
    return results


def extract_data_from_serialized_model(data):
    json_data = []

    if isinstance(data, str):
        data = json.loads(data)

    for entry in data:
        try:
            entry = entry['fields']
        except KeyError:
            pass
        json_data.append(deepcopy(entry))
    return json_data


def get_all_handler():
    countries = list(Country.objects.all().values())

    country_groups = serialize_country_groups(list(CountryGroup.objects.all().values()))

    regions = list(Region.objects.all().values())

    geo_markets = list(GeoMarket.objects.all().values())

    electoral_districts = list(ElectoralDistrict.objects.all().values())

    results = {
        'countries': countries,
        'country_groups': country_groups,
        'regions': regions,
        'geo_markets': geo_markets,
        'electoral_districts': electoral_districts
    }

    return results


def get_countries_handler():
    raw_results = list(Country.objects.all().values())
    return raw_results


def get_country_groups_handler():
    results = serialize_country_groups(list(CountryGroup.objects.all().values()))

    return results


def get_regions_handler():
    raw_results = list(Region.objects.all().values())
    return raw_results


def get_geo_markets_handler():
    raw_results = list(GeoMarket.objects.all().values())
    return raw_results


def get_electoral_districts_handler():
    raw_results = list(ElectoralDistrict.objects.all().values())
    return raw_results


def match_locations_handler(request):
    worker = FacebookLocationsWorker(business_owner_facebook_id=FACEBOOK_CONFIG['business_owner_facebook_id'],
                                     facebook_config=FACEBOOK_CONFIG)

    results = {
        "Type": request['Type'],
        "FormatType": request['FormatType'],
        "Locations": request['Locations'],
        "MatchedLocations": {}
    }

    for source_location in request['Locations']:
        entry = {
            "Matched": True,
            "MatchingLocations": []
        }

        if request['FormatType'] == 'geo_market_code':
            if 'DMA' not in source_location:
                source_location = 'DMA:' + source_location
            match = locations_factory[request['Type']].objects.filter(key=source_location)
            match = json.loads(serializers.serialize('json', match))
            match = extract_data_from_serialized_model(match)
            entry['MatchingLocations'].extend(match)

            if entry['MatchingLocations']:
                entry['Matched'] = True
                results["MatchedLocations"][source_location] = entry
        else:
            if request['Type'] in locations_factory.keys():
                target_locations = locations_factory[request['Type']].objects.all()
                target_locations = json.loads(serializers.serialize('json', target_locations))
                target_locations = extract_data_from_serialized_model(target_locations)
            else:
                target_locations = worker.search(query_string=source_location.lower(),
                                                 location_types=request['Type'])
            for target_location in target_locations:
                try:
                    if match_strings(target_location['name'].lower(), source_location.lower()):
                        entry['MatchingLocations'].append(deepcopy(target_location))
                except KeyError:
                    pass

            if entry['MatchingLocations']:
                entry['Matched'] = True
                results["MatchedLocations"][source_location] = entry

    return results


def search_location_handler(query_string):
    limit = 50
    worker = FacebookLocationsWorker(business_owner_facebook_id=FACEBOOK_CONFIG['business_owner_facebook_id'],
                                     facebook_config=FACEBOOK_CONFIG)
    responses = []
    threads = []
    queue = Queue()
    for location_type in worker.__LOCATION_SEARCH_TYPES__:
        t = Thread(target=lambda q, arg1, arg2, arg3: q.put(worker.search(query_string=arg1,
                                                                          location_types=[arg2],
                                                                          limit=arg3)),
                   args=(queue, query_string, location_type, limit))
        threads.append(t)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    if queue.not_empty:
        responses = [entry
                     for element in queue.queue
                     for entry in element]
    return responses


def update_locations_handler():
    worker = FacebookLocationsWorker(business_owner_facebook_id=FACEBOOK_CONFIG['business_owner_facebook_id'],
                                     facebook_config=FACEBOOK_CONFIG)

    errors = []
    for location_type in locations_factory.keys():
        if location_type != 'country_group':
            locations = worker.search(query_string='', location_types=location_type)

            for location in locations:
                item = locations_factory[location_type]()

                for key, value in location.items():
                    if key != 'id' and hasattr(item, key):
                        setattr(item, key, value)

                try:
                    exists = locations_factory[location_type].objects.filter(name=location['name'])
                    if not exists:
                        item.save()

                except Exception as e:
                    errors.append(
                        'Failed to insert %s into Interests database. Error: %s' % (location, e))

    return errors


def update_country_groups_handler():
    worker = FacebookLocationsWorker(business_owner_facebook_id=FACEBOOK_CONFIG['business_owner_facebook_id'],
                                     facebook_config=FACEBOOK_CONFIG)

    country_groups = worker.search(query_string='', location_types='country_group')
    countries = worker.search(query_string='', location_types='country')

    appended_country_groups = []

    for country_group in country_groups:
        entry = deepcopy(country_group)
        entry['country_codes'] = {}
        for country_code in country_group['country_codes']:
            for country in countries:
                if country['country_code'] == country_code:
                    entry['country_codes'][country_code] = country['name']
                    break
        for region in COUNTRY_GROUPS_LEGEND.keys():
            if entry['key'] in COUNTRY_GROUPS_LEGEND[region]:
                entry['region'] = region
                break

        appended_country_groups.append(deepcopy(entry))

    errors = []
    for location in appended_country_groups:
        item = locations_factory['country_group']()

        for key, value in location.items():
            if key != 'id' and hasattr(item, key):
                setattr(item, key, value)

        try:
            exists = locations_factory['country_group'].objects.filter(name=location['name'])
            if not exists:
                item.save()

        except Exception as e:
            errors.append('Failed to insert %s into Interests database. Error: %s' % (location, e))

    return errors


def get_tree_data():
    pass
