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

from . import OperationsLogs
from models import db_session

import os, json

class Logger:

	str_data = ""
	log_limit = 6

	def log_op(self, op):
		self.str_data = json.dumps(op)
		if(self.__check_op__()):
			op = OperationsLogs(self.str_data)
			db_session.add(op)
			db_session.commit()
			self.__remove_last_op__()
			return True
		else:
			return False

	def __remove_last_op__(self):
		total_ops = OperationsLogs.query.count()
		while (total_ops > self.log_limit):
			op = OperationsLogs.query.first()
			db_session.delete(op)
			db_session.commit()
			total_ops -= 1

	def __check_op__(self):
		ops_log = OperationsLogs.query.filter_by(str_data=self.str_data).first()
		if ops_log is None:
			return True
		else:
			return False
