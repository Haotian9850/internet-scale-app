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
  
##Create

###User
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
###Pet
 - link: api/v1/pets/create
  - example:
    - POST
  {
    name: "Rocky"
    pet_type: "dog"
    description: "A good dog"
    price: 15.999
  }
    url('api/v1/users/(\d+)/get_by_id', views.get_user_by_id),
    url('api/v1/users/(\d+)/update', views.update_user),
    url('api/v1/users/(\d+)/delete', views.delete_user),
    url('api/v1/pets/create', views.create_pet),
    url('api/v1/pets/(\d+)/get_by_id', views.get_pet_by_id),
    url('api/v1/pets/(\d+)/update', views.update_pet),
    url('api/v1/pets/(\d+)/delete', views.delete_pet)

##Read
###User
- link: api/v1/users/(\d+)/get_by_id
  - example:
    - GET   
    
##Update

##Delete
  
