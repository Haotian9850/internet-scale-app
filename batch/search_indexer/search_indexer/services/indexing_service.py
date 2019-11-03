from kafka import KafkaConsumer
from kafka.errors import KafkaError
from .elasticsearch_service import get_es_client, ingest_pet, update_pet_view
from .logging_service import log_pet_views, parse_pet_log


import json
import time
import os
from datetime import datetime


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
    os.system("touch index_pet_called")
    #time.sleep(60)  # wait for kafka and elasticsearch to be ready
    while os.system("ping -c 1 kafka") != 0:
        time.sleep(60)
    os.system("touch start_index")
    consumer = KafkaConsumer(
        group_id="pet-indexer",
        auto_offset_reset="earliest", 
        bootstrap_servers=["kafka:9092"]
    ) 
    consumer.subscribe(
        ["new-pet", "pet-view"]
    )
    # TODO: change to non-blocking in production (?) + add exception handling
    while True:
        for msg in consumer:
            os.system("touch start_consume")
            if msg.topic == "new-pet":
                ingest_pet(
                    es,
                    index_name,
                    json.loads(msg.value.decode("utf-8"))
                )
            if msg.topic == "pet-view":
                log_pet_views(json.loads(msg.value.decode("utf-8")))
                update_pet_view(es, index_name, parse_pet_log())
                
    


    

    