from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, PrimaryKeyConstraint, Table, MetaData
from migrate import *

meta = MetaData()

User = Table(
	"User", meta,
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('username', String(120)),
	Column('password', String(120)),
	Column('level', Integer),
)

Product = Table(
	"Product", meta,
    Column('barcode', String(50), primary_key=True),
    Column('units', Integer),
    Column('price', Float(precision=2)),
    Column('name', String(700)),
)

PriceHistory  = Table(
	"PriceHistory", meta,
    Column('date_changed', DateTime),
    Column('old_price', Float(precision=2)),
    Column('barcode', Integer, primary_key=True),
)        

Sale = Table(
	"Sale", meta,
	Column('id', Integer, primary_key=True, autoincrement=True),
    Column('date', DateTime),
)

SaleDetails = Table(
	"SaleDetails", meta,
	Column('idSale', Integer, primary_key=True),
    Column('idProduct', Integer, primary_key=True),
    Column('productPrice', Float(precision=2)),
    Column('units', Integer),
)

def upgrade(migrate_engine):
	meta.bind = migrate_engine
	User.create()
	Product.create()
	PriceHistory.create()
	Sale.create()
	SaleDetails.create()


def downgrade(migrate_engine):
    User.drop()
    Product.drop()
    PriceHistory.drop()
    Sale.drop()
    SaleDetails.drop()