# Project 4 Changes and Updates

## New features since release `0.0.3`
### The following features are made available in project 4:
- Added cookie-based authentication mechanism in all 4 layers
- Added custom user login / logout / register functionalities in all 4 layers
- Added create listing (create pet) functionality in all 4 layers
- Added view pets for current user functionality in all 4 layers
- Added more unit / integration test cases in `presentation`, `experience` and `entity` layer
- Added more user stories
- Updated project documentation


### Portia: user stories (needs to be updated)
- As the seller, I want to inform the customer what type of animal does the pet belongs to
- As the seller, I want to update the information of the pet to let the customer know the most up-to-date condition of the pet
- As the seller, I want to request to cancel sales when the pet is no longer available
- As the customer, I want to see all the pets listed by all the sellers
- As the customer, I want to type and search about the pet I want
- As the customer, I want to change and update my profile to give my most up-to-date information to the seller
- As the customer, I want to delete my profile when I no longer want to shop on this website



### Deployment & Testing
#### Deployment
1. Ensure that a `mysql` container with a database named `cs4260` and a user `'www'@'%'` who is granted all privileges to `cs4260` and `test_cs4260` (the test database Django test `Client` will create later). Otherwise, `docker-compose up` will not bring up any container
2. Add `mysql` container to docker networks `backend` by running the following command:
    ```
    sudo docker network connect internet-scale-app_backend mysql
    ```
3. Run `sudo docker-compose up` in project root folder to bring up docker container `entity`, `experience` and `presentation`
4. Head to `localhost:8003/homepage` to access the project:
    - Click `[Check it out!]` button to view details for each pet
    - Type in the search bar and click `[Search]` to search for matching pets
    - Click `[Register]` to register as a new user
    - After registeration, new user will be redirected to a login page. Click `[Log in]` after filling in user information
    - After logging in, click `[Create a new pet!]` to create a new listing
    - After a new pet is created, user will be redirected to homepage. If logged in (session not expired), user can click `[My Pets ONLY]` to view only the pets he creates
    - Click `[Log out]` to log out

### Important facts
1. Session for each user will expire after 1200 seconds (20 minutes)
2. Session for each user will be flushed after browser (all browser process) is closed



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
- run the following command to run all tests (an new pet named `Rocky` will be added to database `cs4260`)
    ```
    cd /app/portia
    python manage.py test
    ```
