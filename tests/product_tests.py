
# -*- coding:utf-8 -*-

##############################################################################
# MobilEPR - A small self-hosted ERP that works with your smartphone.
# Copyright (C) 2017  Eligio Becerra
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################

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
		engine.execute("insert into drugstore(id, name) values (1, 'default');")
		engine.execute("insert into drugstore(id, name) values (2, 'Store 2');")
		self.add_product_1_1(self.json_prod_1)
		self.add_product_1_1(self.json_prod_2)
		self.add_product_1_1(self.json_prod_3)
		self.add_product_1_1(self.json_prod_4)
		self.add_product_1_1(self.json_prod_5)
		unittest.TestCase.setUp(self)

	@classmethod
	def tearDownClass(cls):
		engine.execute('delete from pricehistory; delete from product; delete from masterlist ;')
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

	def update_product_1_0(self, barcode, data):
		return self.open_with_auth('/api/v1.0/update_product/'+str(barcode), 'PUT', data)

	def update_product_1_1(self, barcode, data):
		return self.open_with_auth('/api/v1.1/update_product/'+str(barcode), 'PUT', data)

	def list_depleted_products_1_0(self):
		return self.open_with_auth('/api/v1.0/list_depleted_products/', 'GET')

	def list_depleted_products_1_1(self):
		return self.open_with_auth('/api/v1.1/list_depleted_products/', 'GET')

	def test_001_add_product_1_0(self):
		response = self.add_product_1_0(self.json_prod_6)
		json_data = json.loads(response.data)
		assert response.status_code == 200
		assert jsoncompare.are_same(json_data, self.json_prod_6, False, ['storeid'])

	def test_002_add_product_1_1(self):
		response = self.add_product_1_1(self.json_prod_7)
		json_data = json.loads(response.data)
		assert response.status_code == 200
		assert jsoncompare.are_same(json_data, self.json_prod_7, True)

	def test_003_find_product_1_0(self):
		response = self.find_product_1_0('1000')
		json_data = json.loads(response.data)
		assert jsoncompare.are_same(json_data, self.json_prod_6, False, ['storeid'])
		assert response.status_code == 200

	def test_004_find_product_1_1(self):
		response = self.find_product_1_1('1001')
		json_data = json.loads(response.data)
		assert jsoncompare.are_same(json_data, self.json_prod_7, False, ['storeid'])
		assert response.status_code == 200

	def test_005_list_products_1_0(self):
		response = self.list_products_1_0()
		json_data = json.loads(response.data)
		assert len(json_data['mobilerp']) == 4
		assert response.status_code == 200
		assert b'0001' in response.data
		assert b'0002' in response.data
		assert b'0003' in response.data
		assert b'1000' in response.data
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
		response = self.list_products_1_1(1)
		json_data = json.loads(response.data)
		assert len(json_data['mobilerp']) == 4
		assert response.status_code == 200
		assert b'0001' in response.data
		assert b'0002' in response.data
		assert b'0003' in response.data
		assert b'1000' in response.data
		for item in json_data['mobilerp']:
			if item['barcode'] == '0001':
				assert jsoncompare.are_same(item, self.json_prod_1, True)
			if item['barcode'] == '0002':
				assert jsoncompare.are_same(item, self.json_prod_2, True)
			if item['barcode'] == '0003':
				assert jsoncompare.are_same(item, self.json_prod_3, True)
			if item['barcode'] == '1000':
				assert jsoncompare.are_same(item, self.json_prod_6, True)
		response = self.list_products_1_1(2)
		json_data = json.loads(response.data)
		assert len(json_data['mobilerp']) == 3
		assert response.status_code == 200
		assert b'0004' in response.data
		assert b'0005' in response.data
		assert b'1001' in response.data
		for item in json_data['mobilerp']:
			if item['barcode'] == '0004':
				assert jsoncompare.are_same(item, self.json_prod_4, True)
			if item['barcode'] == '0005':
				assert jsoncompare.are_same(item, self.json_prod_5, True)
			if item['barcode'] == '0003':
				assert jsoncompare.are_same(item, self.json_prod_7, True)

	def test_007_update_product_1_0_add_items(self):
		bCode = '0001'
		units = 4
		response = self.find_product_1_0(bCode)
		assert response.status_code == 200
		updated_product = json.dumps({
			'barcode' : bCode,
			'units' : units
			})
		response = self.update_product_1_0(bCode, updated_product)
		assert response.status_code == 200
		json_data = json.loads(response.data)
		assert json_data['barcode'] == bCode
		assert float(json_data['price']) ==  50.5
		assert int(json_data['units']) == 8 # 4 + 4 = 8
		assert json_data['name'] == 'crema_1'

	def test_008_update_item_1_1_add_items(self):
		bCode = '0002'
		units = 2
		response = self.find_product_1_1(bCode)
		assert response.status_code == 200
		updated_product = json.dumps({
			'barcode' : bCode,
			'units' : units,
			})
		response = self.update_product_1_0(bCode, updated_product)
		assert response.status_code == 200
		json_data = json.loads(response.data)
		assert json_data['barcode'] == bCode
		assert float(json_data['price']) ==  1.0
		assert int(json_data['units']) == 10 # 8 + 2 = 10
		assert json_data['name'] == 'crema_2'
		assert int(json_data['storeid']) == 1

	def test_009_update_item_1_0_change_name(self):
		bCode = '0003'
		name = 'doritos'
		response = self.find_product_1_0(bCode)
		assert response.status_code == 200
		updated_product = json.dumps({
			'barcode' : bCode,
			'name' : name,
			})
		response = self.update_product_1_0(bCode, updated_product)
		assert response.status_code == 200
		json_data = json.loads(response.data)
		assert json_data['barcode'] == bCode
		assert float(json_data['price']) ==  150
		assert int(json_data['units']) == 6
		assert json_data['name'] == name

	def test_010_update_item_1_1_change_name(self):
		bCode = '0004'
		name = 'tostitos'
		response = self.find_product_1_1(bCode)
		assert response.status_code == 200
		updated_product = json.dumps({
			'barcode' : bCode,
			'name' : name,
			'storeid' : 2
			})
		response = self.update_product_1_1(bCode, updated_product)
		assert response.status_code == 200
		json_data = json.loads(response.data)
		assert json_data['barcode'] == bCode
		assert float(json_data['price']) ==  3.4
		assert int(json_data['units']) == 3
		assert json_data['name'] == name
		assert int(json_data['storeid']) ==  2

	def test_011_update_item_1_0_change_price(self):
		bCode = '0001'
		price = 10.5
		response = self.find_product_1_0(bCode)
		assert response.status_code == 200
		updated_product = json.dumps({
			'barcode' : bCode,
			'price' : price
			})
		response = self.update_product_1_0(bCode, updated_product)
		assert response.status_code == 200
		json_data = json.loads(response.data)
		assert json_data['barcode'] == bCode
		assert float(json_data['price']) ==  price
		assert int(json_data['units']) == 8 # From last operation in database
		assert json_data['name'] == 'crema_1'

	def test_012_update_item_1_1_change_price(self):
		bCode = '0005'
		price = 32.5
		response = self.find_product_1_1(bCode)
		assert response.status_code == 200
		updated_product = json.dumps({
			'barcode' : bCode,
			'price' : price,
			'storeid': 2
			})
		response = self.update_product_1_1(bCode, updated_product)
		assert response.status_code == 200
		json_data = json.loads(response.data)
		assert json_data['barcode'] == bCode
		assert float(json_data['price']) ==  price
		assert int(json_data['units']) == 1 # From last operation in database
		assert json_data['name'] == 'crema_5'
		assert json_data['storeid'] == 2

	def test_013_update_item_1_0_change_all(self):
		bCode = '1000'
		price = 597.15
		name = 'orcos'
		units = 4
		response = self.find_product_1_0(bCode)
		assert response.status_code == 200
		updated_product = json.dumps({
			'barcode' : bCode,
			'price' : price,
			'name' : name,
			'units' : units
			})
		response = self.update_product_1_0(bCode, updated_product)
		assert response.status_code == 200
		json_data = json.loads(response.data)
		assert json_data['barcode'] == bCode
		assert float(json_data['price']) ==  price
		assert int(json_data['units']) == 12 # 8 + 4
		assert json_data['name'] == name

	def test_014_update_item_1_1_change_all(self):
		bCode = '1001'
		price = 701
		name = 'mani'
		units = 9
		response = self.find_product_1_1(bCode)
		assert response.status_code == 200
		updated_product = json.dumps({
			'barcode' : bCode,
			'price' : price,
			'name' : name,
			'units' : units,
			'storeid': 2
			})
		response = self.update_product_1_1(bCode, updated_product)
		assert response.status_code == 200
		json_data = json.loads(response.data)
		assert json_data['barcode'] == bCode
		assert float(json_data['price']) ==  price
		assert int(json_data['units']) == 13 # From last operation in database
		assert json_data['name'] == name
		assert json_data['storeid'] == 2
	
	# def test_015_list_depleted_products_1_0(self):
	# 	# We need a fake sale so depleted items views will populated properly
	# 	json_sale = json.dumps({

	# 		})
	# 	self.open_with_auth('make')
	# 	print (res.fetchall())
	# 	response = self.list_depleted_products_1_0()
	# 	print(response.data)
	# 	assert response.status_code == 200
	# 	json_data = json.loads(response.data)
	# 	assert len(json_data) == 2
	# 	assert b'0001' in response.data
	# 	assert b'0002' in response.data

	# def test_016_list_depleted_products_1_1(self):
	# 	engine.execute("update product set units = 0 where storeid = 1 and barcode='0003';")
	# 	engine.execute("update product set units = 0 where storeid = 2 and barcode='0004';")
	# 	assert True == False

if __name__ == '__main__':
	unittest.main()
