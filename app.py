#!env/bin/python
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

"""
    app.py
    Main module to run mobiler-server
"""

from flask import Flask, make_response, request, jsonify, url_for
from flask_httpauth import HTTPBasicAuth
from flask_compress import Compress
from flask_script import Manager

from models import Base, engine, db_session
from api.views import api as api
from api import init_crypt

import os

# BOILERPLATE

"""
    Bootstrap of basic for database operation in
    models packagage. We need our context to be
    set at the root directory.
"""

Base.metadata.bind = engine
Base.metadata.reflect(views=True)
Base.query = db_session.query_property()

# PREPARING APP

app = Flask(__name__)
app.config['DEBUG'] = os.getenv('DEBUG') or False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'NOT_A_SAFE_SECRET'
app.register_blueprint(api, url_prefix="/api")
Compress(app)
manager = Manager(app)
print ("Init Crypt :: ", init_crypt(app.config['SECRET_KEY'][:15]))

# manager commands
@manager.command
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        try:
        	url = url_for(rule.endpoint, **options)
        	line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        except:
        	continue
        output.append(line)
    
    for line in sorted(output):
    	print (line)

# LAUNCHING THE APP


@app.route('/')
def index():
    return make_response(jsonify({'mobilerp': 'Welcome to instance xxx'}), 200)

@app.route('/its_alive')
def its_alive():
    return make_response('yeeees!!!!', 200)

if __name__ == '__main__':
	# manager.run()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
