# internet-scale-app
A Django web application based on microservices
# Project 2 Documentation
## Models
### User
  - string: username
  - string: first_name
  - string: last_name 
  - int: age
  - string: gender
  - proper email address: email_address
  - datetime: date_joined (auto created)
  - int: zipcode
  - string: password
### Pet
  - string: name
  - string: pet_type
  - string: description
  - decimal (3 decimal places): price
  - datetime: date_posted (auto created)
## Create
### User
 - link: api/v1/users/create
 - example:
    - POST   
  {
    username: "dw98"
    first_name: "Daniel"
    last_name: "Wang"
    age: 21
    gender: "M"
    email_address: "hw4ce@virginia.edu"
    zipcode: 22904
    password: "123456"
  }
### Pet
 - link: api/v1/pets/create
  - example:
    - POST
  {
    name: "Rocky"
    pet_type: "dog"
    description: "A good dog"
    price: 15.999
  }
## Read
### User
- link: api/v1/users/(\d+)/get_by_id
  - example:
   - GET api/v1/users/1/get_by_id    
### Pet
- link: api/v1/pets/(\d+)/get_by_id
  - example:
   - GET api/v1/users/1/get_by_id  
    
## Update
### User
- link: api/v1/users/(\d+)/update
  - example:
   - POST api/v1/users/1/update
  {
    username: "dw98"
  }
### Pet
- link: api/v1/pets/(\d+)/update
  - example:
   - POST api/v1/pets/1/update
  {
    name: "Bella"
  }
## Delete
### User
- link: api/v1/users/(\d+)/delete
  - example:
   - GET api/v1/users/1/delete
### Pet
- link: api/v1/pets/(\d+)/delete
  - example:
   - GET api/v1/pets/1/delete
