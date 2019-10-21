# Project 4 Changes and Updates

## New features since release `0.0.3`
### The following features are made available in project 4:
- Added cookie-based authentication mechanism across all 4 layers
- Added custom user login / logout / register functionalities across all 4 layers
- Added create listing (create pet) functionality across all 4 layers
- Added view pets for current user functionality across all 4 layers
- Added **password recovery** feature across all 4 layers
- Added more unit / integration test cases in `entity` layer
- Added more user stories
- Updated project doc


### Portia: user stories
1. As the seller, I want to inform the customer what type of animal does the pet belongs to
2. As the seller, I want to update the information of the pet to let the customer know the most up-to-date condition of the pet
3. As the seller, I want to request to cancel sales when the pet is no longer available
4. As the customer, I want to see all the pets listed by all the sellers
5. As the customer, I want to type and search about the pet I want
6. As the customer, I want to change and update my profile to give my most up-to-date information to the seller
7. As the seller, I want to be able to log in with my account, so I can ensure nobody else else can edit information of my pets without my permission
8. As the seller, I want to be able to log out with my account. If I log in to the website in a computer in public, I want to ensure nobody else can use my account after I leave and am no longer using that computer
9. As the customer, I want to see all pets specified by a specific seller because I really all the pets in his/her inventory and want to follow that seller



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
    - Click `[Forget your password?]` to reset password through email
        - Since our team does not have a email service (real email services like `Mailchimp` are generally subscription-based paid services), so we opted for Django's build-in `EMAIL_BACKEND = django.core.mail.backends.filebased.EmailBackend`, which will redirect all emails to a local file system. Currently, all emails sent will be redirected to `/app/portia/emails` in the `entity` container
        - **Note: in a production environment (where a real email service is available), making this feature live only requires changing a few settings in `settings.py` such as  `EMAIL_HOST`, `EMAIL_PORT` and `EMAIL_PASSWORD`** 
    - Go to `/app/portia/emails` to view password recovery email. Follow the link in email to reset password. If password reset is successful, user will be redirected to login page
    - After logging in, click `[Create a new pet!]` to create a new listing
    - After a new pet is created, user will be redirected to homepage. If logged in (session not expired), user can click `[My Pets ONLY]` to view only the pets he creates
    - Click `[Log out]` to log out

### Important facts
1. Session for each user will expire after 1200 seconds (20 minutes)
2. Session for each user will be flushed after browser (all browser processes) is closed




### Testing
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

