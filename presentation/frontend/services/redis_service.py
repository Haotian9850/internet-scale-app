import redis
import json

def get_redis_client(host="redis", port=6379, db=0):
    return redis.Redis(
        host,
        port,
        db
    )

def insert(client, pet_id, pet_details):
    return client.set(
        pet_id,
        json.loads(pet_details)
    )
    

def look_up(client, pet_id):
    if client.exists(pet_id):
        return False
    return client.get(pet_id)