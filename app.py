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

from flask import Flask, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_compress import Compress

from models import Base, engine, db_session
from api.api import api
from reports import salesReport

import os

################################# BOILERPLATE ##################################

Base.metadata.bind = engine
Base.metadata.reflect(views=True)
Base.query = db_session.query_property()

app = Flask(__name__)
app.register_blueprint(api, url_prefix="/api")
Compress(app)

############################### RUNNING THE APP ################################

@app.route('/')
def index():
    return jsonify({'mobilerp':'Welcome to instance xxx'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)