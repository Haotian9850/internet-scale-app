import redis
import json

def get_redis_client(host="redis", port=6379, db=0):
    return redis.Redis(
        host,
        port,
        db
    )

def insert_cache(client, pet_id, pet_details):
    return client.set(
        pet_id,
        json.dumps(pet_details)
    )
    

def look_up_cache(client, pet_id):
    if client.exists(pet_id):
        return True, client.get(pet_id)
    return False, "empty"