from datetime import datetime
from threading import Lock

import requests
from jwt import decode


class TechnicalTokenManager:
    __NUM_OF_RETRIES = 3

    def __init__(self, technical_user, external_services):
        self.__technical_user = technical_user
        self.__external_services = external_services

        self.__token = None
        self.__expiration_date = None
        self.__set_token_lock = Lock()
        self.__get_token_lock = Lock()

    def __set_token(self, token):
        self.__set_token_lock.acquire()
        if not token:
            raise Exception('Token is None!')

        self.__token = token
        decoded_token = decode(token, verify=False)
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
                "EmailAddress": self.__technical_user.email,
                "Password": self.__technical_user.password
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

            technical_token = sign_in_response.json()
            technical_token = technical_token.replace('"', '')

            self.__set_token(technical_token)
            self.__get_token_lock.release()
            return technical_token
