from typing import Dict, Any

from Core.settings import Prod

ALLOWED_AD_ACCOUNTS = ["756882231399117", "389109158588065"]


# ALLOW MODIFICATION ON FEW AD ACCOUNTS ON ENVIRONMENTS THAT ARE NOT PROD
def allow_structure_changes(account_id: str, config: Any) -> bool:
    return account_id in ALLOWED_AD_ACCOUNTS or config.environment == Prod.environment
