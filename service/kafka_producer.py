import os
from kafka import KafkaProducer
import json

class KAFKA_PRODUCER:

    def __init__(self) -> None:
        pass
        
    def producer(self):
        return KafkaProducer(
            bootstrap_servers=os.environ.get('KAFKA_SERVER', 'kafka:9092'),
            value_serializer=lambda x: json.dumps(x).encode('utf-8',),
            security_protocol=os.environ.get('SECURITY_PROTOCOL', 'SASL_PLAINTEXT'),
            sasl_mechanism=os.environ.get('SASL_MECHANISM', 'SCRAM-SHA-256'),
            sasl_plain_username=os.environ.get('SASL_PLAIN_USERNAME', 'admin'), 
            sasl_plain_password=os.environ.get('SASL_PLAIN_PASSWORD', 'admin-secret'),
        )
