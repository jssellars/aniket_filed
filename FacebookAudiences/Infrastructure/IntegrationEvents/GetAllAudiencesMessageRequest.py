from dataclasses import dataclass


@dataclass
class GetAllAudiencesMessageRequest:
    business_owner_facebook_id: str = None
    business_id: str = None
    ad_account_id: str = None
