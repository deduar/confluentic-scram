import os
from kafka import KafkaConsumer
import json

class KAFKA_CONSUMER:

    def __init__(self) -> None:
        pass
        
    def consumer(self):
        return KafkaConsumer(
            os.environ.get('KAFKA_TOPIC_RAW', 't_raw'),
            group_id=os.environ.get('KAFKA_GROUP_ID', 'group_1'),
            bootstrap_servers=os.environ.get('KAFKA_SERVER', 'kafka:9092'),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            security_protocol=os.environ.get('SECURITY_PROTOCOL', 'SASL_PLAINTEXT'),
            sasl_mechanism=os.environ.get('SASL_MECHANISM', 'SCRAM-SHA-256'),
            sasl_plain_username=os.environ.get('SASL_PLAIN_USERNAME', 'admin'), 
            sasl_plain_password=os.environ.get('SASL_PLAIN_PASSWORD', 'admin-secret'),
        )
    