from sqlalchemy import MetaData, Table, create_engine
from models import Base

meta = MetaData()
meta.bind = create_engine('sqlite:///mobilerp.db', convert_unicode=True)
meta.reflect(views=True)

SaleReport = Table("SalesView", meta, autoload=True)
