# -*- coding:utf-8 -*-

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

class SalesTestCase(unittest.TestCase):

	auth_string = 'Basic ' + base64.b64encode(bytes('carlo' + ":" + '123', 'ascii')).decode('ascii')
	ClasIsSetup = False
	
	json_prod_1 = json.dumps({
			'barcode' : '0001',
			'price' : 50.50,
			'units' : 4,
			'name' : 'crema_1',
			'storeid' :  1})
	
	json_prod_2 = json.dumps({
			'barcode' : '0002',
			'price' : 1,
			'units' : 8,
			'name' : 'crema_2',
			'storeid' :  1})
	
	json_prod_3 = json.dumps({
			'barcode' : '0003',
			'price' : 150,
			'units' : 6,
			'name' : 'crema_3',
			'storeid' :  1})
	
	json_prod_4 = json.dumps({
			'barcode' : '0004',
			'price' : 3.40,
			'units' : 3,
			'name' : 'crema_4',
			'storeid' :  2})
	
	json_prod_5 = json.dumps({
			'barcode' : '0005',
			'price' : 200,
			'units' : 1,
			'name' : 'crema_5',
			'storeid' :  2})

	json_prod_6 = json.dumps({
			'barcode' : '0002',
			'price' : 1,
			'units' : 5,
			'name' : 'crema_2',
			'storeid' :  2})

	json_prod_7 = json.dumps({
			'barcode' : '0001',
			'price' : 50.50,
			'units' : 5,
			'name' : 'crema_1',
			'storeid' :  2})

	def setupClass(self):
		engine.execute("delete from operation_logs;")
		engine.execute("insert into drugstore(id, name) values (1, 'default');")
		engine.execute("insert into drugstore(id, name) values (2, 'Store 2');")
		self.add_product_1_1(self.json_prod_1)
		self.add_product_1_1(self.json_prod_2)
		self.add_product_1_1(self.json_prod_3)
		self.add_product_1_1(self.json_prod_4)
		self.add_product_1_1(self.json_prod_5)
		self.update_product_1_1('0002',self.json_prod_6)
		self.update_product_1_1('0001',self.json_prod_7)
		unittest.TestCase.setUp(self)

	@classmethod
	def tearDownClass(cls):
		engine.execute('delete from saledetails; delete from sale; delete from\
						pricehistory; delete from product; delete from masterlist ;')
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

	def add_product_1_1(self, data):
		return self.open_with_auth('/api/v1.1/add_product/', 'POST', data)

	def find_product_1_1(self, storeid, barcode):
		return self.open_with_auth('/api/v1.1/find_product/'+storeid+'/'+barcode, 'GET')

	def update_product_1_1(self, bcode, data):
		return self.open_with_auth('/api/v1.1/update_product/'+bcode, 'PUT', data)

	def make_sale_1_0(self, data):
		return self.open_with_auth('/api/v1.0/make_sale/', 'POST', data)

	def make_sale_1_1(self, data):
		return self.open_with_auth('/api/v1.1/make_sale/', 'POST', data)

	def test_001_make_sale_1_0_normal(self):
		item_1 = dict(
			barcode = '0001',
			units = 2,
			price = 0.0
			)
		item_2 = dict(
			barcode = '0002',
			units = 8,
			price = 0.0
			)
		response = self.find_product_1_1('1', item_1['barcode'])
		assert response.status_code == 200
		data = json.loads(response.data)
		item_1['price'] = float(data['price'])
		response = self.find_product_1_1('1', item_2['barcode'])
		assert response.status_code == 200
		data = json.loads(response.data)
		item_2['price'] = data['price']
		sale = json.dumps({
					"barcode": [item_1['barcode'], item_2['barcode']],
					"units" : [item_1['units'], item_2['units']],
					"token": "1"
				})
		response = self.make_sale_1_0(sale)
		assert response.status_code == 200
		json_data = json.loads(response.data)
		for item in json_data:
			if item['barcode'] == item_1['barcode']:
				assert int(item['units']) == 2
				assert (float(item['price']) * int (item['units'])) == item_1['price'] * item_1['units']
			elif item['barcode'] == item_2['barcode']:
				assert int(item['units']) == 8
				assert (float(item['price']) * int (item['units'])) == item_2['price'] * item_2['units']
		response = self.find_product_1_1('1','0001')
		assert response.status_code==200
		data = json.loads(response.data)
		assert int(data['storeid']) == 1
		assert int(data['units']) == 2 # 4 - 2
		response = self.find_product_1_1('1','0002')
		assert response.status_code==200
		data = json.loads(response.data)
		assert int(data['storeid']) == 1
		assert int(data['units']) == 0 # 8 - 4

	def test_002_make_sale_1_1_normal(self):
		item_1 = dict(
			barcode = '0001',
			units = 2,
			price = 0.0,
			storeid = 2
			)
		item_2 = dict(
			barcode = '0004',
			units = 3,
			price = 0.0,
			storeid = 2 
			)
		response = self.find_product_1_1(str(item_1['storeid']), item_1['barcode'])
		assert response.status_code == 200
		data = json.loads(response.data)
		item_1['price'] = float(data['price'])
		response = self.find_product_1_1(str(item_2['storeid']), item_2['barcode'])
		assert int(data['storeid']) == 2
		assert response.status_code == 200
		data = json.loads(response.data)
		item_2['price'] = data['price']
		assert int(data['storeid']) == 2
		sale = json.dumps({
					"barcode": [item_1['barcode'], item_2['barcode']],
					"units" : [item_1['units'], item_2['units']],
					"token": "5",
					"storeid": 2
				})
		response = self.make_sale_1_1(sale)
		assert response.status_code == 200
		json_data = json.loads(response.data)
		for item in json_data:
			if item['barcode'] == item_1['barcode']:
				assert int(item['units']) == 2 # 2
				assert (float(item['price']) * int (item['units'])) == item_1['price'] * item_1['units']
			elif item['barcode'] == item_2['barcode']:
				assert int(item['units']) == 3 # 1
				assert (float(item['price']) * int (item['units'])) == item_2['price'] * item_2['units']
		response = self.find_product_1_1('2', item_1['barcode'])
		assert response.status_code==200
		data = json.loads(response.data)
		assert int(data['units']) == 3 # 5 - 2
		response = self.find_product_1_1('2', item_2['barcode'])
		assert response.status_code==200
		data = json.loads(response.data)
		assert int(data['units']) == 0 # 3 - 1

	def test_003_make_sale_1_0_fail_duplicated_sale(self):
		response = self.find_product_1_1('1', '0002')
		assert response.status_code == 200
		sale = json.dumps({
					"barcode": ['0001', '0002'],
					"units" : [2, 8],
					"token" : "1"
				})
		response = self.make_sale_1_0(sale)
		assert response.status_code == 428

	def test_004_make_sale_1_1_fail_duplicated_sale(self):
		response = self.find_product_1_1('2','0004')
		assert response.status_code == 200
		sale = json.dumps({
					"barcode": ['0001', '0004'],
					"units" : [2, 3],
					"token" : "5",
					"storeid": 2
				})
		response = self.make_sale_1_1(sale)
		assert response.status_code == 428

	def test_005_make_sale_1_0_fail_not_enough_products(self):
		response = self.find_product_1_1('1', '0002')
		assert response.status_code == 200
		sale = json.dumps({
					"barcode": ['0002'],
					"units" : [8],
					"token" : "2"
				})
		response = self.make_sale_1_0(sale)
		assert response.status_code == 406
		assert b'insuficientes' in response.data


	def test_006_make_sale_1_1_fail_not_enough_products(self):
		response = self.find_product_1_1('2','0004')
		assert response.status_code == 200
		sale = json.dumps({
					"barcode": ['0004'],
					"units" : [8],
					"token" : "8",
					"storeid": 2
				})
		response = self.make_sale_1_1(sale)
		assert response.status_code == 406
		assert b'insuficientes' in response.data


	def test_007_make_sale_1_0_fail_malformed_request(self):
		sale = json.dumps({
					"barcode": [],
					"units" : [8],
					"token" : "2"
				})
		response = self.make_sale_1_0(sale)
		assert response.status_code == 400

	def test_008_make_sale_1_1_fail_malformed_request(self):
		sale = json.dumps({
					"barcode": [],
					"units" : [8],
					"token" : "2"
				})
		response = self.make_sale_1_1(sale)
		assert response.status_code == 400


	def test_009_make_sale_1_1_fail_no_store_id(self):
		response = self.find_product_1_1('2','0004')
		assert response.status_code == 200
		sale = json.dumps({
					"barcode": ['0004'],
					"units" : [8],
					"token" : "8",
				})
		response = self.make_sale_1_1(sale)
		assert response.status_code == 400

	def test_010_make_sale_1_1_fail_invalid_store_id(self):
		response = self.find_product_1_1('2','0004')
		assert response.status_code == 200
		sale = json.dumps({
					"barcode": ['0004'],
					"units" : [8],
					"token" : "8",
					"storeid" : 10
				})
		response = self.make_sale_1_1(sale)
		assert b'storeid' in response.data
		assert response.status_code == 406

	def test_011_make_sale_1_0_fail_no_data(self):
		response = self.make_sale_1_0(None)
		assert response.status_code == 400

	def test_012_make_sale_1_1_fail_no_data(self):
		response = self.make_sale_1_1(None)
		assert response.status_code == 400

	def test_013_make_sale_1_0_fail_no_json(self):
		response = self.make_sale_1_0(json.dumps(None))
		assert response.status_code == 400

	def test_014_make_sale_1_1_fail_no_json(self):
		response = self.make_sale_1_1(json.dumps(None))
		assert response.status_code == 400

	def test_015_make_sale_1_1_fail_inexistent_product(self):
		sale = json.dumps({
					"barcode": ['0010'],
					"units" : [8],
					"token" : "8",
					"storeid": 2
				})
		response = self.make_sale_1_1(sale)
		assert response.status_code == 406
		assert b'no existe' in response.data

	def test_016_make_sale_1_1_fail_existent_product_no_in_this_store(self):
		response = self.find_product_1_1('1','0002')
		assert response.status_code == 200
		sale = json.dumps({
					"barcode": ['0003'],
					"units" : [8],
					"token" : "8",
					"storeid": 2
				})
		response = self.make_sale_1_1(sale)
		assert response.status_code == 406
		assert b'no existe' in response.data

if __name__ == "__main__":
	unittest.main()