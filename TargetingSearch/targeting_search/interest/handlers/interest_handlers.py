import json
from copy import deepcopy

from algorithms.string_matching import match_strings
from app_config.app_config import FACEBOOK_CONFIG
from django.core import serializers
from interest.handlers.interests_search import search_interests, suggest_interests
from interest.models import *
from tools.facebook_worker import FacebookInterestsWorker


def get_all_handler():
    raw_results = json.loads(serializers.serialize('json', RawInterest.objects.all()))
    results = []
    for result in raw_results:
        result = result['fields']
        try:
            result['path'] = json.loads(result['path'])
        except KeyError:
            pass
        except TypeError:
            pass
        results.append(result)
    return results


def get_interest_by_key_handler(interest_key):
    results = json.loads(serializers.serialize('json', RawInterest.objects.filter(key=interest_key)))[0]['fields']
    try:
        results['path'] = json.loads(results['path'])
    except KeyError:
        pass
    except TypeError:
        pass

    return results


def search_interest_handler(search_input):
    results = search_interests(search_input)

    return results


def suggest_interests_handlers(interests):
    suggested_interests = suggest_interests(interests=interests)

    return suggested_interests


def update_interests_handler():
    worker = FacebookInterestsWorker(business_owner_facebook_id=FACEBOOK_CONFIG['business_owner_facebook_id'],
                                     facebook_config=FACEBOOK_CONFIG)
    results = worker.browse_interests()

    errors = []
    for result in results:
        item = RawInterest()

        for key, value in result.items():
            if key == 'path':
                setattr(item, key, json.dumps(value))
            elif key == 'id':
                setattr(item, 'key', result['id'])
            elif key != 'id':
                if hasattr(item, key):
                    setattr(item, key, value)

        try:
            exists = RawInterest.objects.filter(name=result['name'])
            if not exists:
                item.save()

        except Exception as e:
            errors.append(
                'Failed to insert %s into Interests database. Error: %s' % (result, e))

    return errors


def match_interests_handler(request):
    raw_basic_target_interests = json.loads(serializers.serialize('json', RawInterest.objects.all()))
    basic_target_interests = []
    for interest in raw_basic_target_interests:
        try:
            interest = interest['fields']
            interest['path'] = json.loads(interest['path'])
        except KeyError:
            pass
        except TypeError:
            pass
        basic_target_interests.append(interest)

    results = {
        "Interests": request['interests'],
        "MatchedInterests": {}
    }

    for source_interest in request['interests']:
        search_results = search_interests(source_interest)

        target_interests = basic_target_interests
        target_interests.extend(search_results)

        entry = {
            "Matched": False,
            "MatchedInterests": []
        }

        for target_interest in target_interests:
            try:
                if match_strings(target_interest['name'].lower(), source_interest.lower()):
                    entry['MatchedInterests'].append(deepcopy(target_interest))
            except KeyError:
                pass

        if entry['MatchedInterests']:
            entry['Matched'] = True

        results["MatchedInterests"][source_interest] = entry

    return results
