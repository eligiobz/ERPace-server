#!env/bin/python

from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_compress import Compress

from models import User, Product, Sale, SaleDetails, PriceHistory
from models import db_session, init_db

import time, datetime
import os.path

################################# BOILERPLATE ##################################

auth = HTTPBasicAuth()
app = Flask(__name__)
Compress(app)

##################################### AUTH #####################################

@auth.get_password
def get_password(user):
    user = User.query.filter_by(username=user).first()
    if user == None:
        return None
    return user.password

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

##################################### API #####################################

@app.route('/mobilerp/api/v1.0/findProduct/<int:bCode>', methods=['GET'])
@auth.login_required
def findProduct(bCode):
    product = Product.query.filter_by(barcode=bCode).first()
    if (product == None):
        abort(404)
    else:
        return make_response(jsonify({'mobilerp' : [product.serialize]}), 200)

@app.route('/mobilerp/api/v1.0/listProducts/', methods=['GET'])
@auth.login_required
def listProducts():
    products = Product.query.all()
    if products is None:
        abort(400)
    return make_response(jsonify({'mobilerp' : [p.serialize for p in products]}), 200)

@app.route('/mobilerp/api/v1.0/newProduct/', methods=['POST'])
@auth.login_required
def newProduct():
    if not request.json or not 'barcode' in request.json or not 'units' in request.json or not 'price' in request.json or not 'name' in request.json:
        abort(400)
    p = Product(request.json['barcode'], request.json['name'], 
        request.json['units'], request.json['price'])
    db_session.add(p)
    db_session.commit()
    return make_response(jsonify({'mobilerp' : [p.serialize]}), 200)

@app.route('/mobilerp/api/v1.0/updateProduct/<int:bCode>', methods=['PUT'])
@auth.login_required
def updateProduct(bCode):
    if not request.json:
        abort(400)
    p = Product.query.filter_by(barcode=bCode).first()
    if p is None:
        abort(404)
    if 'price' in request.json:
        price_update = PriceHistory(p.barcode)
        db_session.add(price_update)
        db_session.commit()
        p.price = float(request.json['price'])
    if 'units' in request.json :
        p.units = p.units + int(request.json['units'])
    db_session.add(p)
    db_session.commit()
    print ("Update Done")
    return make_response(jsonify({'mobilerp' : [p.serialize]}), 200)

@app.route('/mobilerp/api/v1.0/makeSale', methods=['POST'])
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

@app.route('/mobilerp/api/v1.0/listDepletedProducts/', methods=['GET'])
@auth.login_required
def listDepletedProducts():
    products = Product.query.filter_by(units=0).all()
    if products is None:
        abort(400)
    return make_response(jsonify({'mobilerp' : [p.serialize for p in products]}), 200)

################################## USERS API ##################################

## New User
@app.route('/mobilerp/api/v1.0/users', methods=['POST'])
def add_user():
    if not request.json or (not 'user' in request.json and not 'pass' in request.json 
        or not 'level' in request.json):
        abort(403)
    user = User(request.json['user'], request.json['pass'], request.json['level'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'mobilerp':user.getUser()})

## Update User
@app.route('/mobilerp/api/v1.0/users/<string:n_pass>', methods=['PUT'])
@auth.login_required
def update_pass(n_pass):
    user = User.query.filter_by(email=auth.username()).first()
    user.password = n_pass
    db.session.add(user)
    db.session.commit()
    return jsonify({'user':user.getUser()})

@app.route('/mobilerp/api/v1.0/user/checkLogin/', methods=['GET'])
@auth.login_required
def checkLogin():
    return make_response(jsonify({'logged': 'true'}), 200)

@app.route('/')
def index():
    return jsonify({'mobilerp':'Welcome to instance xxx'})

#### FOR DEBUGGING PURPOSES ###########

def checkDB():
    if not os.path.isfile("mobilerp.db"):
        init_db()

################################

if __name__ == '__main__':
    checkDB()
    app.run(host='0.0.0.0', debug=True)