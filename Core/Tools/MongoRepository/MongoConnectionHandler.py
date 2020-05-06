from pymongo import MongoClient
from sshtunnel import SSHTunnelForwarder, create_logger


class MongoConnectionHandlerException(Exception):
    pass


class MongoConnectionHandler(object):

    __localhost = '127.0.0.1'

    def __init__(self, config):
        if config.ssh_tunnel:
            self.__ssh_tunnel = SSHTunnelForwarder(
                (config.mongo_host, 22),
                ssh_username=config.mongo_ssh_user,
                ssh_password=config.mongo_ssh_pass,
                remote_bind_address=(config.remote_ip, config.remote_port),
                set_keepalive=10,
                logger=create_logger(loglevel=1)
            )
            self.__ssh_tunnel.start()
            self.__client = MongoClient(host=self.__localhost, port=self.__ssh_tunnel.local_bind_port, username=config.mongo_user, password=config.mongo_pass, retryWrites=config.retry_writes)
        else:
            self.__client = MongoClient(config.connection_string)

    @property
    def client(self):
        if self.__client is None:
            raise MongoConnectionHandlerException('Invalid database connection.')

        return self.__client

    def close(self):
        self.__client.close()
        self.__ssh_tunnel.close()
