from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from main import models
import json
import logging

# User story 1
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

# User story 2
class PetUpdateTest(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		pass
		
	def test_success_response(self):
		dog = {'name': 'Rocky', 'pet_type': 'dog', 'description': 'A vert nice dog', 'price': '99.999'}
		c = Client()
		response = c.post('/api/v1/pets/create', dog)
		update = {'description': 'good dog'}
		response = c.post('/api/v1/pets/' + str(5) + '/update', update)
		json_response = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_response["ok"], True) 

	def test_failure_response(self):
		dog = {'name': 'Rocky', 'pet_type': 'dog', 'description': 'A vert nice dog', 'price': '99.999'}
		c = Client()
		response = c.post('/api/v1/pets/create', dog)
		update = {'description': 100}
		response = c.post('/api/v1/pets/' + str(6) + '/update', update)
		json_response = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_response["ok"], False) 
		
	def tearDown(self):
		pass

#User story 3
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