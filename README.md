# Portia: an exotic pet store
## Architecture
This project follows a 4-tier Django project architecture: HTML frontend + experience service APIs + entity / model APIs + backend database. Every tier lives in a separate Docker container, each of which is orchestrated by `docker-compose.yml`

### search layer
 - Container image: `tp33/django`
 - Container name: `batch`
 - Design
    - This container consumes from `kafka` and index messages into `elasticsearch` to support popularity-based pet searching by invoking a blocking script `app/search_indexer/search_indexer/main.py` 


### presentation layer
 - Container image: `tp33/django`
 - Container name: `presentation`
- This layer contains settings for cookie-based client-side sessions (which contains session-based authenticator):
    - Time out: 1200 seconds (20 minutes)
    - Will destroy all sessions after brower process is ended




### experience (application) layer
 - Container image: `tp33/django`
 - Container name: `exprience`
 - Django app name: `main`
 - API design
    - `test/get_all_pets`: returns a list of all pets in table `pets`. `GET` request only. No request body required
    - `test/get_pet_by_id`: returns a pet of specified `pet_id`. `POST` only. Request body:
        ```
        {
            "username": "hao",
            "id": 1
        }
        ```
        *Note: when a user is not logged in, `username` will be set to `"visitor"`* (implementation details, internal use only)
    - `test/get_pet_by_user`: get pets by `username`. `POST` only. Request body:
        ```
        {
            "username": "hao"
        }
    - `test/create_pet`: create a new pet object for authenticated user. `POST` request only. Request body:
        ```
        {
            "name": "cute dog",
            "pet_type": "dog",
            "description": "dog is human's best animal friend",
            "price": 299,
            "authenticator": "IFm1qp3t6SwR17VAk8tvWw==",
            "username": "hao"
        }
        ```
    - `test/search_pets`: return a list of pets matching search keyword. `POST` request only. Request body: 
        ```
        {
            "keyword": "dog"
        }
        ```
    - `test/login`: returns an authenticator if login is successful. `POST` request only
        ```
        {
            "username": "hao",
            "password": "123456"
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
            "password": "123456"
        }
        ```
    - `api/v1/users/(\d+)/get_by_id`: get user by `user_id`. `GET `request only. Request parameter:
        ```
        user_id=29
        ```
    - `api/v1/pets/get_by_user`: get pets by `username`. `POST` only. Request body:
        ```
        {
            "username": "hao"
        }
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
            "password": "123456"          # optional
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
            "authenticator": "IFm1qp3t6SwR17VAk8tvWw==",
            "username": "hao"
        }
        ```
    - `api/v1/pets/get_all_pets`: get a list of all pets
    - `api/v1/pets/(\d+)/get_by_id`: get pet by `pet_id`
    - `api/v1/pets/(\d+)/update`: update pet by its `pet_id`. `POST` only. Request body:
        ```
        {
            "name": "cute samoyed", # optional
            "pet_type": "dog",  # optional   
            "description": "samoyed is cute", # optional
            "price": 299,   # optional
            "date_posted": TIMESTAMP,   #optional
            "authenticator": "IFm1qp3t6SwR17VAk8tvWw==",
            "username": "hao"
        }
        ```
    - `api/v1/pets/(\d+)/delete`: delete pet by its `pet_id`. `POST` only. Request body:
        ```
        {
            "pet_id": 3,
            "username": "hao",
            "authenticator": "IFm1qp3t6SwR17VAk8tvWw=="
        }
        ```

    - `api/v1/login`: login a user. `POST` request only. If login is successful returns an `UTF-8` encoded 128-bit authenticator. Request body:
        ```
        {
            "username": hao,
            "password": "123456"
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
    - `api/v1/reset_password`: reset password for a user. `POST` only. The password resetting process consists of two sequential `POST` requests:
        ```
        {
            "reset": "no",
            "username": "hao"
        }
        ```
        This request will trigger an email being sent to user's registered email address containing an `authenticator`

        followed by:
        ```
        {
            "reset": "yes",
            "authenticator": "fh84o8/MtiFiwUF05J2gRA==",
            "new_password": 123456789
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