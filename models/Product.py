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

from sqlalchemy import Column, Float, Integer, String, ForeignKey
from models import Base


class Product(Base):
    __tablename__ = "product"

    barcode = Column(String, ForeignKey(
        'products_masterlist.barcode'), primary_key=True)
    units = Column(Integer)
    storeid = Column(Integer, ForeignKey('drugstore.id'))

    """Products"""

    def __init__(self, barcode, units, storeid):
        self.barcode = barcode
        self.units = units
        self.storeid = storeid
