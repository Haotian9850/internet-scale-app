from kafka import KafkaConsumer
from kafka.errors import KafkaError

from elasticsearch import Elasticsearch
import logging 
import time 
import threading


es_id_mapping


def get_es_client():
    es = Elasticsearch(["elasticsearch:9200"])
    if not es.ping():
        print("Cannot establish a connection to elasticsearch host.")
    return es


def init(index_name, index_mapping):
    es = get_es_client()
    if not check_existing_index(es, index_name):
        return es.indices.create(
            index=index_name,
            body=index_mapping
        )
    

def check_existing_index(es, index_name):
    return es.indices.exists(index_name)


# check for pet existence first
'''
def index_pet(message, index_name):
    es = get_es_client()
    return es.index(
        index=index_name,
        body=parse_pet(message)
    )
'''


def print_consumer_topic():  
    consumer = KafkaConsumer(
        "new-pet-topic",
        group_id=None,
        auto_offset_reset="earliest", 
        bootstrap_servers=["kafka:9092"]
    ) 
    for message in consumer:
        print("{}:{}:{}: key={} value={}".format(
            message.topic,
            message.partition,
            message.offset,
            message.key,
            message.value
        ))  # will wait for next kafka message



    