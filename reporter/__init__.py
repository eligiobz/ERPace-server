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

from celery import Celery
import os

SALES_REPORT_TEMPLATE = 'templates/pdf/sales_report.html'
SALES_REPORT_STYLE = 'static/css/sales_report_style.css'
DEPLETED_REPORT_TEMPLATE = 'templates/pdf/depleted_product.html'
DEPLETED_REPORT_STYLE = 'static/css/depleted_report_style.css'
OUTPUT_FOLDER = 'static/pdf/'


celery = Celery('app', broker=os.environ['REDIS_URL'])
