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

from flask import abort, jsonify, make_response, request

from models import db_session, engine
from models.Product import Product as Product
from models.PriceHistory import ProductPriceHistory as PriceHistory
from models.views import DepletedItems
from models.MasterList import MasterList as MasterList
from models.ProductsMasterlist import ProductsMasterlist as ProductsMasterlist
from models.views import ProductStore as ProductStore
from models.DrugStores import Drugstore

from reporter.pdfgenerator import generateDepletedReport
from . import auth, api
from . import logger


@api.route('/v1.0/find_product/<bCode>', methods=['GET'])
@api.route('/v1.1/find_product/<storeid>/<bCode>', methods=['GET'])
@auth.login_required
def find_product(bCode, storeid=1):
    rule = request.url_rule
    product = ProductStore.query.filter_by(barcode=bCode).\
        filter_by(storeid=storeid).first()
    valid_store = Drugstore.query.filter_by(id=storeid).first()
    if valid_store is None:
        abort(406)
    if product is None and '/v1.1/' in rule.rule:
        product = MasterList.query.filter_by(barcode=bCode).first()
    if product is None:
        abort(404)
    else:
        if isinstance(product, MasterList):
            data = product.serialize
            data['units'] = 0
            return make_response(jsonify({"mobilerp": data}), 200)
        else:
            return make_response(jsonify({"mobilerp": product.serialize}), 200)


@api.route('/v1.0/list_products/', methods=['GET'])
@api.route('/v1.1/list_products/<int:storeid>', methods=['GET'])
@auth.login_required
def list_products(storeid=None):
    if storeid is None:
        products = ProductStore.query.filter_by(
            storeid=1).order_by(ProductStore.name.asc()).all()
    else:
        products = ProductStore.query.filter_by(
            storeid=storeid).order_by(ProductStore.name.asc()).all()
    if products is None or len(products) == 0:
        abort(412, "Por alguna razon la lista esta vacia")
    return make_response(jsonify({"mobilerp": [p.serialize for p in products]}), 200)


@api.route('/v1.0/add_product/', methods=['POST'])
@auth.login_required
def add_product_1_0():
    if not request.json or 'barcode' not in request.json\
       or 'units' not in request.json or 'price' not in request.json\
       or 'name' not in request.json:
        abort(400)
    if not request.json['barcode'] or not request.json['name']\
       or not request.json['units'] or not request.json['price']:
        abort(400)
    if (logger.log_op(request.json)):
        m = MasterList.query.filter_by(barcode=request.json['barcode']).first()
        if m is not None:
            abort(409, {"message": "Producto existente"})
        m = ProductsMasterlist(request.json['barcode'], request.json['name'],
                               request.json['price'])
        db_session.add(m)
        db_session.commit()
        p = Product(request.json['barcode'], request.json['units'],
                    1)
        db_session.add(p)
        db_session.commit()
        prod = ProductStore.query.filter_by(
            barcode=request.json['barcode']).filter_by(storeid=1).first()
        return make_response(jsonify({"mobilerp": prod.serialize}), 200)
    else:
        return make_response(jsonify({'mobilerp': 'Operacion duplicada, saltando'}), 428)


@api.route('/v1.0/update_product/<bCode>', methods=['PUT'])
@auth.login_required
def update_product_1_0(bCode):
    if not request.json:
        abort(400)
    p = Product.query.filter_by(barcode=bCode).first()
    mlist = ProductsMasterlist.query.filter_by(barcode=bCode).first()
    if p is None:
        abort(400)
    if (logger.log_op(request.json)):
        if 'price' in request.json:
            if str(mlist.price) != request.json['price']:
                price_update = PriceHistory(p.barcode)
                db_session.add(price_update)
                db_session.commit()
                mlist.price = float(request.json['price'])
                db_session.add(mlist)
                db_session.commit()
        if 'units' in request.json:
            p.units = p.units + int(request.json['units'])
        if 'name' in request.json:
            mlist = ProductsMasterlist.query.filter_by(barcode=bCode).first()
            mlist.name = request.json['name']
            db_session.add(mlist)
        db_session.add(p)
        db_session.commit()
        ps = ProductStore.query.filter_by(
            storeid=1).filter_by(barcode=bCode).first()
        return make_response(jsonify({"mobilerp": ps.serialize}), 200)
    else:
        return make_response(jsonify({'mobilerp': 'Operacion duplicada, saltando'}), 428)


