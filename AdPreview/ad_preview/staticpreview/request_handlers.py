from adpreview.config import FacebookConfig
from tools.ad_previews import GenerateAdPreview


def GenerateAdPreviewHandler(request=None):
    assert request is not None

    # Extract data from request
    if 'business_owner_facebook_id' not in request.keys():
        businessOwnerFacebookId = FacebookConfig.user_id
    else:
        businessOwnerFacebookId = request['business_owner_facebook_id']

    if 'ad_account_id' in request.keys():
        adAccountFacebookId = request['ad_account_id']
    else:
        raise ValueError("Invalid request. Ad Account Facebook ID missing.")

    if 'page_id' in request.keys():
        pageFacebookId = request['page_id']
    else:
        raise ValueError("Invalid request. Page Facebook ID missing.")

    if 'instagram_id' in request.keys():
        instagramFacebookId = request['instagram_id']
    else:
        instagramFacebookId = None

    adTemplate = request['advert']

    adPreviewGenerator = GenerateAdPreview(businessOwnerFacebookId)
    adPreview = adPreviewGenerator.GeneratePreview(adAccountFacebookId, adTemplate, pageFacebookId,
                                                   instagramFacebookId)

    return adPreview
