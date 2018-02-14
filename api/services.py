# -*- coding:utf-8 -*-

##############################################################################
# MobilEPR - A small self-hosted ERP that works with your smartphone.
# Copyright (C) 2018  Eligio Becerra
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
from models.PriceHistory import ServicePriceHistory as PriceHistory
from models.views import DepletedItems
from models.MasterList import MasterList as MasterList
from models.Service import Service as Service

from reporter.pdfgenerator import generateDepletedReport
from . import auth, api
from . import logger

@api.route('/v1.1/find_service/<bCode>', methods=['GET'])
@auth.login_required
def find_service(bCode, storeid=None):
    service = Service.query.filter_by(barcode=bCode).first()
    if service is None:
        abort(404)
    else:
        return make_response(jsonify( { "mobilerp" :service.serialize} ), 200)

@api.route('/v1.1/list_services/', methods=['GET'])
@auth.login_required
def list_services():
    services = Service.query.order_by(Service.name.asc()).all()
    if services is None or len(services) == 0: 
       abort(412, "Por alguna razon la lista esta vacia")
    return make_response(jsonify( { "mobilerp" :[p.serialize for p in services] }), 200)


@api.route('/v1.1/add_service/', methods=['POST'])
@auth.login_required
def add_service():
    if not request.json or 'barcode' not in request.json\
       or 'price' not in request.json or 'name' not in request.json :
        abort(400)
    if not request.json['barcode'] or not request.json['name']\
       or not request.json['price']:
        abort(400)
    if (logger.log_op(request.json)):
        m = MasterList.query.filter_by(barcode=request.json['barcode']).first()
        if m is not None:
            abort(409, { "message" : "Servicio existente" })
        m = Service(request.json['barcode'], request.json['name'],
            request.json['price'])
        db_session.add(m)
        db_session.commit()
        return make_response(jsonify( { "mobilerp" :m.serialize} ), 200)
    else:
        return make_response(jsonify({'mobilerp': 'Operacion duplicada, saltando'}), 428)


@api.route('/v1.1/update_service/<bCode>', methods=['PUT'])
@auth.login_required
def update_service_1_1(bCode):
    if not request.json:
        abort(400)
    m = Service.query.filter_by(barcode=bCode).first()
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
        return make_response(jsonify( { "mobilerp" :m.serialize} ), 200)
    else:
        return make_response(jsonify({'mobilerp': 'Operacion duplicada, saltando'}), 428)

@api.route('/v1.1/service_price_history/<bCode>', methods=['GET'])
@auth.login_required
def service_price_hisorty(bCode):
    # TODO Implement
    abort(501)
