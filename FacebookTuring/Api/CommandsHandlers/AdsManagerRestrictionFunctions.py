from typing import Dict

from FacebookTuring.Api.startup import config

ALLOWED_AD_ACCOUNTS = ["756882231399117", "389109158588065"]


# ALLOW MODIFICATION ON FEW AD ACCOUNTS ON ENVIRONMENTS THAT ARE NOT PROD
def allow_structure_changes(structure: Dict) -> bool:
    return structure["account_id"] in ALLOWED_AD_ACCOUNTS or config.environment == "prod"
