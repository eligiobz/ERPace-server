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
import pypandoc

from . import *
import app

env = Environment(loader=FileSystemLoader('.'),
                  extensions=['jinja2.ext.with_'])
env.trim_blocks = True
env.lstrip_blocks = True

pdf_or_latex = ''

if pypandoc.get_pandoc_version().startswith('2'):
  pdf_or_latex = '--pdf-engine=xelatex'
else:
  pdf_or_latex = '--latex-engine=xelatex'


def generateSalesPdf(data):
  template = env.get_template(SALES_REPORT_TEMPLATE)
  template_vars = data
  html_output = template.render(template_vars)
  output = pypandoc.convert_text(html_output, format='html', to='pdf',
    extra_args=[pdf_or_latex, '-V mainfont="DejaVu Serif"',
    '-V sansfont=Arial'], outputfile="static/pdf/salesreport.pdf")
  

def generateDepletedReport(data):
    template = env.get_template(DEPLETED_REPORT_TEMPLATE)
    template_vars = data
    html_output = template.render(template_vars)
    output = pypandoc.convert_text(html_output, format='html', to='pdf', outputfile="static/pdf/salesreport.pdf")
    assert output == ""
