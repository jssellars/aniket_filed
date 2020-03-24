from pymongo import MongoClient
from sshtunnel import SSHTunnelForwarder


class MongoConnectionHandlerException(Exception):
    pass


class MongoConnectionHandler(object):

    def __init__(self, mongo_config):
        if mongo_config.sshTunnel:
            server = SSHTunnelForwarder(
                (mongo_config.mongoHost, 22),
                ssh_username=mongo_config.mongoSSHUser,
                ssh_password=mongo_config.mongoSSHPass,
                remote_bind_address=(mongo_config.remoteIP, mongo_config.remotePort)
            )
            server.start()

            self._client = MongoClient(host='127.0.0.1', port=server.local_bind_port, username=mongo_config.mongoUser, password=mongo_config.mongoPass)
        else:
            self._client = MongoClient(mongo_config.connection_string)

    @property
    def client(self):
        if self._client is None:
            raise MongoConnectionHandlerException('Invalid database connection.')

        return self._client

    def close(self):
        self._client.close()
