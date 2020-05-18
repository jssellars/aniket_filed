from copy import deepcopy

from facebook_business.api import Cursor
from facebook_business.exceptions import FacebookRequestError


class Tools(object):

    @staticmethod
    def ConvertToJson(inputValue):
        if isinstance(inputValue, Cursor):
            value = []
            for entry in inputValue:
                value.append(deepcopy(entry._json))
        elif inputValue:
            try:
                value = inputValue.export_all_data()
            except AttributeError:
                value = inputValue._json
        else:
            value = inputValue
        return value

    @staticmethod
    def CreateError(error, source):
        if isinstance(error, FacebookRequestError):
            apiErrorCode = error.api_error_code()
            error = error._error
            if 'error_user_message' in error.keys():
                message = error['error_user_message']
            else:
                message = error['message']
            errorMessagePartial = {
                'message': message,
                'code': apiErrorCode,
                'type': source,
                'fbtrace_id': None
            }
            errorMessage = {'message': errorMessagePartial,
                            'code': 1,
                            'type': source,
                            'fbtrace_id': None}
        elif isinstance(error, KeyError):
            errorMessagePartial = {
                'message': 'Invalid key',
                'code': 1,
                'type': source,
                'fbtrace_id': None
            }
            errorMessage = {'message': errorMessagePartial,
                            'code': 1,
                            'type': source,
                            'fbtrace_id': None
                            }
        else:
            errorMessagePartial = {
                'message': str(error),
                'code': 1,
                'type': source,
                'fbtrace_id': None
            }
            errorMessage = {'message': errorMessagePartial,
                            'code': 1,
                            'type': source,
                            'fbtrace_id': None
                            }

        return errorMessage
