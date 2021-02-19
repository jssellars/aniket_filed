import jwt
from flask import request


def extract_business_owner_facebook_id():
    jwt_data = decode_jwt_from_headers()
    return jwt_data.get("user_facebook_businessowner_id")


def extract_business_owner_google_id():
    jwt_data = decode_jwt_from_headers()
    return jwt_data.get("user_google_businessowner_id")


def extract_user_filed_id():
    jwt_data = decode_jwt_from_headers()
    return jwt_data.get('user_filed_id')


def decode_jwt_from_headers():
    bearer_token = request.headers.get('Authorization')
    token = bearer_token.replace('Bearer ', '')
    jwt_data = jwt.decode(token, verify=False)
    return jwt_data
