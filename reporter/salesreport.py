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
from models.views import SalesReport
from models import db_session as db_session, mfunc
from datetime import date as ddate, timedelta
from flask import jsonify
from .pdfgenerator import generateSalesPdf

cdate = ddate.today()


def salesReport(initDate, delta=0):
    totalItemsSold = SalesReport.query\
                    .filter(SalesReport.date <= (cdate + timedelta(days=1)))\
                    .filter((SalesReport.date >= (cdate - timedelta(days=delta))))\
                    .with_entities(mfunc.sum(SalesReport.units))\
                    .scalar()
    totalSales = len(db_session.query(\
                    SalesReport.idsale,\
                    mfunc.count(SalesReport.idsale))\
                    .filter(SalesReport.date <= (cdate + timedelta(days=1)))\
                    .filter((SalesReport.date >= (cdate - timedelta(days=delta))))\
                    .group_by(SalesReport.idsale).all())
    totalEarnings = SalesReport.query\
                    .filter(SalesReport.date <= (cdate + timedelta(days=1)))\
                    .filter((SalesReport.date >= (cdate - timedelta(days=delta))))\
                    .with_entities(mfunc.sum(SalesReport.total_earning))\
                    .scalar()
    sales = SalesReport.query.filter(SalesReport.date <= (cdate + timedelta(days=1)))\
                    .filter((SalesReport.date >= (cdate - timedelta(days=delta))))\
                    .order_by(SalesReport.idsale)
    if sales is None or len(sales.all()) == 0:
        return 500
    else:
        data = {
                'title': "Reporte del " + (str(cdate - timedelta(days=delta))\
                         + " a " if delta > 0 else "") + str(cdate),
                'totalItemsSold': totalItemsSold,
                'totalSales': totalSales,
                'totalEarnings': totalEarnings,
                'sales': [s.serialize for s in sales]
                }
        return data
