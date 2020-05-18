import json
import typing

from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum


class LoggerMessageStartup(LoggerMessageBase):

    def __init__(self, app_config: typing.Dict = None, **kwargs):
        self.app_config = app_config
        super().__init__(**kwargs)

    def to_dict(self):
        # get rabbit config details
        rabbit_config = self.app_config.get("rabbitmq", None)
        if rabbit_config is not None:
            rabbit_config_details = {
                "username": rabbit_config["username"],
                "hostname": rabbit_config["hostname"],
                "port": rabbit_config["port"],
                "virtual_host": rabbit_config["virtual_host"],
                "exchanges": rabbit_config["exchanges"]
            }
        else:
            rabbit_config_details = {}

        mongo_config = self.app_config.get("mongo_database", None)
        if mongo_config is not None:
            mongo_config_details = {
                "mongo_host": mongo_config["mongo_host"],
                "remote_ip": mongo_config["remote_ip"],
                "remote_port": mongo_config["remote_port"],
            }
            for key, value in mongo_config.items():
                if key.find("database") > -1:
                    mongo_config_details[key] = value
                if key.find("collection") > -1:
                    mongo_config_details[key] = value
        else:
            mongo_config_details = {}

        # get facebook config details
        facebook_config = self.app_config.get("facebook", None)
        if facebook_config is not None:
            facebook_config_details = {
                "description": facebook_config["description"],
                "api_version": facebook_config["api_version"]
            }
        else:
            facebook_config_details = {}

        sql_config = self.app_config.get("sql_server_database", None)
        if sql_config is not None:
            sql_config_details = {
                "host": sql_config["host"],
                "port": sql_config["port"],
                "database": sql_config["name"]
            }
        else:
            sql_config_details = {}

        external_services = self.app_config.get("external_services", None)

        details = {
            "details": {
                "type": LoggerMessageTypeEnum.STARTUP.value,
                "name": self.app_config.get("service_name", None),
                "description": self.description,
                "environment": self.app_config.get("environment", None),
                "api_name": self.app_config.get("api_name", None),
                "api_version": self.app_config.get("api_version", None),
                "service_version": self.app_config.get("service_version", None),
                "port": self.app_config.get("port", None),
                "debug_mode": self.app_config.get("debug_mode", None),
                "rabbit": json.dumps(rabbit_config_details),
                "mongo": json.dumps(mongo_config_details),
                "tokens_database": json.dumps(sql_config_details),
                "facebook": json.dumps(facebook_config_details),
                "external_services": json.dumps(external_services) if external_services is not None else {}
            }
        }
        return details
