import os
from dotenv import load_dotenv
import json
import datetime
import pytz
import requests

import warnings
warnings.filterwarnings("ignore")

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

import threading
from flask import Flask

from service.service import SERVICE
from service.mongo import MONGO
from kafka.admin import KafkaAdminClient, NewTopic
from service.kafka_consumer import KAFKA_CONSUMER
from service.kafka_producer import KAFKA_PRODUCER
from service.mapping import MAPPING
from service.avro import ConsumerModel, ProducerModel

from coco_cfp_pfm_es.cfp_pfm_es import config_pfm_es, CFP

rest = Flask(__name__)

@rest.route('/')
def index():
    return 'Coinscrap'

@rest.route('/health')
def health():
    try:
        connect[connect.get_database()._Database__name].command('ping')
        return 'True'
    except Exception as e:
        # set response code to 500 and return with KO
        return 'False'
    
@rest.route('/avro_consumer') 
def avro_consumer():
    avro_consumer = {
        "namespace": "aba_cfp.consumer.avro",
        "type": "record",
        "name": "consumer",
        "fields": [
            {"name": "identifier", "type": "string"},
            {"name": "amount",  "type": "float"},
            {"name": "date", "type": "string"},
            {"name": "title", "type": "string"},
            {"name": "cat_id", "type": "int"},
        ]
    }
    return {"AVRO: ":os.environ.get('KAFKA_TOPIC_RAW', 't_raw'),"schema:":avro_consumer}

@rest.route('/avro_producer')
def avro_producer():
    avro_producer = {
        "namespace": "aba_cfp.producer.avro",
        "type": "record",
        "name": "producer",
        "fields": [
            {"name": "co2", "type": "float"},
            {"name": "ch4",  "type": "float"},
            {"name": "n2o", "type": "float"},
            {"name": "h2o", "type": "float"},
        ]
    }
    return {"AVRO: ":os.environ.get('KAFKA_TOPIC_CFP', 't_cfp'),"schema:":avro_producer}

def main_rest():
    # os.environ.get('MONGO_COLLECTION', 'AggregatedCfp'
    rest.run(port=os.environ.get('HEALTH_PORT', '3000'), host='app')

def mongo_thread():
    main_rest(), threading.current_thread()

