# Portia: an exotic pet store
## Architecture
This project follows a 4-tier Django project architecture: HTML frontend + experience service APIs + entity / model APIs + backend database. Every tier lives in a separate Docker container, each of which is orchestrated by `docker-compose.yml`

### presentation layer
 - Container image: `tp33/django`
 - Container name: `presentation`
 - Django app name: `homepage`, `pet_details`
 - Template hierarchy:
    - base view (header + footer, contains search bar)
        - Homepage
            - component to list all pets / list search result
        - Pet detail page: single component

### experience (application) layer
 - Container image: `tp33/django`
 - Container name: `exprience`
 - Django app name: `main`
 - API design
    - `test/get_all_pets`: returns a list of all pets in table `pets`. `GET` request only. No request body required
    - `test/search_pets`: return a list of pets matching search keyword. `POST` request only. Request body: 
        ```
        {
            "keyword": "dog"
        }
        ```
    - `test/sort_pets`: returns a list of pets sorted by specified sorting criteria. `POST` request only. Request body: 
        ```
        {
            "sort_by": "name"
        }
        ```
    - `test/login`: returns an authenticator if login is successful. `POST` request only
        ```
        {
            "username": hao,
            "password": 123456
        }
        ```
    - `test/logout`: log out a user by deleting its authenticator. `POST` request only. Request body:
        ```
        {
            "authenticator": "sAc0gFXexFLPdL4RKuUXBw=="
        }
        ```



### entity layer
 - Container image: `tp33/django`
 - Container name: `entity`
 - API design (only exposed to container `data_service`)
    - `api/v1/users/create`: create a new user. `POST` request only. Request body: 
        ```
        {
            "username": "Tiger2016",
            "first_name": "Tiger",
            "last_name": "Wu",
            "email_address": "tiger2016@gmail.com",     # must be well-formed email address
            "age": 21,
            "gender": "Male",
            "zipcode": 22904,
            "password": 123456  # currently unencrypted
        }
        ```
    - `api/v1/users/(\d+)/get_by_id`: get user by `user_id`. `GET `request only. Request parameter:
        ```
        user_id=29
        ```
    - `api/v1/users/(\d+)/update`: update a user by its `user_id`. `POST` request only. Request body (`/(\d+)/` is `user_id`):
        ```
        {
            "username": "Tiger2016",    # optional
            "first_name": "Tiger",      # optional
            "last_name": "Wu",          # optional
            "email_address": "tiger2016@gmail.com",     # optional
            "age": 21,                  # optional
            "gender": "Male",           # optional
            "zipcode": 22904,           # optional
            "password": 123456          # optional
        }
        ```
    - `api/v1/users/(\d+)/delete`: delete user by its `user_id`. `GET` request only.
    - `api/v1/pets/create`: create a new pet. `POST` only. Request body:
        ```
        {
            "name": "cute dog",
            "pet_type": "dog",
            "description": "dog is human's best animal friend",
            "price": 299,
            "date_posted": TIMESTAMP,
            "authenticator": "IFm1qp3t6SwR17VAk8tvWw=="
        }
        ```
    - `api/v1/pets/get_all_pets`: get a list of all pets
    - `api/v1/pets/(\d+)/get_by_id`: get pet by `pet_id`
    - `api/v1/pets/(\d+)/update`: update pet by its `pet_id`. `POST` only. Request body:
        ```
        {
            "name": "cute dog", # optional
            "pet_type": "dog",  # optional   
            "description": "dog is human's best animal friend", # optional
            "price": 299,   # optional
            "date_posted": TIMESTAMP,   #optional
            "authenticator": "IFm1qp3t6SwR17VAk8tvWw=="
        }
        ```
    - `api/v1/pets/(\d+)/delete`: delete pet by its `pet_id`
    - `api/v1/login`: login a user. `POST` request only. If login is successful returns an `UTF-8` encoded 128-bit authenticator. Request body:
        ```
        {
            "username": hao,
            "password": 123456
        }
        ```
        Returns:
        ```
        {
            "ok": true, 
            "res": "sAc0gFXexFLPdL4RKuUXBw=="
        }
        ```
    - `api/v1/logout`: logout a user by deleting its authenticator. `POST` request only. Request body:
        ```
        {
            "authenticator": "IFm1qp3t6SwR17VAk8tvWw=="
        }
        ```


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
 - Container `web` and requires a mysql container with username `'www'@'%'` and password `$cureUS` and a database named `cs4260` set up. Otherwise, docker compose will not bring up any containers. 