# -*- coding:utf-8 -*-

import os
import app
import unittest
import tempfile
import base64
import json
from datetime import date as ddate, timedelta
from jsoncompare import jsoncompare
from models.MasterList import MasterList as MasterList
from models.Product import Product as Product
from models import db_session as db_session, engine, Base


class SalesTestCase(unittest.TestCase):

    auth_string = 'Basic ' + \
        base64.b64encode(bytes('carlo' + ":" + '123', 'ascii')).decode('ascii')
    ClasIsSetup = False

    json_prod_1 = dict(
        barcode='0001',
        price=50.50,
        units=6,
        name='prod_1',
        storeid=1)

    json_prod_2 = dict(
        barcode='0002',
        price=1,
        units=8,
        name='prod_2',
        storeid=1)

    json_prod_3 = dict(
        barcode='0003',
        price=150,
        units=8,
        name='prod_3',
        storeid=2)

    json_serv_1 = dict(
        barcode='0004',
        price=3.40,
        name='serv_1')

    json_serv_2 = dict(
        barcode='0005',
        price=200,
        name='serv_2')

    json_serv_3 = dict(
        barcode='0006',
        price=1,
        name='serv_3')

    def setupClass(self):
        response = self.open_with_auth('/api/v1.1/daily_report/', 'GET')
        assert response.status_code == 500
        engine.execute("delete from operation_logs;")
        engine.execute(
            "insert into drugstore(id, name) values (1, 'default');")
        engine.execute(
            "insert into drugstore(id, name) values (2, 'Store 2');")
        engine.execute(
            "insert into sale(date) values((CURRENT_DATE - 28) + interval '1 hour');")
        engine.execute("insert into saledetails(idsale, idproduct, productprice, units, storeid)\
						select MAX(sale.id), '0001', 50.50, 2, 1 from sale;")
        engine.execute(
            "update product set units=units-2 where storeid = 1 and barcode='0001'")
        engine.execute(
            "insert into sale(date) values((CURRENT_DATE - 15) + interval '1 hour');")
        engine.execute("insert into saledetails(idsale, idproduct, productprice, units, storeid)\
						select MAX(sale.id), '0003', 1, 2, 2 from sale;")
        engine.execute(
            "update product set units=units-2 where storeid = 1 and barcode='0003'")

        self.add_product_1_1(self.json_prod_1)
        self.add_product_1_1(self.json_prod_2)
        self.add_product_1_1(self.json_prod_3)
        self.add_service_1_1(self.json_serv_1)
        self.add_service_1_1(self.json_serv_2)
        self.add_service_1_1(self.json_serv_3)

        self.setUpSales()
        unittest.TestCase.setUp(self)

    @classmethod
    def tearDownClass(cls):
        engine.execute('delete from saledetails; delete from sale; delete from\
						products_price_history; delete from product; delete from products_masterlist ;')
        engine.execute("delete from services; delete from drugstore;")

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
                             data=json.dumps(data),
                             content_type='application/json'
                             )

    def add_product_1_1(self, data):
        return self.open_with_auth('/api/v1.1/add_product/', 'POST', data)

    def add_service_1_1(self, data):
        return self.open_with_auth('/api/v1.1/add_service/', 'POST', data)

    def make_sale_1_1(self, data):
        return self.open_with_auth('/api/v1.1/make_sale/', 'POST', data)

    def setUpSales(self):
        sale_1 = dict(
            barcode=['0001', '0002'],
            units=[4, 4],
            is_service=[0, 0],
            storeid=1,
            token="fsda"
        )
        sale_2 = dict(
            barcode=['0003', '0004'],
            units=[6, 1],
            is_service=[0, 1],
            storeid=2,
            token="jlk"
        )
        sale_3 = dict(
            barcode=['0005', '0006'],
            units=[4, 4],
            is_service=[1, 1],
            storeid=1,
            token="fsdajlk"
        )
        response = self.make_sale_1_1(sale_1)
        assert response.status_code == 200
        response = self.make_sale_1_1(sale_2)
        assert response.status_code == 200
        response = self.make_sale_1_1(sale_3)
        assert response.status_code == 200

    def test_001_get_daily_report(self):
        response = self.open_with_auth('/api/v1.1/daily_report/', 'GET')
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert json_data['mobilerp']['totalItemsSold'] == 23
        assert json_data['mobilerp']['totalSales'] == 3
        assert json_data['mobilerp']['totalEarnings'] == (
            (self.json_prod_1["price"] * 4) +
            (self.json_prod_2["price"] * 4) +
            (self.json_prod_3["price"] * 6) +
            (self.json_serv_1["price"] * 1) +
            (self.json_serv_2["price"] * 4) +
            (self.json_serv_3["price"] * 4)
        )
        assert "sales" not in json_data['mobilerp']

    def test_002_get_monthly_report(self):
        response = self.open_with_auth('/api/v1.1/monthly_report/', 'GET')
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert json_data['mobilerp']['totalItemsSold'] == 27
        assert json_data['mobilerp']['totalSales'] == 5
        assert "sales" not in json_data['mobilerp']
        assert json_data['mobilerp']['totalEarnings'] == (
            (self.json_prod_1["price"] * 4) +
            (self.json_prod_2["price"] * 4) +
            (self.json_prod_3["price"] * 6) +
            (self.json_serv_1["price"] * 1) +
            (self.json_serv_2["price"] * 4) +
            (self.json_serv_3["price"] * 4) +
            (self.json_prod_1["price"] * 2) +
            (self.json_prod_2["price"] * 2)
        )

    def test_003_get_custom_report(self):
        end = ddate.today()
        init = ddate.today() - timedelta(days=16)
        response = self.open_with_auth(
            '/api/v1.1/custom_report/' + str(init) + '/' + str(end), 'GET')
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert json_data['mobilerp']['totalSales'] == 4
        assert json_data['mobilerp']['totalItemsSold'] == 25
        assert json_data['mobilerp']['totalEarnings'] == (
            (self.json_prod_1["price"] * 4) +
            (self.json_prod_2["price"] * 4) +
            (self.json_prod_3["price"] * 6) +
            (self.json_serv_1["price"] * 1) +
            (self.json_serv_2["price"] * 4) +
            (self.json_serv_3["price"] * 4) +
            (self.json_prod_2["price"] * 2)
        )
        assert 'sales' not in json_data['mobilerp']

    def test_004_get_custom_report_fail_invalid_dates(self):
        """
        Tests that checks for failure when init date is larger
        than end date
        """
        init = ddate.today() + timedelta(days=1)
        end = ddate.today()
        response = self.open_with_auth(
            '/api/v1.1/custom_report/' + str(init) + '/' + str(end), 'GET')
        assert response.status_code == 400

    def test_005_get_custom_report_fail_invalid_dates(self):
        """
        Tests that checks for failure when end date is in the future
        """
        init = ddate.today()
        end = ddate.today() + timedelta(days=1)
        response = self.open_with_auth(
            '/api/v1.1/custom_report/' + str(init) + '/' + str(end), 'GET')
        assert response.status_code == 400


if __name__ == "__main__":
    unittest.main()
