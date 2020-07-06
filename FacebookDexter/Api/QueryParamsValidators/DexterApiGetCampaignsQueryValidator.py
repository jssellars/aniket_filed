import json

from flask import Response


class DexterApiGetCampaignsQueryValidator():
    def validate(self, request_args):
        ad_account_id = request_args.get('adAccountId')
        channel = request_args.get('channel')
        if ad_account_id is None and channel is None:
            error = json.dumps('Please provide ad account and channel')
            return Response(response=error, status=400, mimetype='application/json')
        if ad_account_id is None:
            error = json.dumps('Please provide ad account')
            return Response(response=error, status=400, mimetype='application/json')
        if channel is None:
            error = json.dumps('Please provide channel')
            return Response(response=error, status=400, mimetype='application/json')
        return {
            'ad_account_id': ad_account_id,
            'channel': channel
        }
