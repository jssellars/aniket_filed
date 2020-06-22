# TODO: ADD STATUS CODES TO EVERY RESPONSE
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from staticpreview.request_handlers import *


@csrf_exempt
def GenerateAdPreview(request):
    if request.method == 'POST':
        request = json.loads(request.body.decode())
    else:
        return HttpResponse(status=400)

    response = GenerateAdPreviewHandler(request)
    response = json.dumps({'response': response})

    return HttpResponse(response)
