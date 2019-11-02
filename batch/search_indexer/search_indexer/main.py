from services.elasticsearch_service import get_es_client, init, update_pet_view, index_pet
from services.logging_service import parse_pet_log


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

