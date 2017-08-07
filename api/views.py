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

from flask import Flask, abort, url_for, jsonify, make_response, request

from models import db_session
from models.Product import Product
from models.Sale import Sale
from models.SaleDetails import SaleDetails
from models.PriceHistory import PriceHistory

from .products import *
from .user import *
from .reports import *

@api.route('/v1.0/makeSale', methods=['POST'])
@auth.login_required
def makeSale():
    if not request.json:
        abort(400)
    if 'barcode' not in request.json or len(request.json['barcode']) <= 0:
        abort(400)
    s = Sale()
    db_session.add(s)
    db_session.commit()
    for i in range(0, len(request.json['barcode'])):
        bCode = request.json['barcode'][i]
        units = request.json['units'][i]
        print(bCode, units)
        ps = Product.query.filter_by(barcode=bCode).first()
        if (ps.units - units < 0):
            abort(406)
        else:
            sd = SaleDetails(s.id, ps.barcode, ps.price, units)
            ps.units = ps.units - units
            db_session.add(ps)
            db_session.add(sd)
            db_session.commit()
    return make_response(jsonify({'mobilerp' : '[p.serialize]'}), 200)
