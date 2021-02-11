from __future__ import annotations

import os
from types import ModuleType
from typing import Dict, Type

from Core.pydantic_extensions import replace_in_class
# WARNING: keep all imports, they are imported from this file downstream
from Core.settings_models import (
    Dexter, Exchange, ExternalServices, Facebook, Google,
    MinimumNumberOfDataPoints, Model, Mongo, Name, Queue, RabbitMq, SqlServer,
    TechnicalUser)


class Default:
    domain = "filed.com"
    facebook = Facebook(
        description="Filed Live",
        api_version="v9.0",
        app_id="174014546372191",
        app_secret="718ab2ca9cc128cf4b1b7793ecc116cb",
    )
    google = Google(
        client_config_path="googleads.yaml",
        developer_token="JcuH_-cVSK9CBVpRz3ZIIg",
        client_id="17118844476-ff344s34figbe2sfjmqa5qg7msrjta7m.apps.googleusercontent.com",
        client_secret="bk0Gae3BgAkbbf63GD5kU4jq",
    )
    technical_user = TechnicalUser(email="technical_account@{domain}", password="Fil3ed-Adm1n")

    sql_server = SqlServer(
        host="ng-dev-sql.{domain}",
        port=1433,
        username="dev_sa",
        password="StartingGunFlounderFun",
        name="{Env}.Filed.Facebook.Accounts",
    )
    mongo = Mongo(
        ssh_tunnel=False,
        mongo_username="root",
        mongo_password="BlokeyWokeySystemChokey",
        mongo_host_external="ng-dev-mongo.{domain}",
        mongo_host_internal="192.168.2.91",
        ssh_host="18.130.129.216",
        mongo_port=27017,
        ssh_username="mongo",
        ssh_password="7YPbhiYTEtM=",
        retry_writes=False,
        logs_database="{env}_app_logs",
        logs_collection_name="logs",
    )
    rabbitmq = RabbitMq(
        consumer_name="{env}.{app_kind}.{app_domain}.{app_name}.consumer",
        publish_interval=1,
        heartbeat=0,
        connection_timeout=300,
        username="ntvkpamp",
        password="k5TYym9Z7sp18wNPd4U6VAyH2C99-HPH",
        hostname="juicy-mosquito.rmq.cloudamqp.com",
        port=5672,
        virtual_host="ntvkpamp",
        default_exchange_type="direct",
        exchanges=[
            Exchange(
                name="{env}.direct",
                type="direct",
                inbound_queue=Queue(
                    name="{env}.{app_domain}.{app_name}.inbound", key="{env}.{app_domain}.{app_name}.inbound.key"
                ),
                outbound_queue=Queue(
                    name="{env}.{app_domain}.{app_name}.outbound", key="{env}.{app_domain}.{app_name}.outbound.key"
                ),
            )
        ],
    )
    external_services = ExternalServices(
        authorize_permission_endpoint="http://cs-users-authorization-api:41005/api/v1/Permissions/authorize-permission",
        users_signin_endpoint="http://cs-users-api:41000/api/v1/users/signin",
        subscription_update_business_owner_endpoint="http://cs-subscriptions-and-billing-api:41010/api/v1/contacts/set-businessowner-facebook-id",
        targeting_search="http://py-facebook-campaigns-builder-api:47220/interests/suggestions/",
        facebook_auto_apply="http://py-facebook-turing-api:47350/api/v1/{level}/{structureId}",
        google_auto_apply="",
        notification_endpoint="http://cs-notifications-api:41020/api/v1/email-messages/send-email",
    )

    es_enabled = False
    es_host = "{env}-elasticsearch"
    es_port = 9200

    logger_level = "DEBUG"
    base_url = "/api/v1"
    version = "1.0.0"

    sync_time = "00:10"


