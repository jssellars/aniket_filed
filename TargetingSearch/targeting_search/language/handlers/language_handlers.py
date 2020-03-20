from copy import deepcopy

from algorithms.string_matching import match_strings
from app_config.app_config import FACEBOOK_CONFIG
from language.models import LanguageModel
from tools.facebook_worker import FacebookLanguagesWorker


def get_all_handler():
    raw_results = LanguageModel.objects.all()

    results = [{'name': result.name, 'key': result.key}
               for result in raw_results]
    results = [result for index, result in enumerate(results) if result not in results[index + 1:]]

    return results


def update_languages_handler():
    worker = FacebookLanguagesWorker(business_owner_facebook_id=FACEBOOK_CONFIG['business_owner_facebook_id'],
                                     facebook_config=FACEBOOK_CONFIG)

    results = worker.get_all_values()

    errors = []
    for result in results:
        item = LanguageModel()
        item.name = result['name']
        item.key = result['key']

        try:
            exists = LanguageModel.objects.filter(name=result['name'])
            if not exists:
                item.save()
        except Exception as e:
            errors.append(
                'Failed to insert %s into Language database. Error: %s' % (result, e))

    return errors


def match_languages_handler(request):
    target_languages = get_all_handler()

    results = {
        "Languages": request['Languages'],
        "MatchedLanguages": {}
    }

    for source_language in request['Languages']:

        entry = {
            "Matched": False,
            "MatchingLanguages": []
        }

        for target_language in target_languages:
            if match_strings(target_language['name'].lower(), source_language.lower()):
                entry['MatchingLanguages'].append(deepcopy(target_language))

        if entry['MatchingLanguages']:
            entry['Matched'] = True

        results["MatchedLanguages"][source_language] = entry

    return results
