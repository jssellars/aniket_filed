from datetime import datetime
from threading import Lock

import requests
from jwt import decode

from Core.Web.Security.Authorization import add_bearer_token


class TechnicalTokenManager:
    def __init__(self):
        self.__token = None
        self.__expiration_date = None
        self.__set_token_lock = Lock()
        self.__get_token_lock = Lock()

    def __set_token(self, token, secret_key):
        self.__set_token_lock.acquire()
        if not token:
            raise Exception('Token is None!')

        self.__token = token
        decoded_token = decode(token, secret_key, options={'verify_aud': False})
        expiration_date = datetime.fromtimestamp(decoded_token['exp'])
        self.__expiration_date = expiration_date
        self.__set_token_lock.release()

    def get_token(self, startup):
        self.__get_token_lock.acquire()
        if self.__token and self.__expiration_date > datetime.now():
            self.__get_token_lock.release()
            return self.__token
        else:
            params = {
                "EmailAddress": startup.admin_user.email,
                "Password": startup.admin_user.password
            }

            sign_in_response = requests.post(startup.external_services.users_signin_endpoint, json=params,
                                             headers={"Content-Type": "application/json"})

            filed_admin_token = None
            if sign_in_response.status_code == 200:
                filed_admin_token = sign_in_response.json()
                filed_admin_token = filed_admin_token.replace('"', '')

            headers = add_bearer_token(filed_admin_token)

            response = requests.get(startup.external_services.users_technical_token_endpoint, headers=headers)

            technical_token = None
            if response.status_code == 200:
                response = response.json()
                technical_token = response.replace('"', '')

            self.__set_token(technical_token, startup.jwt_secret_key)
            self.__get_token_lock.release()
            return technical_token
