from staticpreview.models import StaticAdPreview
from tools.ad_previews import GenerateAdPreview


def _preview_generator(request):
    # Extract data from request
    ad_account_id = request['ad_account_id']
    page_id = request['page_id']
    params = request['params']

    preview_generator = GenerateAdPreview()

    try:
        ad_preview = preview_generator.generate_preview(ad_account_id, page_id, params)
    except Exception as e:
        return e

    return ad_preview


def generate_static_preview_handler(request=None):
    assert request is not None

    ad_preview = _preview_generator(request)

    if ad_preview and not StaticAdPreview.objects.filter(facebook_preview_type=request['params']['ad_format']):
        preview = StaticAdPreview()
        preview.preview = ad_preview
        preview.facebook_preview_type = request['params']['ad_format']
        preview.save()


def get_all_handler(request=None):
    assert request is not None

    raw_previews = StaticAdPreview.objects.all()
    previews = [[raw_preview.facebook_preview_type, raw_preview.preview] for raw_preview in raw_previews]

    return previews


def get_preview_by_type_handler(preview_type=None):
    assert preview_type is not None

    raw_preview = StaticAdPreview.objects.filter(facebook_preview_type=preview_type)

    if raw_preview:
        return raw_preview[0].preview
    else:
        return 'Could not find any preview of type: %s' % preview_type


def generate_preview_by_type_handler(request=None):
    assert request is not None

    return _preview_generator(request)