@api.route('/v1.0/list_depleted_products/', methods=['GET'])
@auth.login_required
def list_depleted_products_1_0():
    products = DepletedItems.query.all()
    if products is None or len(products) <= 0:
        abort(400)
    data = {'mobilerp': [p.serialize for p in products]}
    generateDepletedReport(data)
    return make_response(jsonify({"mobilerp": [p.serialize for p in products]}), 200)

################################## V1.1 #######################################


@api.route('/v1.1/add_product/', methods=['POST'])
@auth.login_required
def add_product_1_1():
    if not request.json or 'barcode' not in request.json\
       or 'units' not in request.json or 'price' not in request.json\
       or 'name' not in request.json or 'storeid' not in request.json:
        abort(400)
    if not request.json['barcode'] or not request.json['name']\
       or not request.json['units'] or not request.json['price']\
       or not request.json['storeid']:
        abort(400)
    drugstore = Drugstore.query.filter_by(id=request.json['storeid']).first()
    if drugstore is None:
        abort(400)
    if (logger.log_op(request.json)):
        m = MasterList.query.filter_by(barcode=request.json['barcode']).first()
        if m is not None:
            abort(409, {"message": "Producto existente"})
        m = ProductsMasterlist(request.json['barcode'], request.json['name'],
                               request.json['price'])
        db_session.add(m)
        db_session.commit()
        p = Product(request.json['barcode'], request.json['units'],
                    request.json['storeid'])
        db_session.add(p)
        db_session.commit()
        prod = ProductStore.query.filter_by(barcode=request.json['barcode']).filter_by(
            storeid=request.json['storeid']).first()
        return make_response(jsonify({"mobilerp": prod.serialize}), 200)
    else:
        return make_response(jsonify({'mobilerp': 'Operacion duplicada, saltando'}), 428)


@api.route('/v1.1/update_product/<bCode>', methods=['PUT'])
@auth.login_required
def update_product_1_1(bCode):
    if not request.json or 'storeid' not in request.json:
        abort(400)
    m = ProductsMasterlist.query.filter_by(barcode=bCode).first()
    if m is None:
        abort(400)
    if (logger.log_op(request.json)):
        if 'price' in request.json:
            if str(m.price) != request.json['price']:
                price_update = PriceHistory(m.barcode)
                db_session.add(price_update)
                db_session.commit()
                m.price = float(request.json['price'])
        if 'name' in request.json:
            m.name = request.json['name']
        db_session.add(m)
        db_session.commit()
        p = None
        if 'units' in request.json:
            engine.execute(updateHelper(bCode, int(
                request.json['units']), int(request.json['storeid'])))
        else:
            engine.execute(updateHelper(
                bCode, 0, int(request.json['storeid'])))
        ps = ProductStore.query.filter_by(barcode=bCode).filter_by(
            storeid=request.json['storeid']).first()
        return make_response(jsonify({"mobilerp": ps.serialize}), 200)
    else:
        return make_response(jsonify({'mobilerp': 'Operacion duplicada, saltando'}), 428)


@api.route('/v1.1/list_depleted_products/<storeid>', methods=['GET'])
@auth.login_required
def list_depleted_products_1_1(storeid):
    products = DepletedItems.query.filter_by(storeid=int(storeid)).all()
    if products is None or len(products) <= 0:
        abort(400)
    data = {'mobilerp': [p.serialize for p in products]}
    generateDepletedReport(data)
    return make_response(jsonify({"mobilerp": [p.serialize for p in products]}), 200)


def updateHelper(barcode, units, storeid):
    p = Product.query.filter_by(storeid=storeid, barcode=barcode).first()
    if p is None:
        p = Product(barcode, 0, storeid)
    u = p.units + units
    db_session.add(p)
    db_session.commit()
    return "UPDATE product set units={0} where barcode='{1}' and storeid={2}"\
        .format(u, barcode, storeid)


@api.route('/v1.1/product_price_history/<bCode>', methods=['GET'])
@auth.login_required
def product_price_hisorty(bCode):
    # TODO Implement
    abort(501)
