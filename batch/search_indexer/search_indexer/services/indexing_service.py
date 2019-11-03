from kafka import KafkaConsumer
from kafka.errors import KafkaError
from .elasticsearch_service import get_es_client, ingest_pet, update_pet_view
from .logging_service import log_pet_views


import json
import time
import os


'''
Kafka msg schema:
new-pet:
    {
        "name": cute samoyed,
        "pet_type": dog,
        "description": samoyeds are cute dogs,
        "price": 213,
        "id": 6
    }
pet-view:
    {
        "username": hao,
        "pet_id": 6
    }
'''
def index_pet(es, index_name):  
    time.sleep(60)  # wait for kafka and elasticsearch to be ready
    consumer = KafkaConsumer(
        group_id=None,
        auto_offset_reset="earliest", 
        bootstrap_servers=["kafka:9092"]
    ) 
    consumer.subscribe(
        ["new-pet", "pet-view"]
    )
    # TODO: change to non-blocking in production (?) + add exception handling
    os.system("touch start")
    while True:
        for msg in consumer:
            if msg.topic == "new-pet":
                ingest_pet(
                    es,
                    index_name,
                    json.loads(msg.value.decode("utf-8"))
                )
            if msg.topic == "pet-view":
                log_pet_views(json.loads(msg.value.decode("utf-8")))
    



    

    