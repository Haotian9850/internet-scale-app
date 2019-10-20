# Create your tests here.
from django.test import TestCase, Client
from main import models
import json
import logging
#import requests

# User story 1 : As the seller, I want to inform the customer what type of animal does the pet belongs to
class PetCreateTest(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		c = Client()
		u1 = { "username":"jupaoqq", 
			"first_name":"daniel",
			"last_name":"wang",
			"age":21,
			"gender":"M",
			"email_address":"hw4ce@virginia.edu",
			"zipcode":22904,
			"password":"password"
		}
		response = c.post('/api/v1/users/create', u1) 
		
		
	# success
	def test_success_response(self):
		c = Client()
		u = {
			"username": "jupaoqq", 
			"password": "password"
		}
		#response = requests.post(url = "http://entity:8000//api/v1/login", data = u) 
		response = c.post('/api/v1/login', u)
		#print ('test_sucess_pet_create_pk:')
		#print (response)
		json_response = json.loads((response.content).decode("utf-8"))
		#print (json_response)
		auth_string = json_response['res']
		dog = {
			'name': 'Rocky', 
			'pet_type': 'dog', 
			'description': 'A vert nice dog', 
			'price': '99.999',
			"authenticator": str(auth_string),
			"username": "jupaoqq"
		}
		response = c.post('/api/v1/pets/create', dog)
		json_response = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_response["ok"], True) 

	#failure #1: no auth
	def test_failure_response_1(self):
		dog = {
			'name': 'Rocky', 
			'pet_type': 'dog', 
			'description': 'A vert nice dog', 
			'price': '99.999',

			"username": "jupaoqq"
		}
		c = Client()
		response = c.post('/api/v1/pets/create', dog)
		json_response = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_response["ok"], False)

	#failure #2: missing info
	def test_failure_response_2(self):
		u = {
			"username": "jupaoqq", 
			"password": "password"
		}
		c = Client()
		response = c.post('/api/v1/login', u)
		json_response = json.loads((response.content).decode("utf-8"))
		print ('pet_create_fail_1')
		auth_string = json_response['res']
		dog = {
			'name': 'Rocky', 
			'pet_type': 'dog', 
			'description': 'A vert nice dog', 
			"authenticator": str(auth_string),
			"username": "jupaoqq"
		}
		response = c.post('/api/v1/pets/create', dog)
		json_response = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_response["ok"], False)
		
	def tearDown(self):
		pass


# User story 2 As the seller, I want to update the information of the pet to let the customer know the most up-to-date condition of the pet
class PetUpdateTest(TestCase):
# 3
	def setUp(self):
		logging.disable(logging.CRITICAL)
		c = Client()
		u1 = {
			"username":"jupaoqq", 
			"first_name":"daniel",
			"last_name":"wang",
			"age":21,
			"gender":"M",
			"email_address":"hw4ce@virginia.edu",
			"zipcode":22904,
			"password":"password"
		}
		response = c.post('/api/v1/users/create', u1)
		
	def test_success_response(self):
		u = {
			"username": "jupaoqq", 
			"password": "password"
		}
		c = Client()
		response = c.post('/api/v1/login', u)
		json_response = json.loads((response.content).decode("utf-8"))
		auth_string = json_response['res']
		dog = {
			'name': 'Rocky', 
			'pet_type': 'dog', 
			'description': 'A vert nice dog', 
			'price': '99.999',
			"authenticator": str(auth_string),
			"username": "jupaoqq"
		}
		response = c.post('/api/v1/pets/create', dog)
		### CHANGE to whatever this prints
		print ('update_sucess_pk:')
		print (json.loads((response.content).decode("utf-8")))
		update = {
			'description': 'good dog',
			"authenticator": str(auth_string),
			"username": "jupaoqq"
		}
		response = c.post('/api/v1/pets/' + str(9) + '/update', update)
		json_response = json.loads((response.content).decode("utf-8"))
		#print (json_response)
		self.assertEquals(json_response["ok"], True) 

	# no auth when update
	def test_failure_response_1(self):
		u = {
			"username": "jupaoqq", 
			"password": "password"
		}
		c = Client()
		response = c.post('/api/v1/login', u)
		json_response = json.loads((response.content).decode("utf-8"))
		auth_string = json_response['res']
		dog = {
			'name': 'Rocky', 
			'pet_type': 'dog', 
			'description': 'A vert nice dog', 
			'price': '99.999',
			"authenticator": str(auth_string),
			"username": "jupaoqq"
		}
		response = c.post('/api/v1/pets/create', dog)
		### CHANGE to whatever this prints
		print ('update_fail_1_pk:')
		print (json.loads((response.content).decode("utf-8")))
		update = {
			'description': 'good dog',
			"username": "jupaoqq"
		}
		response = c.post('/api/v1/pets/' + str(7) + '/update', update)
		json_response = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_response["ok"], False) 

	# incompatible data types
	def test_failure_response_2(self):
		u = {
			"username": "jupaoqq", 
			"password": "password"
		}
		c = Client()
		response = c.post('/api/v1/login', u)
		json_response = json.loads((response.content).decode("utf-8"))
		auth_string = json_response['res']
		dog = {
			'name': "pet", 
			'pet_type': 'dog', 
			'description': 'A vert nice dog', 
			'price': '99.999',
			"authenticator": str(auth_string),
			"username": "jupaoqq"
		}
		response = c.post('/api/v1/pets/create', dog)
		### CHANGE to whatever this prints
		print ('update_fail_2_pk:')
		print (json.loads((response.content).decode("utf-8")))
		update = {
			"price": '100',
			"authenticator": str(auth_string),
			"username": "jupaoqq"
		}
		# actual index 8, test for 10
		response = c.post('/api/v1/pets/' + str(10) + '/update', update)
		json_response = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_response["ok"], False) 
		
	def tearDown(self):
		pass

