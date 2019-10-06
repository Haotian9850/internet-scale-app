# Project 3 Changes and Updates

## New features since release `0.0.2`
### The following features are added in project 3:
- Added new `experience` and `presentation` layer in independent docker containers
- Added pet data services in `experience` layer
- Added frontend templates in `presentation` layer including a site homepage, pet detail page and a search result page
- Updated project design doc `project-description.md`
- Added unit and model test cases for `Pet` and `User` in both `experience` and `presentation` layer
- Added user stories 
- Updated `docker-compose.yml` to accomodate new containers and docker networks
- Updated `fixtures.json`

### Portia: user stories
- As the seller, I want to inform the customer what type of animal does the pet belongs to
- As the seller, I want to update the information of the pet to let the customer know the most up-to-date condition of the pet
- As the seller, I want to request to cancel sales when the pet is no longer available
- As the customer, I want to sort the listings of pets by the price from lowest to highest
- As the customer, I want to type and search about the pet I want

### Deployment & Testing
#### Deployment
1. Ensure that a `mysql` container with a database named `cs4260` and a user `'www'@'%'` who is granted all privileges to `cs4260` and `test_cs4260` (the test database Django test `Client` will create later) 
2. Add `mysql` container to docker networks `backend` by running the following command:
    ```
    sudo docker network connect internet-scale-app_backend mysql
    ```
3. Run `sudo docker-compose up` in project root folder to bring up docker container `entity`, `experience` and `presentation`
4. Head to `localhost:8003/homepage` to access the project:
    - Click `[Check it out!]` button to view details for each pet
    - Type in the search bar and click `[Search]` to search for matching pets

#### Testing
1. Testing in `entity` (model layer)
- ssh into container `entity` by running the following command:
    ```
    sudo docker exec -it entity /bin/bash
    ```
- run the following command to run all tests
    ```
    cd /app/portia
    python manage.py test
    ```
2. Testing in `experience` (experience layer)
- ssh into container `experience` by running the following command:
    ```
    sudo docker exec -it experience /bin/bash
    ```
- run the following command to run all tests
    ```
    cd /app/portia
    python manage.py test
    ```