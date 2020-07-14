from datetime import datetime
from threading import Lock

import requests
from jwt import decode

from Core.Web.Security.Authorization import add_bearer_token


class TechnicalTokenManager:
    __NUM_OF_RETRIES = 3

    def __init__(self, admin_user, external_services, jwt_secret_key):
        self.__admin_user = admin_user
        self.__external_services = external_services
        self.__jwt_secret_key = jwt_secret_key

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

    def get_token(self):
        self.__get_token_lock.acquire()
        if self.__token and self.__expiration_date > datetime.now():
            self.__get_token_lock.release()
            return self.__token
        else:
            params = {
                "EmailAddress": self.__admin_user.email,
                "Password": self.__admin_user.password
            }

            sign_in_response = requests.post(self.__external_services.users_signin_endpoint, json=params,
                                             headers={"Content-Type": "application/json"})
            counter = 1
            while sign_in_response.status_code != 200 and counter != self.__NUM_OF_RETRIES:
                counter += 1
                sign_in_response = requests.post(self.__external_services.users_signin_endpoint, json=params,
                                                 headers={"Content-Type": "application/json"})
            if sign_in_response.status_code != 200:
                raise Exception('Sign in failed!')

            filed_admin_token = sign_in_response.json()
            filed_admin_token = filed_admin_token.replace('"', '')

            headers = add_bearer_token(filed_admin_token)
            response = requests.get(self.__external_services.users_technical_token_endpoint, headers=headers)
            counter = 1

            while response.status_code != 200 and counter != self.__NUM_OF_RETRIES:
                counter += 1
                response = requests.get(self.__external_services.users_technical_token_endpoint, headers=headers)

            if response.status_code != 200:
                raise Exception('Could not retrieve the technical token!')

            response = response.json()
            technical_token = response.replace('"', '')

            self.__set_token(technical_token, self.__jwt_secret_key)
            self.__get_token_lock.release()
            return technical_token
