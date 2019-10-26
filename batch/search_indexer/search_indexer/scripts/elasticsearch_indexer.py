from kafka import KafkaConsumer
from kafka.errors import KafkaError

from elasticsearch import Elasticsearch
import logging 
import time 
import threading



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



def index_new_pet():
    es = Elasticsearch(["elasticsearch"])
    
