#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pag_config

DOCUMENT ME!

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

revision 0.2  2017/jan  mlabru
pep8 style conventions

revision 0.1  2016/dez  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/01"

# < imports >--------------------------------------------------------------------------------------

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

# < class CPagConfig >-----------------------------------------------------------------------------

class CPagConfig(QtGui.QWidget):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_parent=None):
        """
        DOCUMENT ME!
        """
        super(CPagConfig, self).__init__(f_parent)

        lgbx_config = QtGui.QGroupBox("Server configuration")
        assert lgbx_config

        # server
        llbl_server = QtGui.QLabel("Server:")
        assert llbl_server

        lcbx_server = QtGui.QComboBox()
        assert lcbx_server
        
        lcbx_server.addItem("Newton (ICEA)")
        lcbx_server.addItem("Newton (ITA)")
        lcbx_server.addItem("Newton (sophos)")

        lvlo_server = QtGui.QHBoxLayout()
        assert lvlo_server
        
        lvlo_server.addWidget(llbl_server)
        lvlo_server.addWidget(lcbx_server)

        # veolocity
        llbl_fast = QtGui.QLabel("Fast Time Simulation:")
        assert llbl_fast

        lcbx_fast = QtGui.QComboBox()
        assert lcbx_fast
        
        lcbx_fast.addItem("0.5")
        lcbx_fast.addItem("1.0")
        lcbx_fast.addItem("2.0")

        lvlo_fast = QtGui.QHBoxLayout()
        assert lvlo_fast
        
        lvlo_fast.addWidget(llbl_fast)
        lvlo_fast.addWidget(lcbx_fast)

        lvlo_config = QtGui.QVBoxLayout()
        assert lvlo_config
        
        lvlo_config.addLayout(lvlo_server)
        lvlo_config.addLayout(lvlo_fast)
        lgbx_config.setLayout(lvlo_config)

        lvlo_main = QtGui.QVBoxLayout()
        assert lvlo_main
        
        lvlo_main.addWidget(lgbx_config)
        lvlo_main.addStretch(1)

        self.setLayout(lvlo_main)

# < the end >--------------------------------------------------------------------------------------
