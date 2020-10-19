from dataclasses import dataclass

from PotterFacebookAccounts.Infrastructure.GraphAPIDtos.GraphAPIBusinessDto import GraphAPIBusinessDto


@dataclass
class GraphAPIAdAccountDto:
    id: str = None
    account_id: str = None
    name: str = None
    account_status: int = None
    currency: str = None
    business: GraphAPIBusinessDto = None
