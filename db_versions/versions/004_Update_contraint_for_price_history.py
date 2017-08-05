from sqlalchemy import Table, MetaData, String, Column
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    PriceHistory = Table('PriceHistory', meta, autoload=True)
    PriceHistory.c.date_changed.alter(primary_key=True)

def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    PriceHistory = Table('PriceHistory', meta, autoload=True)
    PriceHistory.c.date_changed.alter(primary_key=False)
