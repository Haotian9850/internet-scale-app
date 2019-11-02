from kafka import KafkaConsumer
from kafka.errors import KafkaError
from elasticsearch_service import get_es_client, ingest_pet, update_pet_view
from logging_service import log_pet_views

import json
import time


def index_pet(es, index_name):  
    consumer = KafkaConsumer(
        ["new-pet", "pet-view"],
        group_id=None,
        auto_offset_reset="earliest", 
        bootstrap_servers=["kafka:9092"]
    ) 
    # TODO: change to non-blocking in production (?)
    while True:
        msg = consumer.poll(1000)   # timeout: 1000ms
        if msg is None:
            continue
        if msg.error():
            print("Kafka consumer error: {}".format(msg.error()))
            continue
        if msg.topic() == "new-pet":
            ingest_pet(
                es,
                index_name,
                {
                    "name": msg.value.get("name"),
                    "pet_type": msg.value.get("pet_type"),
                    "description": msg.value.get("description"),
                    "price": msg.value.get("price"),
                    "id": msg.value.get("pet_id")
                }
            )
        if msg.topic() == "pet-view":


    '''
    for message in consumer:
        pet = json.loads(message.value.decode("utf-8"))
        if pet["views"] == 0:
            ingest_pet(es, index_name, {
                "name": pet["name"],
                "pet_type": pet["pet_type"],
                "description": pet["description"],
                "price": pet["price"],
                "pet_id": pet["pet_id"]
            })
            print("{}:{}:{}: key={} value={}".format(
                message.topic,
                message.partition,
                message.offset,
                message.key,
                message.value
            ))  # will wait for next kafka message (will hold)
    '''