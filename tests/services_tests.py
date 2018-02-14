import os
import app
import unittest
import tempfile
import base64
import json
from jsoncompare import jsoncompare
from models.MasterList import MasterList as MasterList
from models.Product import Product as Product
from models import db_session as db_session, engine, Base

class ServiceTestCase(unittest.TestCase):

	auth_string = 'Basic ' + base64.b64encode(bytes('carlo' + ":" + '123', 'ascii')).decode('ascii')
	ClasIsSetup = False
	
	json_serv_1 = json.dumps({
			'barcode' : '0001',
			'price' : 50.50,
			'name' : 'servicio_1'
			})
	
	json_serv_2 = json.dumps({
			'barcode' : '0002',
			'price' : 1,
			'name' : 'servicio_2'
			})
	
	json_serv_3 = json.dumps({
			'barcode' : '0003',
			'price' : 150.0,
			'name' : 'servicio_3'
			})
	
	json_serv_4 = json.dumps({
			'barcode' : '0004',
			'price' : 3.40,
			'name' : 'servicio_4'
			})
	
	json_serv_5 = json.dumps({
			'barcode' : '0005',
			'price' : 200,
			'name' : 'servicio_5'
			})

	json_serv_6 = json.dumps({
			'barcode' : '1000',
			'price' : 23.50,
			'name' : 'servicio_6'
			})

	def setupClass(self):
		response = self.list_service_1_1()
		assert response.status_code == 412
		engine.execute("delete from operation_logs; delete from services;")
		engine.execute("insert into drugstore(id, name) values(1, 'prod_1');")
		engine.execute("insert into products_masterlist(barcode, name, price) values('2000', 'prod_1', 10);")
		engine.execute("insert into product(barcode, units, storeid) values('2000', 5 , 1);")
		self.add_service_1_1(self.json_serv_1)
		self.add_service_1_1(self.json_serv_2)
		self.add_service_1_1(self.json_serv_3)
		self.add_service_1_1(self.json_serv_4)
		self.add_service_1_1(self.json_serv_5)
		unittest.TestCase.setUp(self)

	@classmethod
	def tearDownClass(cls):
		engine.execute('delete from service_price_history; delete from services;')
		engine.execute('delete from saledetails;')
		engine.execute("delete from product; delete from products_masterlist;")
		engine.execute("delete from drugstore;")

	def setUp(self):
		app.app.testing = True
		self.app = app.app.test_client()
		if not self.ClasIsSetup:
			print ("Initalizing testing environment")
			self.setupClass()
			self.__class__.ClasIsSetup = True
	
	def open_with_auth(self, url, method, data=None):
		return self.app.open(url, method=method,
			headers={ 'Authorization': self.auth_string },
			data=data,
			content_type='application/json'
			)

	def add_service_1_1(self, data):
		return self.open_with_auth('/api/v1.1/add_service/', 'POST', data)
	
	def find_service_1_1(self, barcode):
		return self.open_with_auth('/api/v1.1/find_service/'+barcode, 'GET')

	def list_service_1_1(self):
		return self.open_with_auth('/api/v1.1/list_services/', 'GET')

	def update_service_1_1(self, barcode, data):
		return self.open_with_auth('/api/v1.1/update_service/'+barcode, 'PUT', data)

	def test_001_add_service_1_1(self):
		response = self.add_service_1_1(self.json_serv_6)
		assert response.status_code == 200
		json_data = json.loads(response.data)
		assert jsoncompare.are_same(json_data["mobilerp"], self.json_serv_6, True)

	def test_002_find_service_1_1(self):
		response = self.find_service_1_1('1000')
		assert response.status_code == 200
		json_data = json.loads(response.data)
		assert jsoncompare.are_same(json_data["mobilerp"], self.json_serv_6, True)
	
	def test_003_list_services_1_1(self):
		response = self.list_service_1_1()
		assert response.status_code == 200
		json_data = json.loads(response.data)
		assert len(json_data["mobilerp"]) == 6
		for item in json_data["mobilerp"]:
			if item['barcode'] == '0001':
				assert jsoncompare.are_same(item, self.json_serv_1, True)
			elif item['barcode'] == '0002':
				assert jsoncompare.are_same(item, self.json_serv_2, True)
			elif item['barcode'] == '0003':
				assert jsoncompare.are_same(item, self.json_serv_3, True)
			elif item['barcode'] == '0004':
				assert jsoncompare.are_same(item, self.json_serv_4, True)
			elif item['barcode'] == '0005':
				assert jsoncompare.are_same(item, self.json_serv_5, True)
			elif item['barcode'] == '0006':
				assert jsoncompare.are_same(item, self.json_serv_6, True)

	def test_004_update_service_1_1_change_name(self):
		service = dict(
			barcode = '0003',
			name = 'doritos'
			)
		response = self.find_service_1_1(service['barcode'])
		assert response.status_code == 200
		response = self.update_service_1_1(service['barcode'], json.dumps(service))
		assert response.status_code == 200
		json_data = json.loads(response.data)
		assert jsoncompare.are_same(json_data["mobilerp"], json.dumps(service))

	def test_005_update_service_1_1_change_price(self):
		service = dict(
			barcode = '0001',
			price = 10.5
		)
		response = self.find_service_1_1(service['barcode'])
		assert response.status_code == 200
		response = self.update_service_1_1(service['barcode'], json.dumps(service))
		assert response.status_code == 200
		json_data = json.loads(response.data)
		assert jsoncompare.are_same(json_data["mobilerp"], json.dumps(service))
		
	def test_006_update_service_1_1_change_all(self):
		service = dict(
			barcode = '0002',
			price = 701,
			name = 'mani',
		)
		response = self.find_service_1_1(service['barcode'])
		assert response.status_code == 200
		response = self.update_service_1_1(service['barcode'], json.dumps(service))
		assert response.status_code == 200
		json_data = json.loads(response.data)
		assert jsoncompare.are_same(json_data["mobilerp"], json.dumps(service))

	def test_007_find_service_fail_1_1(self):
		response = self.find_service_1_1('5001')
		assert response.status_code == 404

	def test_008_add_service_1_1_fail_existent_service(self):
		response = self.add_service_1_1(self.json_serv_1)
		assert response.status_code == 409

	def test_009_add_service_1_1_fail_no_json(self):
		response = self.add_service_1_1(None)
		assert response.status_code == 400

	def test_010_add_service_1_1_fail_incomplete_json(self):
		product = dict(
			name = 'huirr',
			price = 1.2
			)
		response = self.add_service_1_1(json.dumps(product))
		assert response.status_code == 400
		product = dict(
			barcode = '78965',
			name = 'huirr',
			)
		response = self.add_service_1_1(json.dumps(product))
		assert response.status_code == 400

	def test_011_add_service_1_1_fail_empty_data(self):
		product = dict(
			barcode = '',
			name = '',
			price = 1.2,
			units = 3
			)
		response = self.add_service_1_1(json.dumps(product))
		assert response.status_code == 400

	def test_012_add_service_1_1_fail_duplicated_operation(self):
		response = self.add_service_1_1(self.json_serv_1)
		assert response.status_code == 428

	def test_013_update_service_1_1_fail_no_json_data(self):
		response = self.update_service_1_1('0001', json.dumps(None))
		assert response.status_code == 400

	def test_014_update_service_1_0_fail_invalid_service(self):
		service = dict(
			barcode = '0111',
			units = 1)
		response = self.update_service_1_1(service['barcode'], json.dumps(service))
		assert response.status_code == 400

	def test_015_update_service_1_0_fail_duplicated_operation(self):
		service = dict(
			barcode = '0002',
			price = 701,
			name = 'mani'
			)
		response = self.update_service_1_1(service['barcode'], json.dumps(service))
		assert response.status_code == 428
		
	def test_016_update_service_1_1_fail_inexistent_service(self):
		service = dict(
			barcode = '1111',
			price = 701,
			name = 'mani'
			)
		response = self.update_service_1_1(service['barcode'], json.dumps(service))
		assert response.status_code == 400

	def test_017_add_service_1_1_sucess_no_price_change(self):
		service = dict(
			barcode = '0003',
			price = 150.0,
			)
		response = self.find_service_1_1(service['barcode'])
		assert response.status_code == 200
		response = self.update_service_1_1(service['barcode'], json.dumps(service))
		assert response.status_code == 200
		json_data = json.loads(response.data)
		assert float(json_data["mobilerp"]['price']) == service['price']


if __name__ == "__main__":
	unittest.main()