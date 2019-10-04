# Portia: an exotic pet store
## Architecture
This project follows a 4-tire Django project architecture: HTML frontend + experience service APIs + entity / model APIs + backend database. Every tier lives in a separate Docker container, each of which is orchestrated by `docker-compose.yml`

### presentation layer
 - Container image: `tp33/django`
 - Container name: `presentation`
 - Django app name: `main`
 - Template design:
    - Homepage
    - Pet detail page

### experience (application) layer
 - Container image: `tp33/django`
 - Container name: `exprience`
 - Django app name: `main`
 - API design
    - Homepage: `get_pets()`: return a list of all pets in table `pets`
    - Homepage: `search_pet()`: return a list of pets matching search keyword
    - Homepage: `sort()`: return a list of pets sorted by sorting keyword (such as `price` and `date`)
    - Pet detail page: `get_pet_by_id()`: return details of a pet by its `pet_id`

### entity layer
 - Container image: `tp33/django`
 - Container name: `entity`
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

### data layer
 - Container image: `mysql:latest`
 - Container name: `mysql`
 - Django app name: `main`
 - Run command: `sudo docker run --name mysql -d -e MYSQL_ROOT_PASSWORD='$3cureUS' -v /mnt/documents-local/CS4260/internet-scale-app/db:/var/lib/mysql  mysql:latest`
 - SSH into container `mysql`: `docker exec -it mysql /bin/bash`
 - Get in SQL shell: `mysql -uroot -p'$3cureUS'`
 - Network command: `sudo docker network connect internet-scale-app_backend mysql`


## Common gotchas
 ### DB container configuration
 - Container `web` and requires a mysql container with username `'www'@'%'` and password `$cureUS` and a database named `cs4260` set up. Otherwise, docker compose will not bring up any contiainer. 