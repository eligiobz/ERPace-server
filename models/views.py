from sqlalchemy import Column, Integer, DateTime, PrimaryKeyConstraint, String, Float
from models import Base

from datetime import datetime

class SalesReport(Base):

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