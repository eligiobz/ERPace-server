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

from models.User import User as User
from models import db_session

from . import api, auth

@api.route('/v1.0/user/add/', methods=['POST'])
@api.route('/v1.1/user/add/', methods=['POST'])
def add_user():
    if not request.json or ('username' not in request.json or
                            'password' not in request.json or
                            'level' not in request.json):
        abort(406)
    user = User(request.json['username'], request.json['password'],
                request.json['level'])
    db_session.add(user)
    db_session.commit()
    return jsonify({'mobilerp': [user.serialize]})

@api.route('/v1.1/user/delete/<username>', methods=['DELETE'])
@auth.login_required
def delete_user():
    pass


@api.route('/v1.0/user/update_pass/<string:n_pass>', methods=['PUT'])
@api.route('/v1.1/user/update_pass/<string:n_pass>', methods=['PUT'])
@auth.login_required
def update_pass(n_pass):
    user = User.query.filter_by(username=auth.username()).first()
    user.password = n_pass
    db_session.add(user)
    db_session.commit()
    return jsonify({'user': [user.serialize]})

@api.route('/v1.0/user/checkLogin/', methods=['GET'])
@api.route('/v1.1/user/checkLogin/', methods=['GET'])
@auth.login_required
def checkLogin():
    return make_response(jsonify({'logged': 'true'}), 200)
