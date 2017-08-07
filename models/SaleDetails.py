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

from sqlalchemy import Column, Float, Integer, String, PrimaryKeyConstraint
from models import Base

class SaleDetails(Base):
    __tablename__ = "SaleDetails"

    __table_args__ = (
        PrimaryKeyConstraint('idSale', 'idProduct'),
    )

    idSale = Column(Integer)
    idProduct = Column(Integer)
    productPrice = Column(Float(precision=2))
    units = Column(Integer)

    def __init__(self, idSale, idProduct, productPrice, units):
        self.idSale = idSale
        self.idProduct = idProduct
        self.productPrice = productPrice
        self.units = units

    @property
    def serialize(self):
        return {'idSale': self.idSale, 'idProduct': self.idProduct,
        'productPrice': self.productPrice}