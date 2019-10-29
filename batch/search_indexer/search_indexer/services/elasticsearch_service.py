from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
from kafka.errors import KafkaError


INDEX_NAME = "pets"
INDEX_MAPPING = {
    "settings" :{
        "number_of_shards" : 1
    },
    "mappings" : {
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


def update_pet_view(views, index_name, es):
    for pet_id in views.keys():
        es.update(
            index=index_name,
            id=views[pet_id],
            body={
                "script": "ctx._source.views += 1"
            }
        )
    

def ingest_new_pet(es, index_name, pet):
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



if __name__ == "__main__":
    pet = {
        "name": "test_pet",
        "pet_type": "dog",
        "description": "test description",
        "price": 123,
        "pet_id": 15,
        "views": 0
    }
    init(INDEX_NAME, INDEX_MAPPING, get_es_client())
    ingest_new_pet(get_es_client(), INDEX_NAME, pet)
    # print_consumer_topic()