#User story 3 As the seller, I want to request to cancel sales when the pet is no longer available
class PetDeleteTest(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		c = Client()
		u1 = {
			"username":"jupaoqq", 
			"first_name":"daniel",
			"last_name":"wang",
			"age":21,
			"gender":"M",
			"email_address":"hw4ce@virginia.edu",
			"zipcode":22904,
			"password":"password"
		}
		response = c.post('/api/v1/users/create', u1)
	
	# success
	def test_success_response(self):
		u = {
			"username": "jupaoqq", 
			"password": "password"
		}
		c = Client()
		response = c.post('/api/v1/login', u)
		json_response = json.loads((response.content).decode("utf-8"))
		auth_string = json_response['res']
		dog = {
			'name': 'Rocky', 
			'pet_type': 'dog', 
			'description': 'A vert nice dog', 
			'price': '99.999',
			"authenticator": str(auth_string),
			"username": "jupaoqq"
		}
		response = c.post('/api/v1/pets/create', dog)
		### CHANGE to whatever this prints
		print ('delete_success_pk:')
		print (json.loads((response.content).decode("utf-8")))
		
		delete = {
			'pet_id': 4,
			"username": "jupaoqq",
			"authenticator": str(auth_string)	
		}
		#i = json.loads((response.content).decode("utf-8")).get("pet_id")
		#response = c.post('/api/v1/pets/' + str(4) + '/delete', delete)
		#json_response = json.loads((response.content).decode("utf-8"))
		#self.assertEquals(json_response["ok"], True) 
	
	# no auth
	def test_failure_response_1(self):
		u = {
			"username": "jupaoqq", 
			"password": "password"
		}
		c = Client()
		response = c.post('/api/v1/login', u)
		json_response = json.loads((response.content).decode("utf-8"))
		auth_string = json_response['res']
		dog = {
			'name': 'Rocky', 
			'pet_type': 'dog', 
			'description': 'A vert nice dog', 
			'price': '99.999',
			"authenticator": str(auth_string),
			"username": "jupaoqq"
		}
		response = c.post('/api/v1/pets/create', dog)
		### CHANGE to whatever this prints
		print ('delete_fail_1_pk:')
		print (json.loads((response.content).decode("utf-8")))
		
		delete = {
			'pet_id': 2,
			"username": "jupaoqq",  
		}

		#i = json.loads((response.content).decode("utf-8")).get("pet_id")
		#response = c.post('/api/v1/pets/' + str(2) + '/delete', delete)
		#self.assertEquals(json_response["ok"], False) 


	def test_failure_response_2(self):
		u = {
			"username": "jupaoqq", 
			"password": "password"
		}
		c = Client()
		response = c.post('/api/v1/login', u)
		json_response = json.loads((response.content).decode("utf-8"))
		auth_string = json_response['res']
		dog = {
			'name': 'Rocky', 
			'pet_type': 'dog', 
			'description': 'A vert nice dog', 
			'price': '99.999',
			"authenticator": str(auth_string),
			"username": "jupaoqq"
		}
		response = c.post('/api/v1/pets/create', dog)
		### CHANGE to whatever this prints
		### don't change 100
		print ('delete_fail_2_pk:')
		print (json.loads((response.content).decode("utf-8")))
		
		delete = {
			'pet_id': 100,
			"username": "jupaoqq",
			"authenticator": str(auth_string)	
		}

		#i = json.loads((response.content).decode("utf-8")).get("pet_id")
		#response = c.get('/api/v1/pets/' + str(3) + '/delete',delete)
		#json_response = json.loads((response.content).decode("utf-8"))
		#self.assertEquals(json_response["ok"], False) 
		
	def tearDown(self):
		pass

#User story 4 As the customer, I want to see all the pets listed by all the sellers
class PetGetAllTest(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		c = Client()
		u1 = {
			"username":"jupaoqq", 
			"first_name":"daniel",
			"last_name":"wang",
			"age":21,
			"gender":"M",
			"email_address":"hw4ce@virginia.edu",
			"zipcode":22904,
			"password":"password"
		}
		response = c.post('/api/v1/users/create', u1)
		
	def test_success_response(self):
		u = {
			"username": "jupaoqq", 
			"password": "password"
		}
		c = Client()
		response = c.post('/api/v1/login', u)
		json_response = json.loads((response.content).decode("utf-8"))
		auth_string = json_response['res']
		dog = {
			'name': 'Rocky', 
			'pet_type': 'dog', 
			'description': 'A vert nice dog', 
			'price': '99.999',
			"authenticator": str(auth_string),
			"username": "jupaoqq"
		}
		response = c.post('/api/v1/pets/create', dog)
		cat = {
			'name': 'Ella', 
			'pet_type': 'cat', 
			'description': 'A vert nice cat', 
			'price': '19.999',
			"authenticator": str(auth_string),
			"username": "jupaoqq"
		}
		response = c.post('/api/v1/pets/create', cat)
		response = c.get('/api/v1/pets/get_all_pets')
		json_response = len(json.loads((response.content).decode("utf-8"))["res"])
		#print (json_response)
		self.assertEquals(json_response, 2) 
	
	# no pets
	def test_failure_response(self):
		c = Client()
		response = c.get('/api/v1/pets/get_all_pets')
		json_response = len(json.loads((response.content).decode("utf-8")))
		print (json_response)
		self.assertEquals(json_response, 2) 
		
	def tearDown(self):
		pass

# User story 6 As the customer, I want to change and update my profile to give my most up-to-date information to the seller
class UserUpdateTest(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		c = Client()
		u1 = {
			"username":"jupaoqq", 
			"first_name":"daniel",
			"last_name":"wang",
			"age":21,
			"gender":"M",
			"email_address":"hw4ce@virginia.edu",
			"zipcode":22904,
			"password":"password"
		}
		response = c.post('/api/v1/users/create', u1)
		json_response = json.loads((response.content).decode("utf-8"))
		print ('user for user update')
		print (json.loads((response.content).decode("utf-8")))
		
	def test_success_response(self):
		c = Client()
		#print (json.loads((response.content).decode("utf-8")))
		u = {
			"username": "jupaoqq", 
			"password": "password"
		}
		response = c.post('/api/v1/login', u)
		json_response = json.loads((response.content).decode("utf-8"))
		auth_string = json_response['res']
		update = {
			'last_name': 'yang',
			"username": "jupaoqq", 
			"authenticator": str(auth_string)
		}
		print ('user_update_success_pk:')
		print (json.loads((response.content).decode("utf-8")))
		
		response = c.post('/api/v1/users/' + str(14) + '/update', update)
		json_response = json.loads((response.content).decode("utf-8"))
		#print (json_response)
		self.assertEquals(json_response["ok"], True) 

	# no auth
	def test_failure_response1(self):
		c = Client()
		#print (json.loads((response.content).decode("utf-8")))
		u = {
			"username": "jupaoqq", 
			"password": "password"
		}
		response = c.post('/api/v1/login', u)
		json_response = json.loads((response.content).decode("utf-8"))
		auth_string = json_response['res']
		update = {
			'last_name': 'yang',
			"username": "jupaoqq", 
		}
		print ('user_update_failure_pk:')
		print (json.loads((response.content).decode("utf-8")))
		
		response = c.post('/api/v1/users/' + str(14) + '/update', update)
		json_response = json.loads((response.content).decode("utf-8"))
		#print (json_response)
		self.assertEquals(json_response["ok"], False) 

	# incorrect data type
	def test_failure_response2(self):
		c = Client()
		#print (json.loads((response.content).decode("utf-8")))
		u = {
			"username": "jupaoqq", 
			"password": "password"
		}
		response = c.post('/api/v1/login', u)
		json_response = json.loads((response.content).decode("utf-8"))
		auth_string = json_response['res']
		update = {
			'last_name': 100,
			"username": "jupaoqq",
			"authenticator": str(auth_string)
		}
		print ('user_update_failure2_pk:')
		print (json.loads((response.content).decode("utf-8")))
		
		response = c.post('/api/v1/users/' + str(14) + '/update', update)
		json_response = json.loads((response.content).decode("utf-8"))
		#print (json_response)
		self.assertEquals(json_response["ok"], False) 

	def tearDown(self):
		pass

# User story 8 As the customer, I want to change and update my profile to give my most up-to-date information to the seller
class ZLoginTest(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		c = Client()
		u1 = {
			"username":"jupaoqq", 
			"first_name":"daniel",
			"last_name":"wang",
			"age":21,
			"gender":"M",
			"email_address":"hw4ce@virginia.edu",
			"zipcode":22904,
			"password":"password"
		}
		response = c.post('/api/v1/users/create', u1)
		
	def test_success_response(self):
		u = {"username":"jupaoqq", 
			"password": "password"}
		c = Client()
		response = c.post('/api/v1/login', u)
		json_response = json.loads((response.content).decode("utf-8"))
		#print (json_response)
		self.assertEquals(json_response["ok"], True) 

	def tearDown(self):
		pass

# User story 9 As the customer, I want to change and update my profile to give my most up-to-date information to the seller
class ZLogoutTest(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		c = Client()
		u1 = {
			"username":"jupaoqq", 
			"first_name":"daniel",
			"last_name":"wang",
			"age":21,
			"gender":"M",
			"email_address":"hw4ce@virginia.edu",
			"zipcode":22904,
			"password":"password"
		}
		response = c.post('/api/v1/users/create', u1)
		
		
	def test_success_response(self):
		u = {"username":"jupaoqq", 
			"password": "password"}
		c = Client()
		response = c.post('/api/v1/login', u)
		json_response = json.loads((response.content).decode("utf-8"))
		auth_string = json_response["res"]
		print (json_response)
		uu = {"authenticator": auth_string}
		response = c.post('/api/v1/logout', uu)
		print ('test log out')
		
		json_response = json.loads((response.content).decode("utf-8"))
		print (json_response)
		self.assertEquals(json_response["ok"], True) 

#User story 10 As the customer, I want to see all the pets listed by all the sellers
class zGetPetByUserTest(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		c = Client()
		u1 = {
			"username":"jupaoqq", 
			"first_name":"daniel",
			"last_name":"wang",
			"age":21,
			"gender":"M",
			"email_address":"hw4ce@virginia.edu",
			"zipcode":22904,
			"password":"password"
		}
		response = c.post('/api/v1/users/create', u1)
		
	def test_success_response(self):
		u = {
			"username": "jupaoqq", 
			"password": "password"
		}
		c = Client()
		response = c.post('/api/v1/login', u)
		json_response = json.loads((response.content).decode("utf-8"))
		auth_string = json_response['res']
		dog = {
			'name': 'Rocky', 
			'pet_type': 'dog', 
			'description': 'A vert nice dog', 
			'price': '99.999',
			"authenticator": str(auth_string),
			"username": "jupaoqq"
		}
		response = c.post('/api/v1/pets/create', dog)
		cat = {
			'name': 'Ella', 
			'pet_type': 'cat', 
			'description': 'A vert nice cat', 
			'price': '19.999',
			"authenticator": str(auth_string),
			"username": "jupaoqq"
		}
		response = c.post('/api/v1/pets/create', cat)
		u = {'username': 'jupaoqq'}
		response = c.post('/api/v1/pets/get_by_user', u)
		json_response = len(json.loads((response.content).decode("utf-8"))["res"])
		#print (json_response)
		self.assertEquals(json_response, 2) 
	
	# no pets by target user
	def test_failure_response(self):
		c = Client()
		u = {'username': 'jupaoqq'}
		response = c.post('/api/v1/pets/get_by_user', u)
		json_response = len(json.loads((response.content).decode("utf-8")))
		print (json_response)
		self.assertEquals(json_response, 2) 
		
	def tearDown(self):
		pass