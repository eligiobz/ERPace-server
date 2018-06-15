# -*- coding:utf-8 -*-

import os
import app
import unittest
import tempfile
import base64
import json
from models import engine, Base


class UsersTestCase(unittest.TestCase):

    username = 'foo'
    password = 'man'
    new_pass = '54321'
    tmp_pass = 'man1'
    level = 10

    auth_string = 'Basic ' + \
        base64.b64encode(bytes('carlo' + ":" + '123', 'ascii')).decode('ascii')
    ClasIsSetup = False

    def setupClass(self):
        engine.execute("delete from operation_logs;")
        unittest.TestCase.setUp(self)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        if not self.ClasIsSetup:
            print("Initalizing testing environment")
            self.setupClass()
            self.__class__.ClasIsSetup = True

    def open_with_auth(self, url, method, username=None, password=None, data=None):
        if username is None and password is None:
            f_auth_string = self.auth_string
        else:
            f_auth_string = 'Basic ' + \
                base64.b64encode(
                    bytes(username + ":" + password, 'ascii')).decode('ascii')
        return self.app.open(url, method=method,
                             headers={'Authorization': f_auth_string},
                             data=data,
                             content_type='application/json'
                             )

    def add_user_1_0(self, data):
        return self.app.post('/api/v1.0/user/add/', data=json.dumps(data),
                             content_type='application/json', follow_redirects=True)

    def add_user_1_1(self, data):
        return self.app.post('/api/v1.1/user/add/', data=json.dumps(data),
                             content_type='application/json', follow_redirects=True)

    def update_pass_1_0(self, passwd):
        return self.open_with_auth('/api/v1.0/user/update_pass/' + passwd, 'PUT', 'foo1', self.tmp_pass)

    def update_pass_1_1(self, passwd):
        return self.open_with_auth('/api/v1.1/user/update_pass/' + passwd, 'PUT', 'foo1', self.new_pass)

    def delete_user_1_1(self, user):
        return self.open_with_auth('/api/v1.1/user/delete/' + user, 'DELETE', self.username, self.password)

    def check_login_1_0(self, user, passwd):
        return self.open_with_auth('/api/v1.0/user/check_login/', 'GET', user, passwd)

    def check_login_1_1(self, user, passwd):
        return self.open_with_auth('/api/v1.1/user/check_login/', 'GET', user, passwd)

    def test_001_add_user_1_0(self):
        user = dict(
            username=self.username,
            password=self.password,
            level=self.level)
        response = self.add_user_1_0(user)
        assert b'"username": "foo"' in response.data
        assert b'"level": 10' in response.data
        assert response.status_code == 200

    def test_002_add_user_1_1(self):
        user = dict(
            username='foo1',
            password=self.tmp_pass,
            level=13)
        response = self.add_user_1_1(user)
        assert b'"username": "foo1"' in response.data
        assert b'"level": 13' in response.data
        assert response.status_code == 200

    def test_003_add_user_1_0_fail(self):
        user = dict(
            username=None,
            password=None,
            level=None)
        response = self.add_user_1_0(user)
        assert response.status_code == 406
        user = dict(
            username='',
            password='',
            level='')
        response = self.add_user_1_0(user)
        assert response.status_code == 406
        user = dict(
            username="",
            password="",
            level="")
        response = self.add_user_1_0(user)
        assert response.status_code == 406

    def test_004_add_user_1_1_fail(self):
        user = dict(
            username=None,
            password=None,
            level=None)
        response = self.add_user_1_1(user)
        assert response.status_code == 406
        user = dict(
            username='',
            password='',
            level='')
        response = self.add_user_1_1(user)
        assert response.status_code == 406
        user = dict(
            username="",
            password="",
            level="")
        response = self.add_user_1_1(user)
        assert response.status_code == 406

    def test_005_update_pass_1_0(self):
        response = self.update_pass_1_0(self.new_pass)
        assert b'"password": "54321"' in response.data
        assert response.status_code == 200

    def test_006_update_pass_1_1(self):
        response = self.update_pass_1_1(self.tmp_pass)
        assert b'"password": "man1"' in response.data
        assert response.status_code == 200

    def test_007_check_login_1_0_success(self):
        response = self.check_login_1_0(self.username, self.password)
        assert response.status_code == 200

    def test_008_check_login_1_1_sucess(self):
        response = self.check_login_1_0(self.username, self.password)
        assert response.status_code == 200

    def test_009_check_login_1_0_fail_wrong_passwd(self):
        response = self.check_login_1_0(self.username, 'fakepass')
        assert response.status_code == 401

    def test_010_check_login_1_1_fail_wrong_passwd(self):
        response = self.check_login_1_1(self.username, 'fakepass')
        assert response.status_code == 401

    def test_011_add_user_1_0_fail_missing_data(self):
        user = dict(
            username=self.username,
            password='fakepass')
        response = self.add_user_1_0(user)
        assert response.status_code == 406

    def test_012_add_user_1_1_fail_missing_data(self):
        user = dict(
            username=self.username,
            password='fakepass')
        response = self.add_user_1_1(user)
        assert response.status_code == 406

    def test_013_delete_fail_user_non_existent(self):
        response = self.delete_user_1_1('fake_user')
        assert response.status_code == 404

    def test_009_check_login_1_0_fail_non_existing_user(self):
        response = self.check_login_1_0('fake_user', 'fakepass')
        assert response.status_code == 401

    def test_010_check_login_1_1_fail_non_existing_user(self):
        response = self.check_login_1_1('fake_user', 'fakepass')
        assert response.status_code == 401

    def test_999_delete_user_1_1(self):
        response = self.delete_user_1_1('foo1')
        assert response.status_code == 200
        assert b'deleted' in response.data
        response = self.delete_user_1_1('foo')
        assert response.status_code == 200
        assert b'deleted' in response.data

if __name__ == '__main__':
    unittest.main()
