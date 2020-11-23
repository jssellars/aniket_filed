from functools import wraps

import flask_restful
import requests
from flask import request


def authorize_jwt(permission_endpoint):
    def authorize_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            authorized = _authorize_jwt(permission_endpoint=permission_endpoint)

            if authorized:
                return func(*args, **kwargs)

            flask_restful.abort(403)

        return wrapper

    return authorize_wrapper


def authorize_permission(permission_endpoint):
    def inner_authorize_permission(permission):
        def authorize_wrapper(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                authorized = _authorize_permission(
                    permission_endpoint=permission_endpoint,
                    module=permission.module.value,
                    permission=permission.value
                )

                if authorized:
                    return func(*args, **kwargs)

                flask_restful.abort(403)

            return wrapper

        return authorize_wrapper

    return inner_authorize_permission


def _authorize_jwt(permission_endpoint):
    headers = {'Authorization': request.headers.get('Authorization')}
    response = requests.get(permission_endpoint, headers=headers)
    return response.status_code == 204


def _authorize_permission(permission_endpoint, **kwargs):
    headers = {'Authorization': request.headers.get('Authorization')}
    response = requests.get(permission_endpoint, params=kwargs, headers=headers)
    return response.status_code == 204


def add_bearer_token(token, headers=None):
    if not headers:
        headers = {}
    headers["Authorization"] = f"Bearer {token}"
    headers["Content-Type"] = "application/json"
    return headers


def generate_technical_token(technical_token_manager):
    token = technical_token_manager.get_token()
    return token
