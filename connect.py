from kafka import KafkaConsumer, KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaClient
import json


admin_client = KafkaAdminClient(
    bootstrap_servers='b-2.abacfpdev.bzswyw.c4.kafka.eu-west-3.amazonaws.com:9096,b-3.abacfpdev.bzswyw.c4.kafka.eu-west-3.amazonaws.com:9096,b-1.abacfpdev.bzswyw.c4.kafka.eu-west-3.amazonaws.com:9096',
    security_protocol="SASL_SSL",
    sasl_mechanism="SCRAM-SHA-512",
    sasl_plain_username='coinscrap',
    sasl_plain_password='iAxAMDTL8atzac',
    client_id='test'
)

topic_list = []
topic_list.append(NewTopic(name="t_raw", num_partitions=1, replication_factor=1))
try:
    admin_client.create_topics(new_topics=topic_list, validate_only=False)
except:
    print("topic exist !!!")


producer =  KafkaProducer(
    value_serializer=lambda v:json.dumps(v).encode('utf-8'),
    security_protocol="SASL_SSL",
    sasl_mechanism="SCRAM-SHA-512",
    sasl_plain_username="coinscrap", 
    sasl_plain_password="iAxAMDTL8atzac",
    bootstrap_servers='b-2.abacfpdev.bzswyw.c4.kafka.eu-west-3.amazonaws.com:9096,b-3.abacfpdev.bzswyw.c4.kafka.eu-west-3.amazonaws.com:9096,b-1.abacfpdev.bzswyw.c4.kafka.eu-west-3.amazonaws.com:9096'
)

mov_01 = {'identifier':'TEST124','amount':'-15,3','date':'2023-08-08','title':'compras Zara','cat_id':77}
producer.send("t_raw", mov_01)

consumer = KafkaConsumer(
    't_raw',
    value_deserializer=lambda x: json.dumps(x.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    security_protocol="SASL_SSL",
    sasl_mechanism="SCRAM-SHA-512",
    sasl_plain_username='coinscrap',
    sasl_plain_password='iAxAMDTL8atzac',
    bootstrap_servers='b-2.abacfpdev.bzswyw.c4.kafka.eu-west-3.amazonaws.com:9096,b-3.abacfpdev.bzswyw.c4.kafka.eu-west-3.amazonaws.com:9096,b-1.abacfpdev.bzswyw.c4.kafka.eu-west-3.amazonaws.com:9096'
)

for msg in consumer:
    print (msg.value)


# consumer = Consumer(conf)
# # https://docs.oracle.com/es-ww/iaas/Content/Streaming/Tasks/streaming-kafka-python-client-quickstart.htm