class Local:
    environment = "local"
    endpoint_auth_disabled = True

    external_services = ExternalServices(
        authorize_permission_endpoint="http://localhost:41005/api/v1/Permissions/authorize-permission",
        users_signin_endpoint="http://localhost:41000/api/v1/users/signin",
        subscription_update_business_owner_endpoint="http://localhost:41010/api/v1/contacts/set-businessowner-facebook-id",
        targeting_search="http://localhost:47220/api/v1/interests/suggestions/",
        facebook_auto_apply="http://localhost:47350/api/v1/{level}/{structureId}",
        google_auto_apply="",
        notification_endpoint="http://localhost:41020/api/v1/email-messages/send-email",
    )

    sql_server = replace_in_class(
        Default.sql_server,
        name="Dev.Filed.Facebook.Accounts",
    )

    es_host = "localhost"


class Dev:
    environment = "dev"


class Dev2:
    environment = "dev2"


class Dev3:
    environment = "dev3"


class Staging:
    environment = "staging"
    # TODO: see why staged has a separate host and what makes it different from dev / dev2 / dev3
    rabbitmq = replace_in_class(
        Default.rabbitmq,
        username="ecsubdgh",
        password="ieNetipc0tqrtZvzRkSrqaW6ADyASym0",
        hostname="spotted-starfish.rmq.cloudamqp.com",
        port=5672,
        virtual_host="ecsubdgh",
    )


class Prod:
    environment = "prod"
    environment_domain_url = "app"
    sql_server = SqlServer(
        host="35.176.246.229",
        port=1433,
        username="tempsa",
        password="KoalaBearSplitsaStair",
        name="Prod.Filed.Facebook.Accounts",
    )
    mongo = replace_in_class(
        Default.mongo,
        ssh_tunnel=True,
        mongo_username="root",
        mongo_password="BlokeyWokeySystemChokey",
        mongo_host_external="ng-dev-mongo.{domain}",
        mongo_host_internal="192.168.2.91",
        ssh_host="18.130.129.216",
        mongo_port=27017,
        ssh_username="mongo",
        ssh_password="7YPbhiYTEtM=",
        retry_writes=False,
    )
    rabbitmq = replace_in_class(
        Default.rabbitmq,
        username="eirjtnyh",
        password="cAFjL8M2hdTULtKSa7RgLMwgBGKWt3FZ",
        hostname="frizzy-dragonfly.rmq.cloudamqp.com",
        port=5672,
        virtual_host="eirjtnyh",
    )

    logger_level = "INFO"


ENVIRONMENT_KEY = "PYTHON_ENV"
DEFAULT_ENVIRONMENT = "local"
DEFAULT_SETTINGS_CLASS_NAME = "Default"


def get_environment():
    return os.environ.get(ENVIRONMENT_KEY) or DEFAULT_ENVIRONMENT


def get_class_or_default(module: ModuleType, environment: str) -> Type:
    """Get the class named as the environment in the application's settings.
    If not found, defaults to its equivalent in the Core settings.

    Creates a class by composing the default and environment classes
    from both core and app configs. App configs have precedence."""
    name = environment.capitalize()
    core_default_class = globals()[DEFAULT_SETTINGS_CLASS_NAME]
    core_env_class = globals()[name]
    bases = [core_default_class, core_env_class]

    app_default_class = getattr(module, DEFAULT_SETTINGS_CLASS_NAME, None)
    if app_default_class:
        bases.append(app_default_class)

    app_env_class = getattr(module, name, None)
    if app_env_class:
        bases.append(app_env_class)

    # we reverse bases because former overrides latter as per MRO rules
    return type(name, tuple(reversed(bases)), {})


def get_settings(module: ModuleType, environment: str) -> Model:
    raw_class = get_class_or_default(module, environment)
    settings_as_dict = get_mro_vars(raw_class)

    return Model.parse_obj(settings_as_dict)


def get_mro_vars(cls: Type) -> Dict:
    return {k: v for c in reversed(cls.__mro__) for k, v in vars(c).items() if not k.startswith("_")}
