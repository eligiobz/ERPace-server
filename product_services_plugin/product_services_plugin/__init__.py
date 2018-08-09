# -*- coding:utf-8 -*-

##############################################################################
# MobilEPR - A small self-hosted ERP that works with your smartphone.
# Copyright (C) 2018  Eligio Becerra
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

import os, json

class ProductServicePlugin:

    description = ""

    def __init__(self, subdir):
        path = (os.getcwd()+"/"+subdir+"/"+subdir+"/")
        self.description = json.loads(open(path+"plugin.json").read())


if __name__ == "__main__":
    psp = ProductServicePlugin("m_product_services_management")