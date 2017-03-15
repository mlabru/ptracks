#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pag_update

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

# < class CPagUpdate >-----------------------------------------------------------------------------

class CPagUpdate(QtGui.QWidget):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_parent=None):
        """
        DOCUMENT ME!
        """
        super(CPagUpdate, self).__init__(f_parent)

        lgbx_update = QtGui.QGroupBox("Plug-in selection")
        assert lgbx_update

        lckx_system = QtGui.QCheckBox("Update system")
        assert lckx_system

        lckx_apps = QtGui.QCheckBox("Update applications")
        assert lckx_apps

        lckx_docs = QtGui.QCheckBox("Update documentation")
        assert lckx_docs

        lgbx_plugin = QtGui.QGroupBox("Existing plug-ins")
        assert lgbx_plugin

        lqlw_plug-in = QtGui.QListWidget()
        assert lqlw_plug-in

        llwi_qt = QtGui.QListWidgetItem(lqlw_plug-in)
        assert llwi_qt

        llwi_qt.setText("Qt")

        llwi_qsa = QtGui.QListWidgetItem(lqlw_plug-in)
        assert llwi_qsa

        llwi_qsa.setText("QSA")

        llwi_team_builder = QtGui.QListWidgetItem(lqlw_plug-in)
        assert llwi_team_builder

        llwi_team_builder.setText("Teambuilder")

        lbtn_start_update = QtGui.QPushButton("Start update")
        assert lbtn_start_update

        lvlo_update = QtGui.QVBoxLayout()
        assert lvlo_update

        lvlo_update.addWidget(lckx_system)
        lvlo_update.addWidget(lckx_apps)
        lvlo_update.addWidget(lckx_docs)
        lgbx_update.setLayout(lvlo_update)

        lvlo_plug-in = QtGui.QVBoxLayout()
        assert lvlo_plug-in

        lvlo_plug-in.addWidget(lqlw_plug-in)
        lgbx_plugin.setLayout(lvlo_plug-in)

        lvlo_main = QtGui.QVBoxLayout()
        assert lvlo_main

        lvlo_main.addWidget(lgbx_update)
        lvlo_main.addWidget(lgbx_plugin)
        lvlo_main.addSpacing(12)
        lvlo_main.addWidget(lbtn_start_update)
        lvlo_main.addStretch(1)

        self.setLayout(lvlo_main)

# < the end >--------------------------------------------------------------------------------------
