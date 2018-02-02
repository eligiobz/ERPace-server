import os
import app
import unittest
import tempfile

DATABASE_URL = "postgres://postgres:38ae14e484825f8d9daa918c695617bc@quimerabjx.org:30249/mobilerp_testing"

class FlaskrTestCase(unittest.TestCase):

	def setUp(self):
		app.app.config['DATABASE'] = DATABASE_URL
		app.app.testing = True
		self.app = app.app.test_client()
		#with flaskr.app.app_context():
			#flaskr.init_db()

	def tearDown(self):
		pass

	def test_deployment(self):
		rv = self.app.get('/')
		assert b'Welcome to instance xxx' in rv.data

	def add_user(self, username, password, level):
		return self.app.post('/api/v1.0/users/', data={
			'user' : username,
			'pass' : password,
			'level' : level}, follow_redirects=True)

	def add_user(self, username, password, level):
		return self.app.post('/api/v1.1/users/', data={
			'user' : username,
			'pass' : password,
			'level' : level}, follow_redirects=True)

	def test_add_user_1_0(self):
		rv = self.add_user('foo', 'man', '12')
		print (rv.data)
		assert rv.status_code == 200

	def test_add_user_1_1(self):
		rv = self.add_user('foo', 'man', '12')
		print (rv.data)
		assert rv.status_code == 200

if __name__ == '__main__':
	unittest.main()
