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

import os
import importlib as loader

class ModuleLoader():

    __found_dirs__ = []
    __loaded_modules__ = []

    def __init__(self):
        """
        Find all possible modules in current working directory
        """
        for dirs in os.listdir(os.getcwd()):
            if dirs.startswith("m_") and not dirs == "m_module_loader":
                self.__found_dirs__.append(dirs)
        print (self.__found_dirs__)

    def __load_modules__(self):
        """
        Attemping to load modules
        """
        for module in self.__found_dirs__:
            loader.import_module(module, )
        pass

