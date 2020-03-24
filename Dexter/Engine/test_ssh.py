import json
import pymongo
from sshtunnel import SSHTunnelForwarder

MONGO_HOST = '18.130.129.216'
MONGO_USER = 'mongo'
MONGO_PASS = '7YPbhiYTEtM='
MONGO_DB = 'testDB'

def Collect_Pid_DB():
  server = SSHTunnelForwarder(
    (MONGO_HOST,22),
    ssh_username=MONGO_USER,
    ssh_password=MONGO_PASS,
    remote_bind_address=('192.168.2.91', 27017)
  )

  print('ceva')
  server.start()
  print('ceva')
  client = pymongo.MongoClient(host='127.0.0.1',
      port=server.local_bind_port,
      username='mongo-admin',
      password='7YPbhiYTEtM=')
  db = client[MONGO_DB]
  print (db)
  print(json.dumps(db.collection_names(), indent=2))

Collect_Pid_DB()