def main():

    ##LOAD ENV
    load_dotenv()

    ##CREATE MONGO CONNECTOR (fork)
    mong = MONGO()
    global connect
    connect = mong.client_connector()

    #START FLASK for HEALT CHECK /healt
    t = threading.Thread(target=mongo_thread)
    t.start()

    #LOAD MAPPING
    mapp = MAPPING()
    df_map = mapp.load_mapping()

    #LOAD CFP PFM ES
    cfp = CFP(conf=config_pfm_es.load())

    #KAFKA CREATE TOPICS - KafkaAdmin
    admin_client = KafkaAdminClient(
        bootstrap_servers=os.environ.get('KAFKA_SERVER', 'kafka:9092'),
        security_protocol=os.environ.get('SECURITY_PROTOCOL', 'SASL_PLAINTEXT'),
        sasl_mechanism=os.environ.get('SASL_MECHANISM', 'SCRAM-SHA-256'),
        sasl_plain_username=os.environ.get('SASL_PLAIN_USERNAME', 'admin'), 
        sasl_plain_password=os.environ.get('SASL_PLAIN_PASSWORD', 'admin-secret'),
        client_id='1'
    )
    topic_list = []
    topic_list.append(NewTopic(name=os.environ.get('KAFKA_TOPIC_RAW', 't_raw'), num_partitions=1, replication_factor=1))
    topic_list.append(NewTopic(name=os.environ.get('KAFKA_TOPIC_CFP', 't_cfp'), num_partitions=1, replication_factor=1))   
    try:
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
    except:
        pass

    # ##KAFAK PRODUCER
    producer = KAFKA_PRODUCER().producer()

    ##KAFKA SCHEMA PRODUCER
    schema_producer = requests.get(os.environ.get('AVRO_PRODUCER', 'http://app:3000/avro_producer'))
    schema_producer = schema_producer.json()
    producerModel = ProducerModel(None,None,None,None,None)

    #### !!!!!
    #### SEND MESSAGE TO TOPIC T_RAW for check flow !!! REMOVE BEFORE RELEASE
    mov_01 = {'identifier':'TEST124','amount':'-15,3','date':'2023-09-04','title':'compras Zara','cat_id':77}
    producer.send("t_raw", mov_01)
    #### !!!!

    ##KAFKA CONSUMER
    consumer = KAFKA_CONSUMER().consumer()
    
    ##KAFKA SCHEMA CONSUMER
    schema_consumer = requests.get(os.environ.get('AVRO_CONSUMER', 'http://app:3000/avro_consumer'))
    schema_consumer = schema_consumer.json()
    consumerModel = ConsumerModel(None,None,None,None,None)

    # # ##ESTMATE CFP, WRITE IN TOPIC AND UPDATE MONGODB
    timezone = pytz.timezone(os.environ.get('TIME_ZONE', 'Europe/Madrid'))
    for message in consumer:
        message = message.value
        try:
            consumerModel.set_identifier(message['identifier'])
            consumerModel.set_amount(message['amount'])
            consumerModel.set_date(message['date'])
            consumerModel.set_title(message['title'])
            consumerModel.set_cat_id(message['cat_id'])

            df_cat_subCat = mapp.get_cat_subcat(mapp=df_map,cat_id=float(message['cat_id']))
            if len(df_cat_subCat) > 0 :
                mov_to_estimate = {
                    "user_id": consumerModel.get_identifier(),
                    "amount": consumerModel.get_amount(),
                    "date":  consumerModel.get_date(),
                    "title": consumerModel.get_title(),
                    "category":df_cat_subCat.iloc[0]['cat'],
                    "subcategory": df_cat_subCat.iloc[0]['subcat']
                }
                mov = cfp.dic_to_mov(dic=mov_to_estimate)
                estimate = cfp.estimateCFP(mov=mov)
                producer.send(os.environ.get('KAFKA_TOPIC_CFP', 't_cfp'),value=estimate)

                count = {}
                for key, value in estimate.items():
                    count[key] = 1 if value else 0

                increment = {"totalCO2":estimate["co2"],
                            "countCO2": count['co2'],
                            "totalN2O":estimate["n2o"],
                            "countN2O": count['n2o'],
                            "totalCH4":estimate["ch4"],
                            "countCH4": count['ch4'],
                            "totalH2O":estimate["h2o"],
                            "countH2O": count['h2o'],
                            "totalPlastic":estimate["sup"],
                            "countPlastic":count['sup']}

                
                mov_to_estimate['date'] = datetime.datetime.strptime(mov_to_estimate['date']+' 00:00:00', '%Y-%m-%d %H:%M:%S')
                mov_to_estimate['date'] = timezone.localize(mov_to_estimate['date'])

                #
                ## USER TRANSACTIONS
                db = connect[connect.get_database()._Database__name][os.environ.get('MONGO_COLLECTION', 'AggregatedCfp')]

                # Add transaction for user and date
                db.update_one({"identifier":mov_to_estimate["user_id"],"date":mov_to_estimate["date"]},
                            {"$set":{"aggregationPeriodicity":"daily"},
                            "$inc":increment},
                            True)
                # Agregation by User Global (startDate to null)
                db.update_one({"identifier":mov_to_estimate["user_id"],"date":None},
                            {"$set":{"aggregationPeriodicity":None},
                            "$inc":increment},
                            True)
            
                #
                ## GLOBAL TRANSACTONS
                # Global by date
                db.update_one({"identifier":None,"date":mov_to_estimate["date"]},
                            {"$set":{"aggregationPeriodicity":"daily"},
                            "$inc":increment},
                            True)
                # Global total
                db.update_one({"identifier":None,"date":None},
                            {"$set":{"startDate":None,"aggregationPeriodicity":None},
                            "$inc":increment},
                            True)
                
            else:
                print("MESSAGE NOT ESTIMATE", message)

        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")


if __name__ == "__main__":
    main()


