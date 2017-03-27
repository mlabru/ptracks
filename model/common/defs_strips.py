#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
defs_piloto

provide all the interface to store the layer

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

revision 0.1  2015/abr  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2016/02"

# < imports >--------------------------------------------------------------------------------------

# PyQt library
from PyQt4 import QtCore

# < enums >----------------------------------------------------------------------------------------

# < defines >--------------------------------------------------------------------------------------

# strip attributes
D_STP_0, D_STP_ID, D_STP_IND, D_STP_SSR, D_STP_PRF, \
D_STP_LAT, D_STP_LNG, D_STP_ALT, D_STP_PROA, D_STP_IAS, \
D_STP_RAZ, D_STP_HORA, D_STP_STATUS = xrange(13)

# strips list (piloto)
D_STRIPS = {"0":".", "1":"o", "2":"x", "3":"+", "4":"#", "5":"@", "6":"*", "7":"^", "8":"'", "9":":"}

# reverse strips dictionary
D_STRIPS_VALS = {val: key for key, val in D_STRIPS.items()}

# strip default
D_STRIP_DEFAULT = '*'  # u'\u2744'

# < defines >--------------------------------------------------------------------------------------

# < texts >----------------------------------------------------------------------------------------

# mensagens de erro (gvm)
D_MSG_MNA = u"Máquina não autorizada. Terminando !!!"

# < the end >--------------------------------------------------------------------------------------
