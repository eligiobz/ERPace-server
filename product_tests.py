import os
import app
import unittest
import tempfile
import base64
import json

class ProductTestCase(unittest.TestCase):

	username = 'carlo'
	password = '123'

	def setUp(self):
		app.app.testing = True
		self.app = app.app.test_client()

	def tearDown(self):
		pass

	def open_with_auth(self, url, method, data=None):
		return self.app.open(url, method=method,
			headers={
			'Authorization': 'Basic ' + base64.b64encode(bytes(self.username + ":" + self.password, 'ascii')).decode('ascii')
			}, data=data, content_type='application/json'
			)

	def get_headers(self):
		return {
			'Authorization': 'Basic ' + base64.b64encode(bytes(self.username + ":" + self.password, 'ascii')).decode('ascii')
			} 

	def add_product_1_0(self, barcode, price, units, name):
		return self.open_with_auth('/api/v1.0/add_product/', 'POST', json.dumps(dict(
			barcode = barcode,
			price = price,
			units = units,
			name = name)))

	def test_add_product(self):
		rv = self.add_product_1_0('1000', 10, 5, 'crema_1')
		assert rv.status_code == 200
		assert b'"barcode": "1000"'

	def find_product_1_0(self, barcode):
		return self.app.get('/api/v1.0/findProduct/'+barcode,
			headers={
			'Authorization': 'Basic ' + base64.b64encode(bytes('carlo' + ":" + '123', 'ascii')).decode('ascii')
			})

	def test_find_product_1_0(self):
		rv = self.find_product_1_0('001')
		assert b'"barcode": "001"' in rv.data

if __name__ == '__main__':
	unittest.main()