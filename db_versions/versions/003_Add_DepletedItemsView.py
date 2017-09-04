from sqlalchemy import text, MetaData
from migrate import *

meta = MetaData()

CreateDepletedItemsView = text("CREATE VIEW DepletedItemsView AS"\
	" SELECT SaleDetails.idSale, Product.barcode, Product.name, max(Sale.date) as date"
	" FROM Product"
	" JOIN SaleDetails ON SaleDetails.idProduct = Product.barcode"
	" JOIN Sale ON Sale.id = SaleDetails.idSale "
	" WHERE Product.units = 0 group by BARCODE; ")

DropDepletedItemsView = text("DROP VIEW DepletedItemsView")

def upgrade(migrate_engine):
	meta.bind = migrate_engine
	meta.reflect(views=True)
	migrate_engine.execute(CreateDepletedItemsView)


def downgrade(migrate_engine):
	meta.bind = migrate_engine
	meta.reflect(views=True)
	migrate_engine.execute(DropDepletedItemsView)