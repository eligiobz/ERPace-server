# import os
# import app
# import unittest
# import tempfile
# import base64
# import json
# from jsoncompare import jsoncompare
# from models.MasterList import MasterList as MasterList
# from models.Product import Product as Product
# from models import db_session as db_session, engine, Base

# class ServiceTestCase(unittest.TestCase):

# 	auth_string = 'Basic ' + base64.b64encode(bytes('carlo' + ":" + '123', 'ascii')).decode('ascii')
# 	ClasIsSetup = False
	
# 	json_serv_1 = dict(
# 			barcode = '0001',
# 			price = 50.50,
# 			name = 'servicio_1'
# 			)
	
# 	json_serv_2 = dict(
# 			barcode = '0002',
# 			price = 1,
# 			name = 'servicio_2'
# 			)
	
# 	json_serv_3 = dict(
# 			barcode = '0003',
# 			price = 150,
# 			name = 'servicio_3'
# 			)
	
# 	json_serv_4 = dict(
# 			barcode = '0004',
# 			price = 3.40,
# 			name = 'servicio_4'
# 			)
	
# 	json_serv_5 = dict(
# 			barcode = '0005',
# 			price = 200,
# 			name = 'servicio_5'
# 			)

# 	json_serv_6 = dict(
# 			barcode = '1000',
# 			price = 23.50,
# 			name = 'servicio_6'
# 			)

# 	json_serv_7 = dict(
# 			barcode = '1001',
# 			price = 28.30,
# 			name = 'servicio_7'
# 			)

# 	def setupClass(self):
# 		engine.execute("delete from operation_logs; delete from masterlist")
# 		engine.execute("insert into drugstore(id, name) values (1, 'default');")
# 		engine.execute("insert into drugstore(id, name) values (2, 'Store 2');")
# 		self.add_service_1_1(self.json_serv_1)
# 		self.add_service_1_1(self.json_serv_2)
# 		self.add_service_1_1(self.json_serv_3)
# 		self.add_service_1_1(self.json_serv_4)
# 		self.add_service_1_1(self.json_serv_5)
# 		unittest.TestCase.setUp(self)

# 	@classmethod
# 	def tearDownClass(cls):
# 		engine.execute('delete from pricehistory; delete from product; delete from masterlist ;')
# 		engine.execute('delete from saledetails; ')
# 		engine.execute("delete from drugstore;")

# 	def setUp(self):
# 		app.app.testing = True
# 		self.app = app.app.test_client()
# 		if not self.ClasIsSetup:
# 			print ("Initalizing testing environment")
# 			self.setupClass()
# 			self.__class__.ClasIsSetup = True
	
# 	def open_with_auth(self, url, method, data=None):
# 		return self.app.open(url, method=method,
# 			headers={ 'Authorization': self.auth_string },
# 			data=json.dumps(data),
# 			content_type='application/json'
# 			)

# 	def add_service_1_1(self, data):
# 		return self.open_with_auth('/api/v1.1/add_service/', 'POST', data)

	
# 	def find_service_1_1(self, storeid, barcode):
# 		return self.open_with_auth('/api/v1.1/find_service/'+barcode, 'GET')

# 	def list_service_1_1(self, storeid):
# 		return self.open_with_auth('/api/v1.1/list_service/', 'GET')

# 	def update_service_1_1(self, barcode, data):
# 		return self.open_with_auth('/api/v1.1/update_service/', 'PUT', data)

# 	def test_001_add_product_1_0(self):
# 		response = self.add_service_1_1(self.json_serv_7)
# 		json_data = json.loads(response.data)
# 		assert response.status_code == 200
# 		assert jsoncompare.are_same(json_data, self.json_serv_7, True)

# 	def test_002_find_product_1_1(self):
# 		response = self.find_service_1_1('2','1001')
# 		json_data = json.loads(response.data)
# 		assert jsoncompare.are_same(json_data, self.json_serv_7, True)
# 		assert response.status_code == 200

# 	def test_003_list_products_1_1(self):
# 		response = self.list_service_1_1(1)
# 		assert response.status_code == 200

# if __name__ == "__main__":
# 	unittest.main()