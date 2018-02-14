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

from datetime import datetime as ddate


@api.route('/v1.0/daily_report/', methods=['GET'])
@api.route('/v1.1/daily_report/', methods=['GET'])
@auth.login_required
def send_daily_report():
    cdate = ddate.today()
    data = salesReport(cdate)
    generateSalesPdf(data)
    return make_response(jsonify({'mobilerp': data}), 200)


@api.route('/v1.0/monthly_report/', methods=['GET'])
@api.route('/v1.1/monthly_report/', methods=['GET'])
@auth.login_required
def send_monthly_report():
    cdate = ddate.today()
    data = salesReport(cdate, 30)
    generateSalesPdf(data)
    return make_response(jsonify({'mobilerp': data}), 200)

# @api.route('/v1.1/monthlyReport/', methods=['GET'])
# @auth.login_required
# def sendMonthlyReport():
#     cdate = ddate.today()
#     data = salesReport(cdate, 30)
#     generateSalesPdf(data)
#     return make_response(jsonify({'mobilerp': data}), 200)


@api.route('/v1.0/get_report/<fn>', methods=['GET'])
@api.route('/v1.1/get_report/<fn>', methods=['GET'])
@auth.login_required
def get_report(fn):
	return current_app.send_static_file("pdf/"+fn)
