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

from sqlalchemy import Column, Integer, String
from models import Base


class User(Base):
    """ User:: Holds basic user information """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(120))
    password = Column(String(120))
    level = Column(Integer)

    def __init__(self, username, password, level):
        self.username = username
        self.password = password
        self.level = level

    def __repr__(self):
        return {'username': self.username, 'pass': self.password,
                'level': self.level}

    def getUser(self):
        return {'username': self.username, 'pass': self.password,
                'level': self.level}
