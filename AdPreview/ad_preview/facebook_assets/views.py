import json

from django.http import HttpResponse
from facebook_assets.FacebookAssets import FacebookAssets


def GetAdVideos(request, business_owner_facebook_id, ad_account_id):
    if not request.method == 'GET':
        return HttpResponse(status=400)

    response = FacebookAssets(business_owner_facebook_id).GetAdVideosMinimal(ad_account_id)

    return HttpResponse(json.dumps({'response': response}), status=200, content_type='application/json')


def GetAdImages(request, business_owner_facebook_id, ad_account_id):
    if not request.method == 'GET':
        return HttpResponse(status=400)

    response = FacebookAssets(business_owner_facebook_id).GetAdImagesMinimal(ad_account_id)

    return HttpResponse(json.dumps({'response': response}), status=200, content_type='application/json')


def GetPagePostsMinimal(request, business_owner_facebook_id, page_facebook_id):
    if not request.method == 'GET':
        return HttpResponse(status=400)

    response = FacebookAssets(business_owner_facebook_id).GetPagePostsMinimal(page_facebook_id)

    return HttpResponse(json.dumps({'response': response}), status=200, content_type='application/json')
