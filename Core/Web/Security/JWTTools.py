import json


def extract_business_owner_facebook_id(jwt_data):
    user_details = jwt_data["UserDetailsKey"]
    if isinstance(user_details, str):
        user_details = json.loads(user_details)
    return user_details["FacebookBusinessOwnerId"]


def extract_business_owner_google_id(jwt_data):
    user_details = jwt_data["UserDetailsKey"]
    if isinstance(user_details, str):
        user_details = json.loads(user_details)
    return user_details["GoogleBusinessOwnerId"]
