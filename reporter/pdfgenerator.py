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

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from . import *

env = Environment(loader=FileSystemLoader('.'),
                  extensions=['jinja2.ext.with_'])


def generateSalesPdf(data):
    template = env.get_template(SALES_REPORT_TEMPLATE)
    template_vars = data
    html_output = template.render(template_vars)
    HTML(string=html_output).write_pdf(OUTPUT_FOLDER\
                                       + "salesreport.pdf",
                                       stylesheets=[SALES_REPORT_STYLE])


def generateDepletedReport(data):
    template = env.get_template(DEPLETED_REPORT_TEMPLATE)
    template_vars = data
    html_output = template.render(template_vars)
    HTML(string=html_output).write_pdf(OUTPUT_FOLDER\
                                       + "depletedreport.pdf",
                                       stylesheets=[DEPLETED_REPORT_STYLE])
