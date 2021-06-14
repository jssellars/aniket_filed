from dataclasses import dataclass


@dataclass
class DocumentDetails:
    document_content: bytes
    document_name: str
    document_content_type: str
    document_extn: str
    location: str
    is_contract: bool
    campaign_id: int
