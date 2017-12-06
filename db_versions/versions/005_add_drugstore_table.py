from sqlalchemy import text, MetaData, Table, Column, String, Float, Integer
from migrate import *

meta = MetaData()

# New tables
DrugStore = Table(
	"DrugStore", meta,
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('name', String(150)),
)

MasterList = Table(
	"MasterList", meta,
	Column('barcode', String(40)),
	Column('name', String(150)),
	Column('price', Float(precision=2)),
)

#Update product table
Product = Table(
	'Product', meta,
	Column('barcode', Integer, primary_key=True),
	Column('units', Integer),
    Column('storeid', Integer),
)

#Downgrade product table
Product_downgrade = Table(
	'Product_dw', meta,
	Column('barcode', Integer, primary_key=True),
    Column('units', Integer),
    Column('price', Float(precision=2)),
    Column('name', String(700)),
)

#Common OPS
CreateTMPUpdateTable = text("ALTER TABLE Product RENAME TO tmp_Product;")
DropTMPTable = text("DROP table tmp_Product;")

#Managing existing data for upgrade
defaultDrugStore = text("INSERT INTO DrugStore(name) values('default')")
insertMasterListData = text("INSERT INTO MasterList(barcode, name) "\
							"SELECT barcode, name FROM Product")
FillProductData = text("INSERT INTO Product(barcode, units, price)"\
 					" SELECT barcode, units, price FROM tmp_Product;")
SetDefaultStore = text(" UPDATE Product SET storeid = (SELECT MAX(id) FROM DrugStore);")

#Downgrade queries
FillDowngradeData = text("INSERT INTO Product_dw(barcode, units,price, name" \
						"SELECT FROM MasterList.barcode, MasterList.price, MasterList.name"\
						"units FROM MasterList INNER JOIN tmp_Product ON"\
						"MasterList.barcode = tmp_Product.barcode"
						)
UpdateTableName = text("ALTER TABLE Product_dw RENAME TO Product;")


def upgrade(migrate_engine):
	meta.bind = migrate_engine
	DrugStore.create()
	MasterList.create()
	migrate_engine.execute(defaultDrugStore)
	migrate_engine.execute(insertMasterListData)
	migrate_engine.execute(CreateTMPUpdateTable)
	migrate_engine.execute(FillProductData)
	migrate_engine.execute(SetDefaultStore)
	migrate_engine.execute(DropTMPTable)
	Product.create()

def downgrade(migrate_engine):
	migrate_engine.execute(CreateTMPUpdateTable)
	Product_downgrade.create()
	migrate_engine.execute(FillDowngradeData)
	migrate_engine.execute(DropTMPTable)
	MasterList.drop()
	DrugStore.drop()