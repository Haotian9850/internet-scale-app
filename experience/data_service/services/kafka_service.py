from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import json
import time
import logging

# TODO: switch back to async in production 

def send_new_pet(request):
    producer = KafkaProducer(bootstrap_servers=["kafka:9092"])
    try:
        future = producer.send(
            "new-pet-topic",
            json.dumps(
                {
                    "name": request.POST.get("name"),
                    "pet_type": request.POST.get("pet_type"),
                    "description": request.POST.get("description"),
                    "price": request.POST.get("price"),
                    "authenticator": request.POST.get("authenticator"),
                    "username": request.POST.get("username")
                }
            ).encode("utf-8")
        )
        result = future.get(timeout = 60)
        return result is not None   # confirms kafka queuing
    except KafkaError:
        return False
        


'''
def print_consumer_topic():
    consumer = KafkaConsumer(
        "new-pet-topic",
        group_id=None,
        auto_offset_reset="earliest", 
        bootstrap_servers=["kafka:9092"]
    )
    for message in consumer:
        #print(json.loads((message.value).decode("utf-8")))
        print(message)

#send_new_pet()
'''

#time.sleep(20)