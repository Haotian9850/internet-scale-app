from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import json
import time
import logging

# TODO: switch back to async in production 

# elasticsearch index schema
'''
pet = {
    "name": "test_pet",
    "pet_type": "dog",
    "description": "test description",
    "price": 123,
    "pet_id": 15,
    "views": 0
}
'''



def send_new_pet(pet):
    producer = KafkaProducer(bootstrap_servers=["kafka:9092"])
    try:
        future = producer.send(
            "new-pet-topic",
            json.dumps(
                {
                    "name": pet.get("name")[0],
                    "pet_type": pet.get("pet_type")[0],
                    "description": pet.get("description")[0],
                    "price": pet.get("price")[0],
                    "pet_id": pet.get("pet_id")[0],
                    "views": 0
                }
            ).encode("utf-8")
        )
        result = future.get(timeout = 60)
        return result is not None   # confirms kafka queuing
    except KafkaError:
        return False
        