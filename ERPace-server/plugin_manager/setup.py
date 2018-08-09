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

from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='module_loader',
      version='0.1',
      description='ERPace module loader',
      long_description=readme(),
      url='http://github.com/eligiobz/MobilEPR',
      author='Eligio Becerra',
      author_email='eligio_bz@mail.com',
      license='GNU Affero',
      packages=['module_loader'],
      # test_suite='nose.collector',
      # tests_require=['nose'],
      #install_requires=[]
      # classifiers=[
      #   'Development Status :: 3 - Alpha',
      #   'License :: OSI Approved :: MIT License',
      #   'Programming Language :: Python :: 2.7',
      #   'Topic :: Text Processing :: Linguistic',
      # ],
      include_package_data=True,
      zip_safe=False)
