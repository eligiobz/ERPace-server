from flask import abort, make_response, request, jsonify

from models import db_session
from models.Product import Product
from models.Sale import Sale
from models.SaleDetails import SaleDetails
from models.PriceHistory import PriceHistory

from . import api, auth, logger


@api.route('/v1.0/makeSale/', methods=['POST'])
@auth.login_required
def makeSale():
    if not request.json:
        abort(400)
    if 'barcode' not in request.json or len(request.json['barcode']) <= 0:
        abort(400)
    if (logger.log_op(request.json)):
        s = Sale()
        db_session.add(s)
        db_session.commit()
        for i in range(0, len(request.json['barcode'])):
            bCode = request.json['barcode'][i]
            units = request.json['units'][i]
            ps = Product.query.filter_by(barcode=bCode).first()
            if (ps.units - units < 0):
                abort(406)
            else:
                ps.units = ps.units - units
                db_session.add(ps)
                db_session.commit()
                sd = SaleDetails(s.id, ps.barcode, ps.price, units)
                db_session.add(sd)
                db_session.commit()
        return make_response(jsonify({'mobilerp': '[p.serialize]'}), 200)
    else:
        return make_response(jsonify({'mobilerp': 'Operacion duplicada, saltando'}), 428)
