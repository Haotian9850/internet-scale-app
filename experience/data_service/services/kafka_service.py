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
    "pet_id": 15
}

view = {
    "username": hao
    "pet_id": 6
}
'''

def get_kafka_producer():
    return KafkaProducer(bootstrap_servers=["kafka:9092"])



def send_pet_view(producer, view):
    try:
        future = producer.send(
            "pet-view",
            json.dumps(
                {
                    "username": view.get("username"),
                    "pet_id": view.get("pet_id")
                }
            ).encode("utf-8")
        )
        result = future.get(timeout = 60)
        return result is not None
    except KafkaError:
        return False
    




def send_new_pet(producer, pet):
    try:
        future = producer.send(
            "new-pet",
            json.dumps(
                {
                    "name": pet["name"][0],
                    "pet_type": pet["pet_type"][0],
                    "description": pet["description"][0],
                    "price": pet["price"][0],
                    "pet_id": pet["pet_id"]
                }
            ).encode("utf-8")
        )
        result = future.get(timeout = 60)
        return result is not None   # confirms kafka queuing
    except KafkaError:
        return False
        

'''
send_new_pet(
    get_kafka_producer(),
    {
        "name": "test5",
        "pet_type": "dog",
        "description": "Des",
        "price": 123,
        "pet_id": 36
    }
)
'''

