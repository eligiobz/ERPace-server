import os
import app
import unittest
import tempfile
import base64
import json
from models.MasterList import MasterList as MasterList
from models.Product import Product as Product

class ProductTestCase(unittest.TestCase):

	auth_string = 'Basic ' + base64.b64encode(bytes('carlo' + ":" + '123', 'ascii')).decode('ascii')
	barcode = '1000'
	initial_units = 10
	name = 'crema_1'
	price = 5.50
	storeid = 1

	@classmethod
	def setUpClass(cls):
		pass
		# add_product_1_1('0001', 4, 50.50, 'crema_1', 1)
		# add_product_1_1('0002', 8, 10,'crema_2', 1)
		# add_product_1_1('0003', 6, 150,	'crema_3', 1)
		# add_product_1_1('0004', 3, 3.40, 'crema_4', 2)
		# add_product_1_1('0005', 1, 200,	'crema_5', 2)

	@classmethod
	def tearDownClass(cls):
		Product.query.delete()
		MasterList.query.delete()

	def setUp(self):
		app.app.testing = True
		self.app = app.app.test_client()

	def tearDown(self):
		pass

	def open_with_auth(self, url, method, data=None):
		return self.app.open(url, method=method,
			headers={ 'Authorization': self.auth_string },
			data=data,
			content_type='application/json'
			) 

	def add_product_1_0(self, barcode, units, price, name):
		return self.open_with_auth('/api/v1.0/add_product/', 'POST', json.dumps(dict(
			barcode = barcode,
			price = price,
			units = units,
			name = name)))

	def add_product_1_1(self, barcode, units, price, name, storeid):
		return self.open_with_auth('/api/v1.1/add_product/', 'POST', json.dumps(dict(
			barcode = barcode,
			units = units,
			price = price,
			name = name,
			storeid = storeid)))

	def find_product_1_0(self, barcode):
		return self.open_with_auth('/api/v1.0/find_product/'+barcode, 'GET')

	def find_product_1_1(self, barcode):
		return self.open_with_auth('/api/v1.1/find_product/'+barcode, 'GET')

	def list_products_1_0(self):
		return self.open_with_auth('/api/v1.0/list_product/', 'GET')

	def list_products_1_1(self):
		return self.open_with_auth('/api/v1.1/list_product/', 'GET')

	def test_001_add_product_1_0(self):
		rv = self.add_product_1_0(self.barcode, self.initial_units, self.price, self.name)
		json_data = json.loads(rv.data)
		assert rv.status_code == 200
		assert json_data['barcode'] == self.barcode
		assert json_data['name'] == self.name
		assert int(json_data['units']) == self.initial_units
		assert float(json_data['price']) == self.price
		assert int(json_data['storeid']) == 1

	def test_002_add_product_1_1(self):
		rv = self.add_product_1_1('1001', self.initial_units, self.price, 
			self.name, self.storeid)
		json_data = json.loads(rv.data)
		assert rv.status_code == 200
		assert json_data['barcode'] == '1001'
		assert json_data['name'] == self.name
		assert int(json_data['units']) == self.initial_units
		assert float(json_data['price']) == self.price
		assert int(json_data['storeid']) == self.storeid

	def test_003_find_product_1_0(self):
		rv = self.find_product_1_0(self.barcode)
		json_data = json.loads(rv.data)
		assert rv.status_code == 200
		assert json_data['barcode'] == self.barcode
		assert json_data['name'] == self.name
		assert int(json_data['units']) == self.initial_units
		assert float(json_data['price']) == self.price
		assert int(json_data['storeid']) == self.storeid

	def test_004_find_product_1_1(self):
		rv = self.find_product_1_0('1001')
		json_data = json.loads(rv.data)
		assert rv.status_code == 200
		assert json_data['barcode'] == '1001'
		assert json_data['name'] == self.name
		assert int(json_data['units']) == self.initial_units
		assert float(json_data['price']) == self.price
		assert int(json_data['storeid']) == self.storeid


if __name__ == '__main__':
	unittest.main()