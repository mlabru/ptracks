#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_config

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

try:
    import view.resources.resources_super_rc2
    
except ImportError:
    import view.resources.resources_super_rc3

# view
# import view.super.page_model as wpm
import view.super.pag_config as pcfg
import view.super.pag_query as pqry
import view.super.pag_update as pupd

# < class CDlgConfig >-----------------------------------------------------------------------------

class CDlgConfig(QtGui.QDialog):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control, f_parent=None):
        """
        initializes the wizard
        """
        # check input
        assert f_control
        
        # init super class
        super(CDlgConfig, self).__init__(f_parent)

        # create list widget
        self.__qlw_contents = QtGui.QListWidget()
        assert self.__qlw_contents
        
        self.__qlw_contents.setViewMode(QtGui.QListView.IconMode)
        self.__qlw_contents.setIconSize(QtCore.QSize(96, 84))
        self.__qlw_contents.setMovement(QtGui.QListView.Static)
        self.__qlw_contents.setMaximumWidth(128)
        self.__qlw_contents.setSpacing(12)

        # create stacked pages
        self.__qsw_pages = QtGui.QStackedWidget()
        assert self.__qsw_pages
        
        self.__qsw_pages.addWidget(pcfg.CPagConfig())
        self.__qsw_pages.addWidget(pupd.CPagUpdate())
        self.__qsw_pages.addWidget(pqry.CPagQuery())

        # create close button
        lbtn_close = QtGui.QPushButton("Close")
        assert lbtn_close

        lbtn_close.clicked.connect(self.close)

        # load icons
        self.__create_icons()

        # list positioning
        self.__qlw_contents.setCurrentRow(0)

        lhlo_horizontal = QtGui.QHBoxLayout()
        assert lhlo_horizontal
        
        lhlo_horizontal.addWidget(self.__qlw_contents)
        lhlo_horizontal.addWidget(self.__qsw_pages, 1)

        lhlo_buttons = QtGui.QHBoxLayout()
        assert lhlo_buttons
        
        lhlo_buttons.addStretch(1)
        lhlo_buttons.addWidget(lbtn_close)

        lvlo_main = QtGui.QVBoxLayout()
        assert lvlo_main 

        lvlo_main.addLayout(lhlo_horizontal)
        lvlo_main.addStretch(1)
        lvlo_main.addSpacing(12)
        lvlo_main.addLayout(lhlo_buttons)

        self.setLayout(lvlo_main)

        # dialog title
        self.setWindowTitle(self.tr("Super 0.1 [Supervisor]", None))

    # ---------------------------------------------------------------------------------------------
    # (QListWidgetItem *, QListWidgetItem *)
    def __change_page(self, f_current, f_previous):
        """
        DOCUMENT ME!
        """
        if not f_current:
            f_current = f_previous

        self.__qsw_pages.setCurrentIndex(self.__qlw_contents.row(f_current))

    # ---------------------------------------------------------------------------------------------
    def __create_icons(self):
        """
        DOCUMENT ME!
        """
        # config button
        lbtn_config = QtGui.QListWidgetItem(self.__qlw_contents)
        assert lbtn_config
        
        lbtn_config.setIcon(QtGui.QIcon(':/images/config.png'))
        lbtn_config.setText("Configuration")
        lbtn_config.setTextAlignment(QtCore.Qt.AlignHCenter)
        lbtn_config.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        # update button
        lbtn_update = QtGui.QListWidgetItem(self.__qlw_contents)
        assert lbtn_update

        lbtn_update.setIcon(QtGui.QIcon(':/images/update.png'))
        lbtn_update.setText("Update")
        lbtn_update.setTextAlignment(QtCore.Qt.AlignHCenter)
        lbtn_update.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        # query button
        lbtn_query = QtGui.QListWidgetItem(self.__qlw_contents)
        assert lbtn_query

        lbtn_query.setIcon(QtGui.QIcon(':/images/query.png'))
        lbtn_query.setText("Query")
        lbtn_query.setTextAlignment(QtCore.Qt.AlignHCenter)
        lbtn_query.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        # connect
        self.__qlw_contents.currentItemChanged.connect(self.__change_page)

# < the end >--------------------------------------------------------------------------------------
