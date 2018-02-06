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
	tmp_pass = 'man1'
	level = 10

	def setUp(self):
		app.app.testing = True
		self.app = app.app.test_client()

	def tearDown(self):
		pass
		
	def open_with_auth(self, url, method, username, password):
		return self.app.open(url, method=method,
			headers={
			'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" +password, 'ascii')).decode('ascii')
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

	def update_pass_1_0(self, passwd):
		return self.open_with_auth('/api/v1.0/user/update_pass/'+passwd, 'PUT', 'foo1', self.tmp_pass)

	def update_pass_1_1(self, passwd):
		return self.open_with_auth('/api/v1.1/user/update_pass/'+passwd, 'PUT', 'foo1', self.new_pass)

	def delete_user_1_1(self, user):
		return self.open_with_auth('api/v1.1/user/delete/'+user, 'DELETE', self.username, self.password)

	def test_001_add_user_1_0(self):
		response = self.add_user_1_0(self.username, self.password, self.level)
		assert b'"username": "foo"' in response.data
		assert b'"level": 10' in response.data
		assert response.status_code == 200

	def test_002_add_user_1_1(self):
		response = self.add_user_1_1('foo1', self.tmp_pass, '13')
		assert b'"username": "foo1"' in response.data
		assert b'"level": 13' in response.data
		assert response.status_code == 200

	def test_003_add_user_1_0_fail(self):
		response = self.add_user_1_0(None, None, None)
		assert response.status_code == 406
		response = self.add_user_1_0('', '', '')
		assert response.status_code == 406
		response = self.add_user_1_0("", "", "")
		assert response.status_code == 406

	def test_004_add_user_1_1_fail(self):
		response = self.add_user_1_0(None, None, None)
		assert response.status_code == 406
		response = self.add_user_1_0('', '', '')
		assert response.status_code == 406
		response = self.add_user_1_0("", "", "")
		assert response.status_code == 406

	def test_005_update_pass_1_0(self):
		response = self.update_pass_1_0(self.new_pass)
		assert b'"password": "54321"' in response.data
		assert response.status_code == 200

	def test_006_update_pass_1_1(self):
		response = self.update_pass_1_1(self.tmp_pass)
		assert b'"password": "man1"' in response.data
		assert response.status_code == 200

	def test_007_delete_user_1_1(self):
		response = self.delete_user_1_1('foo1')
		assert response.status_code == 200
		assert b'deleted' in response.data
		response = self.delete_user_1_1('foo')
		assert response.status_code == 200
		assert b'deleted' in response.data

if __name__ == '__main__':
	unittest.main()
