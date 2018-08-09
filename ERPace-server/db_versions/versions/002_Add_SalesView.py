from sqlalchemy import MetaData, text
from migrate import *

meta = MetaData()

CreateSalesView = text("CREATE VIEW SalesView AS SELECT"\
			" Sale.date, Product.name, SaleDetails.idSale, SaleDetails.productPrice,"\
			" SaleDetails.units, SaleDetails.productPrice * SaleDetails.units AS total_earning"\
			" FROM SaleDetails"\
			" JOIN Sale on Sale.id = SaleDetails.idSale"\
			" JOIN Product ON Product.barcode = SaleDetails.idProduct")

DropSalesView = text("DROP VIEW SalesView")

def upgrade(migrate_engine):
	meta.bind = migrate_engine
	meta.reflect(views=True)
	migrate_engine.execute(CreateSalesView)

def downgrade(migrate_engine):
	meta.bind = migrate_engine
	meta.reflect(views=True)
	migrate_engine.execute(DropSalesView)
    