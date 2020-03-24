from dataclasses import dataclass


@dataclass
class Field:
    turing_key: str = None
    dexter_key: str = None


class TuringFieldsMetadata:

    all_cpc = Field("cpc_all", "cpc")
    account_id = Field("account_id", "ad_account_id")

