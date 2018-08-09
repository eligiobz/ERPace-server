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

import os, json
import importlib

class ModuleLoader():
    """
    This class 

    TODO: Write proper documentation, make this singleton
    """

    __found_plugins__ = []
    __loaded_modules__ = []

    def __init__(self):
        """
        Find all possible modules in current working directory
        """
        for dirs in os.listdir(os.getcwd()):
            if dirs.endswith("_plugin"):
                try:
                    pkg_path = os.getcwd()+"/"+dirs+"/"+dirs+"/"
                    pkg_name = json.loads(open(pkg_path+"/plugin.json").read())["pkg_name"]
                    self.__found_plugins__.append([dirs, pkg_name])
                except FileNotFoundError as e:
                    print(dirs, " is an invalid plugin")
                #self.__found_dirs__.append(dirs,)
        print (self.__found_plugins__)
        self.__load_modules__()

    def __load_modules__(self):
        """
        Attemping to load modules
        """
        print ("CURRENT WORKING DIR ::", os.getcwd())
        for module in self.__found_plugins__:
            try:
                print("Clearing caches")
                #importlib.invalidate_caches()
                print("Attemping to load", module[0])
                m = importlib.import_module("."+module[0]+"."+module[0]+".", module[0])
                print ("Module loaded", module[0])
            except Exception as e:
                print (e, "in", os.getcwd())
            

