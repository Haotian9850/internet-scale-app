from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json
import time

import os

#from logging_service import parse_pet_log


def get_es_client():
    es = Elasticsearch(["elasticsearch:9200"])
    for i in range(100):
        if not es.ping():
            print("Cannot establish a connection to elasticsearch host. Retrying....")
        else:
            break
        time.sleep(1)
    return es


def init(index_name, index_mapping, es):
    if not check_existing_index(es, index_name):
        print("Creating elasticsearch index {}".format(index_name))
        return es.indices.create(
            index=index_name,
            body=index_mapping
        )


def check_existing_index(es, index_name):
    return es.indices.exists(index_name)
    

def update_pet_view(es, index_name, views):
    for pet_id in views.keys():
        update_view(es, index_name, pet_id, views[pet_id])


def update_view(es, index_name, pet_id, new_view):
    es.update(
        index=index_name,
        id=pet_id,
        body={
            "script": "ctx._source.views={}".format(new_view)
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
            "pet_id": pet["pet_id"],
            "views": 0
        }
    )


'''
ingest_pet(
    get_es_client(),
    "pets",
    {
        "name": "test",
        "pet_type": "dog",
        "description": "Des",
        "price": 123,
        "pet_id": 29
    }
)
'''

'''
update_pet_view(
    get_es_client(),
    "pets",
    parse_pet_log()
)
'''


