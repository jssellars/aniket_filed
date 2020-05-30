from facebook_business.exceptions import FacebookRequestError


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
    def create_error_rabbit(error, code=None, source=None):
        if code is None:
            code = "BadRequest"
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
                'description': message,
                'code': code,
                'type': source,
                'fbtrace_id': None
            }
        elif isinstance(error, KeyError):
            error_message = {
                'message': 'Invalid key',
                'code': code,
                'type': source,
                'fbtrace_id': None
            }
        else:
            error_message = {
                'message': str(error),
                'code': code,
                'type': source,
                'fbtrace_id': None
            }

        return error_message

    @staticmethod
    def create_error(error, code=None, source=None):
        if code is None:
            code = "BadRequest"
        if isinstance(error, FacebookRequestError):
            error = error._error
            if 'error_user_message' in error.keys():
                message = error['error_user_message']
            elif 'error_user_msg' in error.keys():
                message = error['error_user_msg']
            else:
                message = error['message']
            error_message = {
                'description': message,
                'code': code
            }
        elif isinstance(error, KeyError):
            error_message = {
                'description': str(error),
                'code': code
            }
        else:
            error_message = {
                'description': str(error),
                'code': code
            }

        return error_message
