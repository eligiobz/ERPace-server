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
    __tablename__ = "saledetails"

    __table_args__ = (
        PrimaryKeyConstraint('idsale', 'idproduct'),
    )

    idsale = Column(Integer)
    idproduct = Column(Integer)
    productprice = Column(Float(precision=2))
    units = Column(Integer)
    storeid = Column(Integer)

    def __init__(self, idSale, idProduct, productPrice, units, storeid):
        self.idsale = idSale
        self.idproduct = idProduct
        self.productprice = productPrice
        self.units = units
        self.storeid = storeid

    @property
    def serialize(self):
        return {'idSale': self.idsale, 'idproduct': self.idproduct,
                'productprice': self.productprice, 'storeid': self.storeid}
