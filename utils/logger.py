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

import os, json

class Logger():

	log_limit = 20
	file_name = "operations_log.txt"
	file_name_tmp = "operations_log.bkp"
	file_exists = False

	def __init__(self):
		self.file_exists = os.path.isfile(self.file_name)

	def log_op(self, op):
		if(self.__check_op__(op)):
			if (self.file_exists):
				file = open(self.file_name, 'a')
			else:
				file = open(self.file_name, 'w')
				file_exists = True
			json.dump(op, file)
			file.write('\n')
			return True
		else:
			return False

	def __remove_last_op__(self):
		os.rename(self.file_name, self.file_name_tmp)
		file_tmp = open(self.file_name_tmp,'r')
		file = open(self.file_name,'w')
		line_count = 0
		for line in file_tmp:
			if line_count == 0:
				line_count += 1
				continue
			else:
				file.write(line)
		file_tmp.close()
		file.close()
		os.remove(self.file_name_tmp)

	def __check_op__(self, op):
		file = None
		line_count = 0
		if(self.file_exists):
			file = open(self.file_name, 'r')
			for line in file:
				prev_op = json.loads(line)
				if prev_op == op:
					return False
				else:
					line_count = line_count + 1
			file.close()
			if (line_count >= self.log_limit):
				self.__remove_last_op__()
			return True
		else:
			return True
