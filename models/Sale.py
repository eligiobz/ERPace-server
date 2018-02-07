# -*- coding:utf-8 -*-

##############################################################################
# MobilEPR - A small self-hosted ERP that works with your smartphone.
# Copyright (C) 2017  Eligio Becerra
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################

from sqlalchemy import Column, Integer, DateTime
from models import Base

from datetime import datetime


class Sale (Base):
    __tablename__ = "sale"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)

    def __init__(self):
        self.date = datetime.now()


""" 
Commented out for the time being as serialization 
of this object doesn't currently takes place during operation
"""
    # @property
    # def serialize(self):
    #     return {'sale': self.id, 'date': self.date}
