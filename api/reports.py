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

from flask import make_response, jsonify
from reporter.salesreport import salesReport as salesReport
from . import api, auth

from datetime import datetime as ddate


@api.route('/v1.0/dailyReport', methods=['GET'])
@auth.login_required
def sendDailyReport():
    cdate = ddate.today()
    return make_response(jsonify({'mobilerp': salesReport(cdate)}), 200)


@api.route('/v1.0/monthlyReport', methods=['GET'])
@auth.login_required
def sendMonthlyReport():
    cdate = ddate.today()
    return make_response(jsonify({'mobilerp': salesReport(cdate, 30)}), 200)
