import json

import humps
from flask import request, Response
from flask_restful import Resource

from Core.Web.FacebookGraphAPI.Tools import Tools
from Core.Web.Security.JWTTools import extract_business_owner_google_id
from Core.Web.Security.Permissions import AccountsPermissions
from GoogleTuring.Api.Commands.AdAccountInsightsCommand import AdAccountInsightsCommand
from GoogleTuring.Api.CommandsHandlers.GoogleAdAccountInsightsHandler import \
    GoogleAdAccountInsightsHandler
from GoogleTuring.Api.Mappings.AdAccountInsightsCommandMapping import AdAccountInsightsCommandMapping
from GoogleTuring.Api.Startup import startup


class AdAccountInsightsEndpoint(Resource):
    @startup.authorize_permission(permission=AccountsPermissions.CAN_ACCESS_ACCOUNTS)
    def post(self):
        try:
            business_owner_google_id = extract_business_owner_google_id()
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = AdAccountInsightsCommandMapping(AdAccountInsightsCommand)
            command = mapping.load(raw_request)
            command.business_owner_google_id = business_owner_google_id
        except Exception as e:
            response = json.dumps({"message": f"Failed to process request. Error {str(e)}"})
            return Response(response=response, status=400, mimetype='application/json')

        try:
            response = GoogleAdAccountInsightsHandler.handle(config=startup.google_config, command=command)
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            response = Tools.create_error(e, 'GOOGLE_ACCOUNTS_BAD_REQUEST')
            response = json.dumps(response)
            return Response(response=response, status=400, mimetype='application/json')
