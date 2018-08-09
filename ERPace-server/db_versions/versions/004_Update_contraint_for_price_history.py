from sqlalchemy import text, MetaData, Table, Column, DateTime, Float, Integer
from migrate import *

UpdateTable = text("ALTER TABLE PriceHistory RENAME TO tmp_PriceHistory;")
RecoverData = text("INSERT INTO PriceHistory(date_changed, old_price, barcode)"\
					" SELECT date_changed, old_price, barcode"\
					" FROM tmp_PriceHistory;" )
DropTable = text("DROP table tmp_PriceHistory;")

def upgrade(migrate_engine):
	# pass
	meta = MetaData(bind=migrate_engine)
	migrate_engine.execute(UpdateTable)
	PriceHistory  = Table(
		"PriceHistory", meta,
		Column('date_changed', DateTime, primary_key=True),
		Column('old_price', Float(precision=2)),
		Column('barcode', Integer, primary_key=True),)
	PriceHistory.create()
	migrate_engine.execute(RecoverData)
	migrate_engine.execute(DropTable)

def downgrade(migrate_engine):
	# pass
	meta = MetaData(bind=migrate_engine)
	migrate_engine.execute(UpdateTable)
	PriceHistory  = Table(
		"PriceHistory", meta,
		Column('date_changed', DateTime),
		Column('old_price', Float(precision=2)),
		Column('barcode', Integer, primary_key=True),)
	PriceHistory.create()
	migrate_engine.execute(RecoverData)
	migrate_engine.execute(DropTable)
