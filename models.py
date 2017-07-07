import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
 
engine = create_engine('sqlite:///mobilerp.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


Base = declarative_base()
Base.query = db_session.query_property()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(120))
    password = Column(String(120))
    level = Column(Integer)

    """ User:: Holds basic user information """
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

class Sale (Base):
    __tablename__ = "Sale"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)

    """docstring for CustomSalad"""
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
    productPrice = Column(Float)
    units = Column(Integer)

    """List of all the available ingredients"""
    def __init__(self, idSale, idProduct, productPrice):
        self.idSale = idSale
        self.idProduct = idProduct
        self.productPrice = productPrice

    def __repr__(self):
        return {'idSale': self.idSale, 'idProduct': self.idProduct,
        'productPrice': self.productPrice}