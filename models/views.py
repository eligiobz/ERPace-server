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

"""
views.py in models

This package doesn't provide any views to the api Blueprint, instead it
handles all of the views in the database, intead of creating them as a
separate entity inside this model.
"""


from sqlalchemy import Column, Integer, DateTime, PrimaryKeyConstraint,\
                       String, Float
from models import Base

from datetime import datetime


class SalesReport(Base):

    __tablename__ = "salesview"

    __table_args__ = (
        PrimaryKeyConstraint('idsale', 'name'),
    )

    idsale = Column(Integer)
    date = Column(DateTime)
    name = Column(String(700))
    productprice = Column(Float(precision=2))
    units = Column(Integer)
    total_earning = Column(Float(precision=2))

    initDate = ""
    endDate = ""

    def __init__(self, initDate="", endDate=""):
        if not initDate == "" and not endDate == "":
            self.initDate = initDate
            self.endDate = endDate

    @property
    def serialize(self):
        return {'idSale': self.idsale, 'date': self.date,
                'name': self.name, 'productprice': self.productprice,
                'units': self.units, 'total_earning': self.total_earning}

class DepletedItems(Base):

    __tablename__ = "depleteditemsview"

    __table_args__ = (
        PrimaryKeyConstraint('idsale', 'barcode', 'date'),
    )

    idsale = Column(Integer)
    date = Column(DateTime)
    name = Column(String(700))
    barcode = Column(String(50))

    @property
    def serialize(self):
        return {'idSale': self.idsale, 'date': self.date,
                'name': self.name, 'barcode': self.barcode}


class ProductStore(Base):

    __tablename__ = "products_store"

    __table_args__ = (
        PrimaryKeyConstraint('barcode', 'storeid'),
    )

    barcode = Column(String(60))
    name = Column(String(700))
    units = Column(Integer)
    price = Column(Float(precision=2))
    storeid =  Column(Integer)

    @property
    def serialize(self):
        return {'units': self.units, 'price': self.price,
                'name': self.name, 'barcode': self.barcode,
                'storeid': self.storeid}