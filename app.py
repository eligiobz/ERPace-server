#!env/bin/python

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

from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_compress import Compress
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models import Base, engine, db_session
from models.User import User
from models.Product import Product
from models.Sale import Sale
from models.SaleDetails import SaleDetails
from models.PriceHistory import PriceHistory
from models import db_session, engine #, init_db

from api.api import api

from reports import salesReport

import time, datetime
from datetime import date as ddate
import os.path

################################# BOILERPLATE ##################################

Base.metadata.bind = engine
Base.metadata.reflect(views=True)
Base.query = db_session.query_property()

auth = HTTPBasicAuth()
app = Flask(__name__)
app.register_blueprint(api, url_prefix="/api")
Compress(app)

###########

@app.route('/')
def index():
    return printLinks()
    #return jsonify({'mobilerp':'Welcome to instance xxx'})

#### FOR DEBUGGING PURPOSES ###########

def checkDB():
    if not os.path.isfile("mobilerp.db"):
        init_db()


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

def printLinks():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))

    print(links)

################################

if __name__ == '__main__':
    checkDB()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)