from typing import Dict, Any

ALLOWED_AD_ACCOUNTS = ["756882231399117", "389109158588065"]


# ALLOW MODIFICATION ON FEW AD ACCOUNTS ON ENVIRONMENTS THAT ARE NOT PROD
def allow_structure_changes(structure: Dict, startup: Any) -> bool:
    return structure["account_id"] in ALLOWED_AD_ACCOUNTS or startup.environment == "prod"
