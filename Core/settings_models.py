from typing import Any, List, Optional

from pydantic import BaseModel, Extra, Field, root_validator

from Core.pydantic_extensions import format_templates_recursive


class Queue(BaseModel):
    name: str
    key: str


class Exchange(BaseModel):
    name: str
    type: str
    inbound_queue: Optional[Queue]
    outbound_queue: Optional[Queue]


class RabbitMq(BaseModel):
    consumer_name: Optional[str]
    hostname: str
    port: int
    username: str
    password: str
    connection_timeout: int
    default_exchange_type: str
    exchanges: List[Exchange]
    heartbeat: int
    publish_interval: int
    virtual_host: str

    @property
    def connection_string(self):
        return f"amqp://{self.username}:{self.password}@{self.hostname}:{self.port}/{self.virtual_host}"

    @property
    def default_exchange(self) -> Exchange:
        return self.get_exchange_by_type(self.default_exchange_type)

    def get_exchange_by_type(self, exchange_type: str) -> Optional[Exchange]:
        for e in self.exchanges:
            if e.type == exchange_type:
                return e

        return None

    @property
    def secondary_exchange(self) -> Optional[Exchange]:
        if len(self.exchanges) == 2:
            return self.exchanges[1]

        return None


class SqlServer(BaseModel):
    host: str
    port: int
    username: str
    password: str
    name: str

    @property
    def connection_string(self):
        return f"mssql+pymssql://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"


class Mongo(BaseModel):
    ssh_tunnel: bool
    ssh_host: str
    ssh_username: str
    ssh_password: str
    mongo_host_external: str
    mongo_host_internal: str
    mongo_port: int
    mongo_username: str
    mongo_password: str
    retry_writes: bool
    accounts_collection_name: Optional[str]
    accounts_database: Optional[str]
    accounts_journal_collection_name: Optional[str]
    accounts_journal_database_name: Optional[str]
    accounts_journal_sync_reports_collection_name: Optional[str]
    business_owner_pages_collection_name: Optional[str]
    google_accounts_database_name: Optional[str]
    google_insights_database_name: Optional[str]
    google_structures_database_name: Optional[str]
    insights_database: Optional[str]
    insights_database_name: Optional[str]
    journal_collection_name: Optional[str]
    journal_database_name: Optional[str]
    location_data_collection_name: Optional[str]
    logging_collection_name: Optional[str]
    logging_database_name: Optional[str]
    logs_database: Optional[str]
    logs_collection_name: Optional[str]
    recommendations_collection_name: Optional[str]
    recommendations_database_name: Optional[str]
    structures_database: Optional[str]
    structures_database_name: Optional[str]
    publish_feedback_database_name: Optional[str]
    publish_feedback_collection_name: Optional[str]

    @property
    def connection_string_internal(self):
        if self.mongo_username and self.mongo_password:
            return (
                f"mongodb://{self.mongo_username}:{self.mongo_password}"
                f"@{self.mongo_host_internal}:{self.mongo_port}/?authSource=admin"
            )
        return f"{self.mongo_host_internal}:{self.mongo_port}/?authSource=admin"

    @property
    def connection_string_external(self):
        if self.mongo_username and self.mongo_password:
            return (
                f"mongodb://{self.mongo_username}:{self.mongo_password}"
                f"@{self.mongo_host_external}:{self.mongo_port}/?authSource=admin"
            )

        return f"{self.mongo_host_external}:{self.mongo_port}"


class ExternalServices(BaseModel):
    authorize_permission_endpoint: Optional[str]
    facebook_auto_apply: Optional[str]
    google_auto_apply: Optional[str]
    subscription_update_business_owner_endpoint: Optional[str]
    targeting_search: Optional[str]
    users_signin_endpoint: Optional[str]
    notification_endpoint: Optional[str]


class TechnicalUser(BaseModel):
    email: str
    password: str


class Facebook(BaseModel):
    description: str
    api_version: str
    app_id: str
    app_secret: str


class Google(BaseModel):
    client_config_path: str
    developer_token: str
    client_id: str
    client_secret: str
    client_secret: str
    redirect_uri: str
    token_url: str
    scopes: List[str]


class MinimumNumberOfDataPoints(BaseModel):
    field_3: int = Field(..., alias="3")
    field_7: int = Field(..., alias="7")
    field_14: int = Field(..., alias="14")
    field_30: int = Field(..., alias="30")


class Dexter(BaseModel):
    min_results: int
    days_since_last_change: int
    recommendation_days_last_updated: int
    time_intervals: List[int]
    date_stop: Any
    minimum_number_of_data_points: Optional[MinimumNumberOfDataPoints]


class Name(BaseModel):
    domain: str
    name: str
    kind: str

    @property
    def full(self):
        return "".join(i.title() for i in (self.domain, self.name, self.kind))


class Model(BaseModel):
    domain: str
    base_url: str
    environment: str
    environment_domain_url: Optional[str]
    logger_level: str
    name: Name
    version: str
    days_to_sync: Optional[int]
    dexter: Optional[Dexter]
    external_services: Optional[ExternalServices]
    es_enabled: Optional[bool]
    es_host: Optional[str]
    es_port: Optional[int]
    facebook: Optional[Facebook]
    google: Optional[Google]
    mongo: Optional[Mongo]
    port: Optional[int]
    rabbitmq: Optional[RabbitMq]
    sql_server: Optional[SqlServer]
    sync_time: Optional[str]
    technical_user: Optional[TechnicalUser]
    endpoint_auth_disabled: bool = False

    @root_validator(allow_reuse=True)
    def format_templates(cls, values):
        return {k: format_templates_recursive(v, values) for k, v in values.items()}

    # TODO: apply to all models
    class Config:
        validate_assignment = True
        extra = Extra.forbid

    @property
    def version_endpoint_payload(self):
        return {"name": self.name.full, "version": self.version, "environment": self.environment}
