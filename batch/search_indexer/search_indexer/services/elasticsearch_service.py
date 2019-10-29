from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json


INDEX_NAME = "pets"
INDEX_MAPPING = {
    "settings": {
        "number_of_shards" : 1
    },
    "mappings": {
            "properties": {
                "name" : { "type" : "text" },
                "pet_type" : { "type" : "text" },
                "description" : { "type" : "text" },
                "price" : { "type" : "double" },
                "views" : { "type" : "long" }
            } 
    }
}



def get_es_client():
    es = Elasticsearch(["elasticsearch:9200"])
    if not es.ping():
        print("Cannot establish a connection to elasticsearch host.")
    return es


def init(index_name, index_mapping, es):
    if not check_existing_index(es, index_name):
        return es.indices.create(
            index=index_name,
            body=index_mapping
        )


def check_existing_index(es, index_name):
    return es.indices.exists(index_name)
    

def update_pet_view(es, index_name, views):
    for pet_id in views.keys():
        update_view(es, index_name, pet_id, views["pet_id"])


def update_view(es, index_name, pet_id, new_view):
    es.update(
        index=INDEX_NAME,
        id=pet_id,
        body={
            "script": "ctx._source.visits={}".format(new_view)
        }
    )



def ingest_pet(es, index_name, pet):
    return es.index(
        index=index_name,
        id=pet["pet_id"],
        body={
            "name": pet["name"],
            "pet_type": pet["pet_type"],
            "description": pet["description"],
            "price": pet["price"],
            "views": pet["views"]
        }
    )


def ingest_new_pet(es, index_name):  
    consumer = KafkaConsumer(
        "new-pet-topic",
        group_id=None,
        auto_offset_reset="earliest", 
        bootstrap_servers=["kafka:9092"]
    ) 
    for message in consumer:
        pet = json.loads(message.value.decode("utf-8"))
        ingest_pet(es, index_name, {
            "name": pet["name"],
            "pet_type": pet["pet_type"],
            "description": pet["description"],
            "price": pet["price"],
            "pet_id": pet["pet_id"],
            "views": pet["views"]
        })
        print("{}:{}:{}: key={} value={}".format(
            message.topic,
            message.partition,
            message.offset,
            message.key,
            message.value
        ))  # will wait for next kafka message (will hold)



if __name__ == "__main__":
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
    '''
    es = get_es_client()
    ingest_new_pet(get_es_client(), INDEX_NAME, pet)
    update_pet_view(get_es_client(), INDEX_NAME, 15, 43)
    '''

    ingest_new_pet(get_es_client(), INDEX_NAME)