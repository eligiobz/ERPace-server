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

from models import db_session
from models.Product import Product as Product
from models.PriceHistory import PriceHistory as PriceHistory

from . import auth, api


@api.route('/v1.0/findProduct/<bCode>', methods=['GET'])
@auth.login_required
def findProduct(bCode):
    product = Product.query.filter_by(barcode=bCode).first()
    if (product is None):
        abort(404)
    else:
        return make_response(jsonify({'mobilerp': [product.serialize]}), 200)


@api.route('/v1.0/listProducts/', methods=['GET'])
@auth.login_required
def listProducts():
    print (request)
    products = Product.query.all()
    if products is None:
        abort(400)
    return make_response(jsonify({'mobilerp':
                         [p.serialize for p in products]}), 200)


@api.route('/v1.0/newProduct/', methods=['POST'])
@auth.login_required
def newProduct():
    if not request.json or 'barcode' not in request.json\
       or 'units' not in request.json or 'price' not in request.json\
       or 'name' not in request.json:
        abort(400)
    p = Product(request.json['barcode'], request.json['name'],
                request.json['units'], request.json['price'])
    db_session.add(p)
    db_session.commit()
    return make_response(jsonify({'mobilerp': [p.serialize]}), 200)


@api.route('/v1.0/updateProduct/<int:bCode>', methods=['PUT'])
@auth.login_required
def updateProduct(bCode):
    if not request.json:
        abort(400)
    p = Product.query.filter_by(barcode=bCode).first()
    if p is None:
        abort(404)
    if 'price' in request.json:
        if str(p.price) != request.json['price']:
            price_update = PriceHistory(p.barcode)
            db_session.add(price_update)
            db_session.commit()
            p.price = float(request.json['price'])
    if 'units' in request.json:
        p.units = p.units + int(request.json['units'])
    db_session.add(p)
    db_session.commit()
    return make_response(jsonify({'mobilerp': [p.serialize]}), 200)


@api.route('/v1.0/listDepletedProducts/', methods=['GET'])
@auth.login_required
def listDepletedProducts():
    products = Product.query.filter_by(units=0).all()
    if products is None:
        abort(400)
    return make_response(jsonify({'mobilerp':
                         [p.serialize for p in products]}), 200)
