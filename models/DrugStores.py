# -*- coding:utf-8 -*-

##############################################################################
# MobilEPR - A small self-hosted ERP that works with your smartphone.
# Copyright (C) 2018  Eligio Becerra
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

from sqlalchemy import Column, Float, Integer, String
from models import Base

class Drugstore(Base):
    __tablename__ = "drugstore"

    id = Column(Integer, primary_key=True)
    name = Column(String(700))

    """Drugstore"""
    def __init__(self, id, name):
        self.id = barcode
        self.name = name
        
    """Prepares the Drugstore to be returned in JSON format"""
    @property
    def serialize(self):
        return {'id': self.id, 'name': self.name}
