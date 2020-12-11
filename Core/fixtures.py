from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Core import settings
from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Core.Web.Security.Authorization import authorize_permission, fake_authorize_permission, fake_authorize_jwt, \
    authorize_jwt
from Core.Web.Security.TechnicalTokenManager import TechnicalTokenManager
from Core.mongo_adapter import MongoAdapter
from Core.rabbitmq_adapter import RabbitMqAdapter


class Fixtures:
    def __init__(self, config: settings.Model) -> None:
        self.config = config

        self._authorize_permission = None
        self._authorize_jwt = None
        self._mongo_adapter = None
        self._rabbitmq_adapter = None
        self._sql_db_engine = None
        self._sql_db_session = None
        self._business_owner_repository = None
        self._technical_token_manager = None

    @property
    def authorize_permission(self):
        if self._authorize_permission is None:
            func = fake_authorize_permission if self.config.endpoint_auth_disabled else authorize_permission
            self._authorize_permission = func(self.config.external_services.authorize_permission_endpoint)

        return self._authorize_permission

    @property
    def authorize_jwt(self):
        if self._authorize_jwt is None:
            func = fake_authorize_jwt if self.config.endpoint_auth_disabled else authorize_jwt
            self._authorize_jwt = func(self.config.external_services.authorize_permission_endpoint)

        return self._authorize_jwt

    @property
    def mongo_adapter(self):
        if self._mongo_adapter is None:
            self._mongo_adapter = MongoAdapter(self.config.mongo)

        return self._mongo_adapter

    @property
    def rabbitmq_adapter(self):
        """Uses default exchange."""
        if self._rabbitmq_adapter is None:
            self._rabbitmq_adapter = RabbitMqAdapter(
                self.config.rabbitmq, self.config.rabbitmq.default_exchange
            )

        return self._rabbitmq_adapter

    def get_rabbit_mq_adapter(self, exchange_type: str) -> RabbitMqAdapter:
        return RabbitMqAdapter(self.config.rabbitmq, self.config.rabbitmq.get_exchange_by_type(exchange_type))

    @property
    def sql_db_engine(self):
        if self._sql_db_engine is None:
            self._sql_db_engine = create_engine(self.config.sql_server.connection_string)

        return self._sql_db_engine

    @property
    def sql_db_session(self):
        if self._sql_db_session is None:
            self._sql_db_session = sessionmaker(bind=self.sql_db_engine)

        return self._sql_db_session

    @property
    def business_owner_repository(self):
        if self._business_owner_repository is None:
            self._business_owner_repository = BusinessOwnerRepository(self.sql_db_session)

        return self._business_owner_repository

    @property
    def technical_token_manager(self):
        if self._technical_token_manager is None:
            self._technical_token_manager = TechnicalTokenManager(
                self.config.technical_user, self.config.external_services
            )

        return self._technical_token_manager
