import os
from pymongo import MongoClient, timeout

class MONGO:

    def __init__(self) -> None:
        pass

    def client_connector(self):
        client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://mongo:27017/coinscrap'))
        # database = client.get_database()._Database__name
        # db = client[database][os.environ.get('MONGO_URI', 'AggregatedCfp']
        return client

