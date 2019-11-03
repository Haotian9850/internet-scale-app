from services.elasticsearch_service import get_es_client, init
from services.indexing_service import index_pet
import os
import time


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
                "pet_id" : { "type" : "integer" }
            } 
    }
}



if __name__ == "__main__":
    es = get_es_client()
    init(INDEX_NAME, INDEX_MAPPING, es)

    print("indexing pets....")
    index_pet(es, INDEX_NAME)

