class DexterApiGetCountsByCategoryCommandValidator:
    def validate(self, request_json):
        errors = []

        data= request_json
        campaigns_ids = data.get('campaignIds')
        channel = data.get('channel')

        if not campaigns_ids:
            errors.append('Campaign Ids not provided')

        if not channel:
            errors.append('Channel not provided')

        if len(errors) > 0:
            return False, errors

        parameters = {
            "campaign_ids": campaigns_ids,
            "channel" : channel
        }

        return True, parameters
