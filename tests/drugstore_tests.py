# -*- coding:utf-8 -*-

import os
import app
import unittest
import tempfile
import base64
import json
from jsoncompare import jsoncompare
from models import db_session as db_session, engine, Base


class DrugstoreTestCase(unittest.TestCase):

    auth_string = 'Basic ' + \
        base64.b64encode(bytes('carlo' + ":" + '123', 'ascii')).decode('ascii')
    ClasIsSetup = False

    drugstore_1 = json.dumps({
        'name': 'Store 1'
    })

    drugstore_2 = json.dumps({
        'name': 'Store 2'
    })

    def setupClass(self):
        engine.execute("delete from drugstore;")
        unittest.TestCase.setUp(self)

    @classmethod
    def tearDownClass(cls):
        engine.execute("delete from drugstore;")

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        if not self.ClasIsSetup:
            print("Initalizing testing environment")
            self.setupClass()
            self.__class__.ClasIsSetup = True

    def open_with_auth(self, url, method, data=None):
        return self.app.open(url, method=method,
                             headers={'Authorization': self.auth_string},
                             data=data,
                             content_type='application/json'
                             )

    def add_drugstore(self, data):
        return self.open_with_auth('/api/v1.1/add_drugstore/', 'POST', data)

    def test_001_add_drugstore(self):
        response = self.add_drugstore(self.drugstore_1)
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert jsoncompare.are_same(
            json_data["mobilerp"], self.drugstore_1, False, ['id'])
        response = self.add_drugstore(self.drugstore_2)
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert jsoncompare.are_same(
            json_data["mobilerp"], self.drugstore_2, False, ['id'])

    def test_002_list_drugstores(self):
        response = self.open_with_auth('/api/v1.1/list_drugstores/', 'GET')
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert len(json_data["mobilerp"]) == 2

    def test_003_edit_drugstore(self):
        response = self.open_with_auth('/api/v1.1/list_drugstores/', 'GET')
        assert response.status_code == 200
        json_data = json.loads(response.data)
        i = 2
        for item in json_data["mobilerp"]:
            new_json = json.dumps({
                'name': 'Store X' + str(i),
                'id': item['id']
            })
            response = self.open_with_auth(
                '/api/v1.1/edit_drugstore/', 'PUT', new_json)
            assert response.status_code == 200
            new_data = json.loads(response.data)
            assert jsoncompare.are_same(new_data, new_json)
            i = i + 1

    def test_004_add_drugstore_fail_no_data(self):
        response = self.add_drugstore(json.dumps(None))
        assert response.status_code == 406

    """
		Disabled until further notice
	"""
    # def test_005_add_drugstore_fail_empty_data(self):
    # 	data = dict(
    # 		name = None)
    # 	response = self.add_drugstore(json.dumps(data))
    # 	assert response.status_code == 400
    # 	data = dict(
    # 		name = '')
    # 	response = self.add_drugstore(json.dumps(data))
    # 	assert response.status_code == 400

    def test_006_edit_drugstore_fail_no_data(self):
        response = self.open_with_auth(
            '/api/v1.1/edit_drugstore/', 'PUT', json.dumps(None))
        assert response.status_code == 406

    def test_007_edit_drugstore_fail_empty_data(self):
        data = dict(
            name=None)
        response = self.open_with_auth(
            '/api/v1.1/edit_drugstore/', 'PUT', json.dumps(data))
        assert response.status_code == 406
        data = dict(
            name='')
        response = self.open_with_auth(
            '/api/v1.1/edit_drugstore/', 'PUT', json.dumps(data))
        assert response.status_code == 406

    def test_008_edit_drugstore_fail_incomplete_data(self):
        data = dict(
            name="")
        response = self.open_with_auth(
            '/api/v1.1/edit_drugstore/', 'PUT', json.dumps(data))
        assert response.status_code == 406
        data = dict(
            id=1)
        response = self.open_with_auth(
            '/api/v1.1/edit_drugstore/', 'PUT', json.dumps(data))
        assert response.status_code == 406

if __name__ == "__main__":
    unittest.main()
