from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from main import models
import json
import logging

# User story 1 : As the seller, I want to inform the customer what type of animal does the pet belongs to
class PetCreateTest(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		pass
		
	def test_success_response(self):
		dog = {'name': 'Rocky', 'pet_type': 'dog', 'description': 'A vert nice dog', 'price': '99.999'}
		c = Client()
		response = c.post('/api/v1/pets/create', dog)
		json_response = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_response["ok"], True) 

	def test_failure_response(self):
		dog = {'pet_type': 'dog', 'description': 'A vert nice dog', 'price': '99.999'}
		c = Client()
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
		pass
		
	def test_success_response(self):
		dog = {'name': 'Rocky', 'pet_type': 'dog', 'description': 'A vert nice dog', 'price': '99.999'}
		c = Client()
		response = c.post('/api/v1/pets/create', dog)
		#print (json.loads((response.content).decode("utf-8")))
		update = {'description': 'good dog'}
		response = c.post('/api/v1/pets/' + str(7) + '/update', update)
		json_response = json.loads((response.content).decode("utf-8"))
		#print (json_response)
		self.assertEquals(json_response["ok"], True) 

	def test_failure_response(self):
		dog = {'name': 'Rocky', 'pet_type': 'dog', 'description': 'A vert nice dog', 'price': '99.999'}
		c = Client()
		response = c.post('/api/v1/pets/create', dog)
		update = {'description': 100}
		response = c.post('/api/v1/pets/' + str(8) + '/update', update)
		json_response = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_response["ok"], False) 
		
	def tearDown(self):
		pass

#User story 3 As the seller, I want to request to cancel sales when the pet is no longer available
class PetDeleteTest(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		pass
		
	def test_success_response(self):
		dog = {'name': 'Rocky', 'pet_type': 'dog', 'description': 'A vert nice dog', 'price': '99.999'}
		c = Client()
		response = c.post('/api/v1/pets/create', dog)
		#i = json.loads((response.content).decode("utf-8")).get("pet_id")
		response = c.get('/api/v1/pets/' + str(3) + '/delete')
		json_response = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_response["ok"], True) 
	
	def test_failure_response(self):
		dog = {'name': 'Rocky', 'pet_type': 'dog', 'description': 'A vert nice dog', 'price': '99.999'}
		c = Client()
		response = c.post('/api/v1/pets/create', dog)
		#i = json.loads((response.content).decode("utf-8")).get("pet_id")
		response = c.get('/api/v1/pets/' + str(4) + '/delete')
		json_response = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_response["ok"], False) 
		
	def tearDown(self):
		pass

#User story 4 As the customer, I want to see all the pets listed by all the sellers
class PetGetAllTest(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		pass
		
	def test_success_response(self):
		dog = {'name': 'Rocky', 'pet_type': 'dog', 'description': 'A vert nice dog', 'price': '99.999'}
		c = Client()
		response = c.post('/api/v1/pets/create', dog)
		cat = {'name': 'Charlie', 'pet_type': 'cat', 'description': 'A vert nice cat', 'price': '89.999'}
		response = c.post('/api/v1/pets/create', cat)
		response = c.get('/api/v1/pets/get_all_pets')
		json_response = len(json.loads((response.content).decode("utf-8"))["res"])
		#print (json_response)
		self.assertEquals(json_response, 2) 
	
	def test_failure_response(self):
		c = Client()
		response = c.get('/api/v1/pets/get_all_pets')
		json_response = len(json.loads((response.content).decode("utf-8")))
		print (json_response)
		self.assertEquals(json_response, 0	) 
		
	def tearDown(self):
		pass

# User story 6 As the customer, I want to change and update my profile to give my most up-to-date information to the seller
class UserUpdateTest(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		pass
		
	def test_success_response(self):
		u = {"username":"jupaoqq", 
			"first_name":"daniel",
			"last_name":"wang",
			"age":21,
			"gender":"M",
			"email_address":"hw4ce@virginia.edu",
			"zipcode":22904,
			"password":"gshbdh"}
		c = Client()
		response = c.post('/api/v1/users/create', u)
		#print (json.loads((response.content).decode("utf-8")))
		update = {'last_name': 'yang'}
		response = c.post('/api/v1/users/' + str(2) + '/update', update)
		json_response = json.loads((response.content).decode("utf-8"))
		#print (json_response)
		self.assertEquals(json_response["ok"], True) 

	def tearDown(self):
		pass

# User story 7 As the customer, I want to change and update my profile to give my most up-to-date information to the seller
class UserDeleteTest(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		pass
		
	def test_success_response(self):
		u = {"username":"jupaoqq", 
			"first_name":"daniel",
			"last_name":"wang",
			"age":21,
			"gender":"M",
			"email_address":"hw4ce@virginia.edu",
			"zipcode":22904,
			"password":"gshbdh"}
		c = Client()
		response = c.post('/api/v1/users/create', u)
		#print (json.loads((response.content).decode("utf-8")))
		update = {'last_name': 'yang'}
		response = c.get('/api/v1/users/' + str(1) + '/delete')
		json_response = json.loads((response.content).decode("utf-8"))
		#print (json_response)
		self.assertEquals(json_response["ok"], True) 

	def tearDown(self):
		pass