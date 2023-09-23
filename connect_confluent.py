from confluent_kafka import Producer
import socket

conf = {
    'bootstrap.servers': "b-2.abacfpdev.bzswyw.c4.kafka.eu-west-3.amazonaws.com:9096",
    'client.id': socket.gethostname()

    }

producer = Producer(conf)
producer.produce('t_test',"{'uno':1,'dos':2}")

