from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
from kafka.errors import KafkaError



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

print_consumer_topic()