# -*- coding:utf-8 -*-

##############################################################################
# MobilEPR - A small self-hosted ERP that works with your smartphone.
# Copyright (C) 2017-2018  Eligio Becerra
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

from flask import abort, make_response, request, jsonify

from models import db_session, engine
from models.Product import Product
from models.MasterList import MasterList
from models.views import ProductStore
from models.Sale import Sale
from models.SaleDetails import SaleDetails
from models.DrugStores import Drugstore
# from models.PriceHistory import PriceHistory
from models.Service import Service

from . import api, auth, logger

@api.route('/v1.1/find_article/<barcode>', methods=['GET'])
@api.route('/v1.1/find_article/<barcode>/<storeid>', methods=['GET'])
@auth.login_required
def find_article(barcode, storeid=None):
    if not barcode:
        abort(404)
    print("Will look  for product?")
    if storeid is not None:
        print("Looking for product")
        article = ProductStore.query.filter_by(barcode=barcode)\
            .filter_by(storeid=storeid).first()
    if article is None:
        print("Looking for service")
        article  = Service.query.filter_by(barcode=barcode)\
            .first()
    if article is None:
        abort(404)
    return make_response (jsonify({"mobilerp" : article.serialize}), 200)
    # article = MasterList.query

@api.route('/v1.0/make_sale/', methods=['POST'])
@auth.login_required
def make_sale_1_0():
    if not request.json:
        abort(400)
    if 'barcode' not in request.json or len(request.json['barcode']) <= 0 or\
        'units' not in request.json or len(request.json['units']) <= 0 or\
        'is_service' not in request.json or len(request.json['is_service']) <= 0:
        abort(400)
    if (logger.log_op(request.json)):
        s = Sale()
        db_session.add(s)
        db_session.commit()
        for i in range(0, len(request.json['barcode'])):
            if int(request.json['is_service'][i]) == 0:
                bCode = request.json['barcode'][i]
                units = request.json['units'][i]
                ps = ProductStore.query.filter_by(barcode=bCode).filter_by(storeid=1).first()
                if (ps.units - units < 0):
                    abort(406, {"message": 'articulos insuficientes'})
                else:
                    q = updateHelper(bCode, units, 1)
                    engine.execute(q)
                    sd = SaleDetails(s.id, ps.barcode, ps.price, units, 1)
                    db_session.add(sd)
                    db_session.commit()
            elif int(request.json['is_service'][i]) == 1:
                bCode = request.json['barcode'][i]
                units = request.json['units'][i]
                ps = MasterList.query.filter_by(barcode=bCode).first()
                sd = SaleDetails(s.id, ps.barcode, ps.price, units, 1)
                db_session.add(sd)
                db_session.commit()
            else:
                abort(400)
        sd = SaleDetails.query.filter_by(idsale=s.id).all()
        return make_response(jsonify( { "mobilerp" :[sd_.serialize for sd_ in sd] } ), 200)
    else:
        return make_response(jsonify({'mobilerp': 'Operacion duplicada, saltando'}), 428)

################################## V1.1 #######################################

@api.route('/v1.1/make_sale/', methods=['POST'])
@auth.login_required
def make_sale_1_1():
    if not request.json or 'storeid' not in request.json or\
        'barcode' not in request.json or len(request.json['barcode']) <= 0 or\
        'is_service' not in request.json or len(request.json['is_service']) <= 0:
        abort(400)
    drugstore = Drugstore.query.filter_by(id=request.json['storeid']).first()
    if drugstore is None:
        abort (406, { "message" : "storeid invalido"})
    if (logger.log_op(request.json)):
        s = Sale()
        db_session.add(s)
        db_session.commit()
        for i in range(0, len(request.json['barcode'])):
            if int(request.json['is_service'][i]) == 0:
                bCode = request.json['barcode'][i]
                units = request.json['units'][i]
                m = MasterList.query.filter_by(barcode=bCode).first()
                ps = Product.query.filter_by(barcode=bCode).\
                    filter_by(storeid=request.json['storeid']).first()
                if ps is None:
                    abort(406, {"message": 'Uno de tus articulos no existe'})
                if (ps.units - units < 0):
                    abort(406, {"message": 'articulos insuficientes'})
                else:
                    q = updateHelper(bCode, units, request.json['storeid'])
                    engine.execute(q)
                    sd = SaleDetails(s.id, m.barcode, m.price, units, request.json['storeid'])
                    db_session.add(sd)
                    db_session.commit()
            elif int(request.json['is_service'][i]) == 1:
                bCode = request.json['barcode'][i]
                units = request.json['units'][i]
                m = MasterList.query.filter_by(barcode=bCode).first()
                sd = SaleDetails(s.id, m.barcode, m.price, units, request.json['storeid'])
                db_session.add(sd)
                db_session.commit()
        sd = SaleDetails.query.filter_by(idsale = s.id).all()
        return make_response(jsonify( { "mobilerp" :[sd_.serialize for sd_ in sd]}), 200)
    else:
        return make_response(jsonify({'mobilerp': 'Operacion duplicada, saltando'}), 428)

def updateHelper(barcode, units, storeid):
    p = Product.query.filter_by(storeid=storeid, barcode=barcode).first()
    u = p.units - units
    return "UPDATE product set units={0} where barcode='{1}' and storeid={2}"\
        .format(u, barcode, storeid)
