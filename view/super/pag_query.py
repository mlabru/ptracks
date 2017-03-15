#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pag_query

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

# < class CPagQuery >------------------------------------------------------------------------------

class CPagQuery(QtGui.QWidget):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_parent=None):
        """
        DOCUMENT ME!
        """
        super(CPagQuery, self).__init__(f_parent)

        lgbx_plugins = QtGui.QGroupBox("Look for plug-ins")
        assert lgbx_plugins

        llbl_name = QtGui.QLabel("Name:")
        assert llbl_name
        
        lqle_name = QtGui.QLineEdit()
        assert lqle_name

        llbl_date = QtGui.QLabel("Released after:")
        assert llbl_date
        
        ldte_date = QtGui.QDateTimeEdit(QtCore.QDate.currentDate())
        assert ldte_date

        lckx_releases = QtGui.QCheckBox("Releases")
        assert lckx_releases
        
        lckx_upgrades = QtGui.QCheckBox("Upgrades")
        assert lckx_upgrades

        lspx_hits = QtGui.QSpinBox()
        assert lspx_hits
        
        lspx_hits.setPrefix("Return up to ")
        lspx_hits.setSuffix(" results")
        lspx_hits.setSpecialValueText("Return only the first result")
        lspx_hits.setMinimum(1)
        lspx_hits.setMaximum(100)
        lspx_hits.setSingleStep(10)

        lbtn_start_query = QtGui.QPushButton("Start query")
        assert lbtn_start_query

        lglo_plugins = QtGui.QGridLayout()
        assert lglo_plugins
        
        lglo_plugins.addWidget(llbl_name, 0, 0)
        lglo_plugins.addWidget(lqle_name, 0, 1)
        lglo_plugins.addWidget(llbl_date, 1, 0)
        lglo_plugins.addWidget(ldte_date, 1, 1)
        lglo_plugins.addWidget(lckx_releases, 2, 0)
        lglo_plugins.addWidget(lckx_upgrades, 3, 0)
        lglo_plugins.addWidget(lspx_hits, 4, 0, 1, 2)
        lgbx_plugins.setLayout(lglo_plugins)

        lvlo_main = QtGui.QVBoxLayout()
        assert lvlo_main
        
        lvlo_main.addWidget(lgbx_plugins)
        lvlo_main.addSpacing(12)
        lvlo_main.addWidget(lbtn_start_query)
        lvlo_main.addStretch(1)

        self.setLayout(lvlo_main)

# < the end >--------------------------------------------------------------------------------------
