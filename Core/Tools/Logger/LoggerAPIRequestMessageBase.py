import typing

from flask import request


class LoggerAPIRequestMessageBase:
    def __init__(self, api_request: request = None):
        self.details = {
            'details': {
                'verb': api_request.method,
                'base_url': api_request.base_url,
                'endpoint': api_request.endpoint,
                'full_path': api_request.full_path,
                'remote_address': api_request.remote_addr,
                'payload': api_request.get_data()
                # === WARNING ===
                # === !! only activate this log if it is really needed !! ===
                # 'headers': api_request.headers
            }
        }

    def to_dict(self) -> typing.Dict:
        return self.details

    @property
    def request_details(self) -> typing.Dict:
        return self.details["details"]
