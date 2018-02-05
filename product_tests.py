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

class ProductTestCase(unittest.TestCase):

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
			'barcode' : '1000',
			'price' : 23.50,
			'units' : 8,
			'name' : 'crema_X'}, ensure_ascii=False, sort_keys=True)

	json_prod_7 = json.dumps({
			'barcode' : '1001',
			'price' : 28.30,
			'units' : 4,
			'name' : 'crema_X2',
			'storeid': 2})


	def setupClass(self):
		engine.execute("delete from operation_logs;")
		self.add_product_1_1(self.json_prod_1)
		self.add_product_1_1(self.json_prod_2)
		self.add_product_1_1(self.json_prod_3)
		self.add_product_1_1(self.json_prod_4)
		self.add_product_1_1(self.json_prod_5)
		unittest.TestCase.setUp(self)

	@classmethod
	def tearDownClass(cls):
		engine.execute('delete from pricehistory; delete from product; delete from masterlist ;')

	def setUp(self):
		app.app.testing = True
		self.app = app.app.test_client()
		if not self.ClasIsSetup:
			print ("Initalizing testing environment")
			self.setupClass()
			self.__class__.ClasIsSetup = True
		

	def tearDown(self):
		pass

	def open_with_auth(self, url, method, data=None):
		return self.app.open(url, method=method,
			headers={ 'Authorization': self.auth_string },
			data=data,
			content_type='application/json'
			)

	def add_product_1_0(self, data):
		return self.open_with_auth('/api/v1.0/add_product/', 'POST', data)

	def add_product_1_1(self, data):
		return self.open_with_auth('/api/v1.1/add_product/', 'POST', data)

	def find_product_1_0(self, barcode):
		return self.open_with_auth('/api/v1.0/find_product/'+barcode, 'GET')

	def find_product_1_1(self, barcode):
		return self.open_with_auth('/api/v1.1/find_product/'+barcode, 'GET')

	def list_products_1_0(self):
		return self.open_with_auth('/api/v1.0/list_products/', 'GET')

	def list_products_1_1(self, storeid):
		return self.open_with_auth('/api/v1.1/list_products/'+str(storeid), 'GET')

	def test_001_add_product_1_0(self):
		rv = self.add_product_1_0(self.json_prod_6)
		json_data = json.loads(rv.data)
		assert rv.status_code == 200
		assert jsoncompare.are_same(json_data, self.json_prod_6, False, ['storeid'])

	def test_002_add_product_1_1(self):
		rv = self.add_product_1_1(self.json_prod_7)
		json_data = json.loads(rv.data)
		assert rv.status_code == 200
		assert jsoncompare.are_same(json_data, self.json_prod_7, True)

	def test_003_find_product_1_0(self):
		rv = self.find_product_1_0('1000')
		json_data = json.loads(rv.data)
		assert jsoncompare.are_same(json_data, self.json_prod_6, False, ['storeid'])
		assert rv.status_code == 200

	def test_004_find_product_1_1(self):
		rv = self.find_product_1_1('1001')
		json_data = json.loads(rv.data)
		assert jsoncompare.are_same(json_data, self.json_prod_7, False, ['storeid'])
		assert rv.status_code == 200

	def test_005_list_products_1_0(self):
		rv = self.list_products_1_0()
		json_data = json.loads(rv.data)
		assert len(json_data['mobilerp']) == 4
		assert rv.status_code == 200
		assert b'0001' in rv.data
		assert b'0002' in rv.data
		assert b'0003' in rv.data
		assert b'1000' in rv.data
		for item in json_data['mobilerp']:
			if item['barcode'] == '0001':
				assert jsoncompare.are_same(item, self.json_prod_1, False, ['storeid'])
			if item['barcode'] == '0002':
				assert jsoncompare.are_same(item, self.json_prod_2, False, ['storeid'])
			if item['barcode'] == '0003':
				assert jsoncompare.are_same(item, self.json_prod_3, False, ['storeid'])
			if item['barcode'] == '1000':
				assert jsoncompare.are_same(item, self.json_prod_6, False, ['storeid'])
		
	def test_006_list_products_1_1(self):
		rv = self.list_products_1_1(1)
		json_data = json.loads(rv.data)
		assert len(json_data['mobilerp']) == 4
		assert rv.status_code == 200
		assert b'0001' in rv.data
		assert b'0002' in rv.data
		assert b'0003' in rv.data
		assert b'1000' in rv.data
		for item in json_data['mobilerp']:
			if item['barcode'] == '0001':
				assert jsoncompare.are_same(item, self.json_prod_1, True)
			if item['barcode'] == '0002':
				assert jsoncompare.are_same(item, self.json_prod_2, True)
			if item['barcode'] == '0003':
				assert jsoncompare.are_same(item, self.json_prod_3, True)
			if item['barcode'] == '1000':
				assert jsoncompare.are_same(item, self.json_prod_6, True)
		rv = self.list_products_1_1(2)
		json_data = json.loads(rv.data)
		assert len(json_data['mobilerp']) == 3
		assert rv.status_code == 200
		assert b'0004' in rv.data
		assert b'0005' in rv.data
		assert b'1001' in rv.data
		for item in json_data['mobilerp']:
			if item['barcode'] == '0004':
				assert jsoncompare.are_same(item, self.json_prod_4, True)
			if item['barcode'] == '0005':
				assert jsoncompare.are_same(item, self.json_prod_5, True)
			if item['barcode'] == '0003':
				assert jsoncompare.are_same(item, self.json_prod_7, True)

if __name__ == '__main__':
	unittest.main()