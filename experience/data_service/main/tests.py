from django.test import SimpleTestCase, Client
from main import models
import json
import logging
import requests

# User story 5
class PetSearchTest(SimpleTestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		pass
		
	def test_success_response(self):
		dog = {'name': 'Rocky', 'pet_type': 'dog', 'description': 'A very nice dog', 'price': '99.999'}
		c = Client()
		response = requests.post(url = "http://entity:8000/api/v1/pets/create", data = dog) 
		#print(response)
		kw = {"keyword" : "dog"}
		response = c.post('/test/search_pets', kw)
		#print (json.loads((response.content).decode("utf-8")))
		json_response = json.loads((response.content).decode("utf-8"))
		#response = requests.get(url = "http://entity:8000/api/v1/pets/1/delete")
		#print (json.loads((response.content).decode("utf-8")))
		self.assertEquals(json_response["ok"], True) 
		
		
	def tearDown(self):
		pass

