# Portia: an exotic pet store
## Architecture
This project follows a 4-tire Django project architecture: HTML frontend + experience service APIs + entity / model APIs + backend database. Every tier lives in a separate Docker container, each of which is orchestrated by `docker-compose.yml`
### HTML frontend
 - homepage
 - pet detail page

### experience service APIs
 - Explnanation: the experience layer will invoke entity APIs via HTTP and recieve JSON respones. Similarly, it will provide HTTP / JSON APIs to the HTML templates
 - Container image: `tp33/django`
 - Container name: data-service
 - API design
    - Homepage: `get_pets()`: return a list of all pets in table `pets`
    - Homepage: `search_pet()`: return a list of pets matching search keyword
    - Homepage: `sort()`: return a list of pets sorted by sorting keyword (such as `price` and `date`)
    - Pet detail page: `get_pet_by_id()`: return details of a pet by its `pet_id`

### entity / model APIs
 - Container image: `tp33/django`
 - Container name: web
 - API design (only exposed to container `data_service`)
    - `api/v1/users/create`: create a new user
    - `api/v1/users/(\d+)/get_by_id`: get user by `user_id`
    - `api/v1/users/(\d+)/update`: update a user by its `user_id`
    - `api/v1/users/(\d+)/delete`: delete user by its `user_id`
    - `api/v1/pets/create`: create a new pet
    - `api/v1/pets/get_all_pets`: get a list of all pets
    - `api/v1/pets/(\d+)/get_by_id`: get pet by `pet_id`
    - `api/v1/pets/(\d+)/update`: update pet by its `pet_id`
    - `api/v1/pets/(\d+)/delete`: delete pet by its `pet_id`

### backend database
 - Container image: `mysql:latest`
 - Container name: `mysql`
 - Run command: `sudo docker run --name mysql -d -e MYSQL_ROOT_PASSWORD='$3cureUS' -v /mnt/documents-local/CS4260/internet-scale-app/db:/var/lib/mysql  mysql:latest`
 - Network command: `sudo docker network connect internet-scale-app_backend mysql`


## Common gotchas
 ### DB container configuration
 - Container `web` and requires a mysql container with username `'www'@'%'` and password `$cureUS` and a database named `cs4260` set up. Otherwise, docker compose will not bring up any contiainer. 
 - `requests` module need to be installed via `pip` in container `data_service` by running `pip install requests` (can be automated using a script later)