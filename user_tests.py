import os
import app
import unittest
import tempfile
import base64
import json

class UsersTestCase(unittest.TestCase):

	username = 'foo'
	password = 'man'
	new_pass = '54321'
	tmp_pass = 'man'
	level = 10

	def setUp(self):
		app.app.testing = True
		self.app = app.app.test_client()

	def tearDown(self):
		pass

	def open_with_auth(self, url, method):
		return self.app.open(url, method=method,
			headers={
			'Authorization': 'Basic ' + base64.b64encode(bytes(self.username + ":" + self.password, 'ascii')).decode('ascii')
			}
			)

	def open_with_auth_2(self, url, method):
		return self.app.open(url, method=method,
			headers={
			'Authorization': 'Basic ' + base64.b64encode(bytes(self.username + ":" + self.new_pass, 'ascii')).decode('ascii')
			}
			)

	def add_user_1_0(self, username, password, level):
		return self.app.post('/api/v1.0/user/add/', data=json.dumps(dict(
			username = username,
			password = password,
			level = level)), content_type='application/json', follow_redirects=True)

	def add_user_1_1(self, username, password, level):
		return self.app.post('/api/v1.1/user/add/', data=json.dumps(dict(
			username = username,
			password = password,
			level = level)), content_type='application/json', follow_redirects=True)

	def test_add_user_1_0(self):
		rv = self.add_user_1_0(self.username, self.password, '12')
		assert b'"username": "foo"' in rv.data
		assert b'"level": 12' in rv.data
		assert rv.status_code == 200

	def test_add_user_1_0_fail(self):
		pass

	def test_add_user_1_1(self):
		rv = self.add_user_1_1('foo1', 'man1', '13')
		assert b'"username": "foo1"' in rv.data
		assert b'"level": 13' in rv.data
		assert rv.status_code == 200

	def test_add_user_1_1_fail(self):
		pass

	def update_pass_1_0(self, passwd):
		return self.open_with_auth('/api/v1.0/user/update_pass/'+passwd, 'PUT')

	def update_pass_1_1(self, passwd):
		return self.open_with_auth_2('/api/v1.1/user/update_pass/'+passwd, 'PUT')

	def test_update_pass_1_0(self):
		rv = self.update_pass_1_0(self.new_pass)
		assert b'"password": "54321"' in rv.data
		assert rv.status_code == 200

	def test_update_pass_1_1(self):
		rv = self.update_pass_1_1(self.tmp_pass)
		assert b'"password": "man"' in rv.data
		assert rv.status_code == 200
		self.password = self.tmp_pass

if __name__ == '__main__':
	unittest.main()
