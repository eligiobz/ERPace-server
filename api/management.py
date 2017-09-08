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

from flask import make_response, jsonify, current_app
from reporter.salesreport import salesReport as salesReport
from reporter.pdfgenerator import generateSalesPdf
from . import api, auth

import os, shutil

@api.route('/v1.0/dbBackup/', methods=['GET'])
@auth.login_required
def sendDatabase():
	try:
		os.makedirs('static/db/')
	except FileExistsError:
		print ("Already exist")
	shutil.copyfile("mobilerp.db", "static/db/mobilerp.db")
	return current_app.send_static_file("db/mobilerp.db")