from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.exceptions import FacebookRequestError

from Core.Tools.Misc.ObjectManipulators import extract_class_attributes_values


class Tools(object):

    @staticmethod
    def convert_to_json(value):
        if value:
            try:
                value = value.export_all_data()
            except AttributeError:
                value = value._json
        return value

    @staticmethod
    def create_error(error, source=None):
        if isinstance(error, FacebookRequestError):
            api_error_code = error.api_error_code()
            error = error._error
            if 'error_user_message' in error.keys():
                message = error['error_user_message']
            elif 'error_user_msg' in error.keys():
                message = error['error_user_msg']
            else:
                message = error['message']
            error_message = {
                'message': message,
                'code': api_error_code,
                'type': source,
                'fbtrace_id': None
            }
        elif isinstance(error, KeyError):
            error_message = {
                'message': 'Invalid key',
                'code': 1,
                'type': source,
                'fbtrace_id': None
            }
        else:
            error_message = {
                'message': str(error),
                'code': 1,
                'type': source,
                'fbtrace_id': None
            }
            
        return error_message


class FacebookInsightsFieldsAndParameters:
    fields = extract_class_attributes_values(AdsInsights.Field)
    breakdowns = extract_class_attributes_values(AdsInsights.Breakdowns)
    action_breakdowns = extract_class_attributes_values(AdsInsights.ActionBreakdowns)
    action_attribution_windows = extract_class_attributes_values(AdsInsights.ActionAttributionWindows)
