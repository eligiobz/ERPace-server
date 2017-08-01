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

from models import User, Product, Sale, SaleDetails, PriceHistory, SaleReport
from models import db_session, init_db, mfunc
from datetime import date as ddate, timedelta


cdate = ddate.today() 

def dailyReport():
	totalItemsSold = SaleReport.query\
					.filter(SaleReport.date >= cdate)\
					.with_entities(mfunc.sum(SaleReport.units))\
					.scalar()
	totalSales = len(db_session.query(\
					SaleReport.idSale,\
					mfunc.count(SaleReport.idSale))\
					.filter(SaleReport.date >= cdate)\
					.group_by(SaleReport.idSale).all())
	totalEarnings = SaleReport.query\
					.filter(SaleReport.date >= cdate)\
					.with_entities(mfunc.sum(SaleReport.total_earning))\
					.scalar()
	sales = SaleReport.query.filter(SaleReport.date >= cdate)
	if sales is None:
		return 500
	else:
		return {'totalItemsSold':totalItemsSold, \
				'totalSales':totalSales,\
				'totalEarnings':totalEarnings,\
				'sales': [s.serialize for s in sales] \
				}

def monthlyReport():
	totalItemsSold = SaleReport.query\
					.filter(SaleReport.date.between(cdate - timedelta(days=30), cdate))\
					.with_entities(mfunc.sum(SaleReport.units))\
					.scalar()
	totalSales = len(db_session.query(\
					SaleReport.idSale,\
					mfunc.count(SaleReport.idSale))\
					.filter(SaleReport.date.between(cdate - timedelta(days=30), cdate))\
					.group_by(SaleReport.idSale).all())
	totalEarnings = SaleReport.query\
					.filter(SaleReport.date.between(cdate - timedelta(days=30), cdate))\
					.with_entities(mfunc.sum(SaleReport.total_earning))\
					.scalar()
	sales = SaleReport.query.filter(SaleReport.date.between(cdate - timedelta(days=30), cdate))
	if sales is None:
		return 500
	else:
		return {'totalItemsSold':totalItemsSold, \
				'totalSales':totalSales,\
				'totalEarnings':totalEarnings,\
				'sales': [s.serialize for s in sales] \
				}

def jsonReport(sales):
	print(sales)
	#totalUnits = sale)
	return {'totalUnits': totalUnits, 'sales': sales}