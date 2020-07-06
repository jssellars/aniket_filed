from dataclasses import dataclass


@dataclass
class DexterApiLoggingInfo:
    name: str
    logger_type: str
    es_host: str
    es_port: int
    level: str
    index_name: str
