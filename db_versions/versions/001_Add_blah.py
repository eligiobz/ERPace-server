from sqlalchemy import Table, Column, Integer, String, MetaData
from migrate import *

meta = MetaData()

User = Table(
	'User', meta,
	Column('id', Integer, primary_key=True),
	Column('login', String(40)),
	Column('passwd', String(40)),
)


def upgrade(migrate_engine):
	meta.bind = migrate_engine
	User.create()


def downgrade(migrate_engine):
	meta.bind = migrate_engine
	User.drop()
