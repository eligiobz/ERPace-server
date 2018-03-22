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

from flask import Blueprint, make_response, jsonify
from flask_httpauth import HTTPBasicAuth, HTTPDigestAuth

from models.User import User as User
#from models import pwd_context
from utils.Logger import Logger as Logger

api = Blueprint('api', __name__, static_folder='static', template_folder='templates')
auth = HTTPBasicAuth()
logger = Logger()


@auth.get_password
def get_password(user):
    user = User.query.filter_by(username=user).first()
    if user is None:
        return None
    return user.password

# @auth.get_password
# def get_password(user):
#     user = User.query.filter_by(username=user).first()
#     if user is None:
#         return None
#     hashed_pass = pwd_context.hash(HTTPDigestAuth.get_password())
#     if hashed_pass == user.password:
#     	return user.password
#     else:
#     	return None

# @auth.verify_password
# def verify_password(username, passwd):
# 	user = User.query.filter_by(username=username).first()
# 	if not user:
# 		return False
# 	res=  pwd_context.verify(passwd, user.password)
# 	print ("Password verification says :: ", res)
# 	return pwd_context.verify(passwd, user.password)

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)
