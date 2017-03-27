#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
data

simple data loader module. Loads data files from the "data" directory shipped with application.
Enhancing this to handle caching etc.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import os

# < module data >----------------------------------------------------------------------------------

# data
M_DATA_PY = os.path.abspath(os.path.dirname(__file__))
M_DATA_DIR = os.path.normpath(os.path.join(M_DATA_PY, "../.."))

# -------------------------------------------------------------------------------------------------
def filepath(f_filename):
    """
    determine the path to a file in the data directory
    """
    # return
    return os.path.join(M_DATA_DIR, f_filename)

# -------------------------------------------------------------------------------------------------
def load(f_filename, f_mode="rb"):
    """
    open a file in the data directory
    """
    # return
    return open(os.path.join(M_DATA_DIR, f_filename), f_mode)

# < the end >--------------------------------------------------------------------------------------
