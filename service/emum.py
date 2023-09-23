import os
from enum import Enum
class EnvironmentVariables(str, Enum):
    KAFKA_SERVER = 'KAFKA_SERVER'
    KAFKA_PORT = 'KAFKA_PORT'
    KAFKA_GROUP_ID = 'KAFKA_GROUP_ID'
    KAFKA_TOPIC_RAW = 'KAFKA_TOPIC_RAW'
    KAFKA_TOPIC_CFP = 'KAFKA_TOPIC_CFP'
    MONGO_URI = 'MONGO_URI'
    MONGO_COLLECTION = 'MONGO_COLLECTION'
    MONGO_ALIVE_TIMEOUT = 'MONGO_ALIVE_TIMEOUT'
    SASL_PLAIN_USERNAME='SASL_PLAIN_USERNAME'
    SASL_PLAIN_PASSWORD='SASL_PLAIN_PASSWORD'

    HTTP_PORT='HTTP_PORT'
    HTTP_HOST='HTTP_HOST'

    ONLY_REST='ONLY_REST'

    def get_env(self, variable=None):
        return os.environ.get(self, variable)
    

class AbaCfpConfig():
    # static variable __instance
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if AbaCfpConfig.__instance == None:
            AbaCfpConfig.__instance = AbaCfpConfig()
        return AbaCfpConfig.__instance

    HTTP_PORT=int(EnvironmentVariables.HTTP_PORT.get_env() or 8080)
    HTTP_HOST=EnvironmentVariables.HTTP_HOST.get_env() or '0.0.0.0'
    MONGO_URI=EnvironmentVariables.MONGO_URI.get_env() or 'mongodb://localhost:27017/coinscrap'
    MONGO_COLLECTION=EnvironmentVariables.MONGO_COLLECTION.get_env() or 'AggregatedCfp'
    MONGO_ALIVE_TIMEOUT=int(EnvironmentVariables.MONGO_ALIVE_TIMEOUT.get_env() or 5)
    ONLY_REST=bool(EnvironmentVariables.ONLY_REST.get_env() or False)
