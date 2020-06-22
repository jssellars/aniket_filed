import json

from django.http import HttpResponse
from misc.handlers import GetBudgetValidationCatalogHandler
from misc.handlers import GetMarketingRecommendationsHandler


def GetBudgetValidationCatalog(request, businessOwnerFacebookId, adAccountFacebookId):
    if request.method == 'GET':
        try:
            response = GetBudgetValidationCatalogHandler(businessOwnerFacebookId, adAccountFacebookId)
        except Exception as e:
            response = {
                'message': 'An unknown error has accured. %s. Please try again or contact support.' % str(e),
                'error_usr_message': 'An unknown error has accured. Please try again or contact support.',
                'error_user_title': 'Unknown error'
            }
            return HttpResponse(json.dumps({'results': response}), status=500, content_type='application/json')
    else:
        return HttpResponse(status=400)

    return HttpResponse(json.dumps({'results': response}), status=200, content_type='application/json')


def GetMarketingRecommendations(request, businessOwnerFacebookId, adAccountFacebookId, level):
    if request.method == 'GET':
        try:
            response = GetMarketingRecommendationsHandler(businessOwnerFacebookId, adAccountFacebookId, level)
        except Exception as e:
            response = {
                'message': 'An unknown error has accured. %s. Please try again or contact support.' % str(e),
                'error_usr_message': 'An unknown error has accured. Please try again or contact support.',
                'error_user_title': 'Unknown error'
            }
            return HttpResponse(json.dumps({'results': response}), status=500, content_type='application/json')
    else:
        return HttpResponse(status=400)

    return HttpResponse(json.dumps({'results': response}), status=200, content_type='application/json')
