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

from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, PrimaryKeyConstraint, Table, MetaData, func as mfunc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import os
import sys
import time, datetime
 
engine = create_engine('sqlite:///mobilerp.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class User(Base):
    """ User:: Holds basic user information """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(120))
    password = Column(String(120))
    level = Column(Integer)

    def __init__(self, username, password, level):
        self.username = username
        self.password = password
        self.level = level

    def __repr__(self):
        return {'username': self.username, 'pass': self.password, 'level': self.level}

    def getUser(self):
        return {'username': self.username, 'pass': self.password, 'level': self.level}


class Product(Base):
    __tablename__ = "Product"

    barcode = Column(Integer, primary_key=True)
    units = Column(Integer)
    price = Column(Float(precision=2))
    name = Column(String(700))
    
    """Products"""
    def __init__(self, barcode, name,  units, price):
        self.barcode = barcode
        self.name = name
        self.units = units
        self.price = price
            
    """Prepares the Product to be returned in JSON format"""
    @property
    def serialize(self):
        return {'barcode': self.barcode,'name': self.name, 
        'units': self.units, 'price': self.price }

class PriceHistory(Base):
    __tablename__ = "PriceHistory"
    """docstring for PriceHistory"""
    date_changed = Column(DateTime)
    old_price = Column(Float(precision=2))
    barcode = Column(Integer, primary_key=True)

    def __init__(self, barcode):
        self.barcode = barcode
        self.old_price = (Product.query.filter_by(barcode=barcode).first()).price
        self.date_changed = datetime.datetime.now()

    @property
    def serialize(self):
        pass
        

class Sale (Base):
    __tablename__ = "Sale"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)

    def __init__(self):
        self.date = datetime.datetime.now()

    @property
    def serialize(self):
        return {'sale': self.id, 'date': self.date}

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

class SaleReport(Base):

    __tablename__ = "SalesView"

    __table_args__ = (
        PrimaryKeyConstraint('idSale', 'name'),
    )

    idSale = Column(Integer)
    date = Column(DateTime)
    name = Column(String(700))
    productPrice = Column(Float(precision=2))
    units = Column (Integer)
    total_earning = Column(Float(precision=2))

    initDate = ""
    endDate = ""

    def __init__(self, initDate="", endDate=""):
        if not initDate == "" and not endDate == "":
            self.initDate = initDate
            self.endDate = endDate

    @property
    def serialize(self):
        return {'idSale': self.idSale, 'date': self.date,\
                'name': self.name, 'productPrice': self.productPrice,\
                'units': self.units, 'total_earning':self.total_earning\
                }

def init_db():
    Base.metadata.create_all(engine)
    u = User("carlo", 123, 0)
    db_session.add(u)
    db_session.commit()