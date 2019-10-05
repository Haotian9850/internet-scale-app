from django.test import TestCase, Client
from main import models
import json
import logging

# User story 1
class PetSearchTest(TestCase):
# 1
	def setUp(self):
		logging.disable(logging.CRITICAL)
		pass
		
	def test_success_response(self):
		dog = {'name': 'Rocky', 'pet_type': 'dog', 'description': 'A vert nice dog', 'price': '99.999'}
		c = Client()
		response = c.post('http://entity:8000/api/v1/pets/create', dog)
		print(response)
		kw = {"keyword" : "dog"}
		response = c.post('/test/search_pets', kw)
		print (response)
		json_response = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_response["ok"], True) 
		
	def tearDown(self):
		pass