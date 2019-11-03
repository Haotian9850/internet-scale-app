from elasticsearch import Elasticsearch
import requests
import json 
import time


def get_es_client():
    es = Elasticsearch(["elasticsearch:9200"])
    for i in range(100):
        if not es.ping():
            print("Cannot establish a connection to elasticsearch host. Retrying....")
        else:
            break
        time.sleep(1)
    return es



'''
    @Returns;
        A list of pet object defined in es index mapping
'''
def search_pet_by_keyword(request):
    # internal, no need to check request method
    es = get_es_client()
    pets = []
    sorted_pets = []
    result = es.search(
        index="pets",
        body={
            "query": {
                    "multi_match" : {
                    "query": request.POST.get("keyword"),
                    "type": "best_fields",
                    "fields": ["name", "description", "pet_type"],
                    "tie_breaker": 0.3
                    }
                }
            }
    )
    for pet in result["hits"]["hits"]:
        pets.append({
            "pet_id": pet["_source"]["pet_id"],
            "name": pet["_source"]["name"],
            "description": pet["_source"]["description"],
            "pet_type": pet["_source"]["pet_type"],
            "price": pet["_source"]["price"],
            "views": pet["_source"]["views"]
        })
    for view in sorted([int(pet["views"]) for pet in pets], reverse=True):
        for pet in pets:
            if pet["views"] == view:
                sorted_pets.append(pet)
    return sorted_pets
    
