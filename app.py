#!env/bin/python

from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_compress import Compress
import time, datetime
#import hashlib
#import random
import os.path

################################# BOILERPLATE ##################################

auth = HTTPBasicAuth()
app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mobilerp.db'
app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
Compress(app)

#################################### MODELS ####################################

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    level = db.Column(db.Integer)

    """ User:: Holds basic user information """
    def __init__(self, username, password, level):
        self.username = username
        self.password = password
        self.level = level

    def __repr__(self):
        return {'username': self.username, 'pass': self.password, 'level': self.level}

    def getUser(self):
        return {'username': self.username, 'pass': self.password, 'level': self.level}



class Product(db.Model):
    barcode = db.Column(db.Integer, primary_key=True)
    units = db.Column(db.Integer)
    price = db.Column(db.Float(precision=2))
    name = db.Column(db.String(700))
    
    """Products"""
    def __init__(self, barcode, name,  units, price):
        self.barcode = barcode
        self.name = name
        self.units = units
        self.price = price
            
    """Prepares the Product to be returned in JSON format"""
    @property
    def serialize(self):
        return {'barcode': self.barcode,'name': self.name, 
        'units': self.units, 'price': self.price }

class Sale (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime)

    """docstring for CustomSalad"""
    def __init__(self):
        self.date = datetime.datetime.now()

    @property
    def serialize(self):
        return {'sale': self.id, 'date': self.date}

class SaleDetails(db.Model):
    __tablename__ = "SaleDetails"
    __table_args__ = (
        db.PrimaryKeyConstraint('idSale', 'idProduct'),
    )
    idSale = db.Column(db.Integer)
    idProduct = db.Column(db.Integer)
    productPrice = db.Column(db.Float)
    units = db.Column(db.Integer)

    """List of all the available ingredients"""
    def __init__(self, idSale, idProduct, productPrice):
        self.idSale = idSale
        self.idProduct = idProduct
        self.productPrice = productPrice

    def __repr__(self):
        return {'idSale': self.idSale, 'idProduct': self.idProduct,
        'productPrice': self.productPrice}

##################################### AUTH #####################################

@auth.get_password
def get_password(em):
    user = User.query.filter_by(username=em).first()
    if user == None:
        return None
    return user.password

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

################################## ORDERS API ##################################

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
    db.session.add(p)
    db.session.commit()
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
        p.price = float(request.json['price'])
    if 'units' in request.json :
        p.units = p.units + int(request.json['units'])
    db.session.commit()
    return make_response(jsonify({'mobilerp' : [p.serialize]}), 200)

@app.route('/mobilerp/api/v1.0/makeSale', methods=['POST'])
@auth.login_required
def makeSale():
    if not request.json:
        abort(400)
    if 'barcode' not in request.json or len(request.json['barcode']) <= 0:
        abort(400)
    s = Sale()
    db.session.add(s)
    db.session.commit()
    for bCode in request.json['barcode']:
        print(bCode)
        ps = Product.query.filter_by(barcode=int(bCode)).first()
        if (ps.units - 1 < 0):
            abort(406)
        else:
            sd = SaleDetails(s.id, ps.barcode, ps.price)
            db.session.add(sd)
            db.session.commit()
    return make_response(jsonify({'mobilerp' : '[p.serialize]'}), 200)

# @app.route('/mobilerp/api/v1.0/salad/', methods=['POST'])
# @auth.login_required
# def new_salad():
#     if not request.json:
#         abort(418)
#     if not 'ingredients' in request.json:
#         abort(406)
#     new_salad = None
#     if 'name' in request.json:
#         print ("Name in request")
#         new_salad = CustomSalad(request.json['name'])
#     else:
#         print ("No name in request")
#         new_salad = CustomSalad(str(time.time()))
#     db.session.add(new_salad)
#     for ingredient in request.json['ingredients']:
#         ing_exist = Ingredients.query.filter_by(id=ingredient).first()
#         if (ing_exist == None):
#             return make_response(jsonify({'error': "This ingredient doesn't exist"}), 406)
#     db.session.commit()
#     for ingredient in request.json['ingredients']:
#         c_salad = saladIngredients(new_salad.id, ingredient)
#         db.session.add(c_salad)
#         db.session.commit()
#     return make_response(jsonify({'salad': new_salad.id}), 201)

# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)

# @app.route('/mobilerp/api/v1.0/order', methods=['POST'])
# @auth.login_required
# def new_order():
#     if not request.json:
#         abort(418)
#     if not 'entryTime' in request.json:
#         print ("No entry time")
#         abort(406)
#     if not 'sendAddress' in request.json:
#         print ("No address")
#         abort(406)
#     new_order = None
#     if 'deliveryTime' in request.json:
#         print ("deliveryTime in request")
#         #Fri, 25 Nov 2016 23:17:09 GMT
#         new_order = Order(
#             datetime.datetime.strptime(request.json['entryTime'],
#                 "%a, %d %b %Y %H:%M:%S %Z"),
#             request.json['sendAddress'], 
#             datetime.datetime.strptime(request.json['deliveryTime'],
#                 "%a, %d %b %Y %H:%M:%S %Z"))
#     else:
#         print ("No deliveryTime in request")
#         new_order = Order(
#             datetime.datetime.strptime(request.json['entryTime'],
#                 "%a, %d %b %Y %H:%M:%S %Z"),
#             request.json['sendAddress'])
#     db.session.add(new_order)
#     user = User.query.filter_by(email=auth.username()).first()
#     userOrder = UserOrder(user.id, new_order.id)
#     db.session.add(UserOrder(user.id, new_order.id))
#     db.session.commit()
#     return make_response(jsonify({'order': new_order.id}), 201)

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

@app.route('/mobilerp/api/v1.0/user/checkLogin/', methods=['POST'])
def checkLogin():
    if not request.json or not 'user' in request.json or not 'pass' in request.json:
        abort(403)
    user = User.query.filter_by(username=request.json['user'], password = request.json['pass']).first()
    if (user is None):
        abort(401)
    else:
        return make_response(jsonify({'logged': 'true'}), 200)

@app.route('/')
def index():
    return "Hello, World!"

#### FOR DEBUGGING PURPOSES ###########

def checkDB():
    if not os.path.isfile("mobilerp.db"):
        db.create_all()

################################

if __name__ == '__main__':
    #checkDB()
    app.run(host='0.0.0.0', debug=True)