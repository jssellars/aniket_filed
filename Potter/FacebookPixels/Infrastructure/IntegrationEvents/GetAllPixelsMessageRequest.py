from dataclasses import dataclass


@dataclass 
class GetAllPixelsMessageRequest:
    business_owner_facebook_id: str = None
    ad_account_id: str = None 