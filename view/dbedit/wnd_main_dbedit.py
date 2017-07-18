#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wnd_main_dbedit

janela principal do editor da base de dados

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

revision 0.2  2014/nov  mlabru
inclusão de fixos, procedimentos e radares

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2014/11"

# < import >---------------------------------------------------------------------------------------

# python library
import os

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

# view
import view.dbedit.dlg_aer_data_new as dlgaer
import view.dbedit.dlg_exe_data_new as dlgexe
import view.dbedit.dlg_fix_data_new as dlgfix
import view.dbedit.dlg_prf_data_new as dlgprf
import view.dbedit.dlg_trj_data_new as dlgtrj

import view.dbedit.wnd_main_dbedit_ui as wmain_ui

# control
import control.events.events_basic as events

# < class CWndMainDBEdit >-------------------------------------------------------------------------

class CWndMainDBEdit(QtGui.QMainWindow, wmain_ui.Ui_CWndMainDBEdit):
    """
    janela principal do editor da base de dados
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control, f_parent=None):
        """
        constructor

        @param f_control: control
        @param f_parent: parent widget
        """
        # init super class
        super(CWndMainDBEdit, self).__init__(f_parent)

        # check input
        assert f_control

        # control
        self.__control = f_control
        assert self.__control

        # event
        self.__event = f_control.event
        assert self.__event

        # create main menu ui
        self.setupUi(self)

        # create connections
        self.btn_aer.clicked.connect(self.cbk_aerodromos)
        self.btn_exe.clicked.connect(self.cbk_exercicios)
        self.btn_fix.clicked.connect(self.cbk_fixos)
        self.btn_prf.clicked.connect(self.cbk_performances)
        self.btn_trj.clicked.connect(self.cbk_trajetorias)
        self.btn_sai.clicked.connect(self.cbk_sair)

        # dialogs
        self.__dlg_aer = None
        self.__dlg_exe = None
        self.__dlg_fix = None
        self.__dlg_prf = None
        self.__dlg_trj = None

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def cbk_aerodromos(self):
        """
        callback da opção edição de aeródromos da janela principal
        """
        # já existe a dialog de edição da tabela de aeródromos ?
        if self.__dlg_aer is None:
            # cria a dialog de edição da tabela de aeródromos
            self.__dlg_aer = dlgaer.CDlgAerDataNEW(self.__control, self)
            assert self.__dlg_aer
        else:
            self.setVisible(False)

        # exibe a dialog de edição da tabela de aeródromos
        self.__dlg_aer.show()

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def cbk_exercicios(self):
        """
        callback da opção edição de exercícios da janela principal
        """
        # já existe a dialog de edição da tabela de exercícios ?
        if self.__dlg_exe is None:
            # cria a dialog de edição da tabela de exercícios
            self.__dlg_exe = dlgexe.CDlgExeDataNEW(self.__control, self)
            assert self.__dlg_exe
        else:
            self.setVisible(False)

        # exibe a dialog de edição da tabela de exercícios
        self.__dlg_exe.show()

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def cbk_fixos(self):
        """
        callback da opção edição de fixos da janela principal
        """
        # já existe a dialog de edição da tabela de fixos ?
        if self.__dlg_fix is None:
            # cria a dialog de edição da tabela de fixos
            self.__dlg_fix = dlgfix.CDlgFixDataNEW(self.__control, self)
            assert self.__dlg_fix
        else:
            self.setVisible(False)

        # exibe a dialog de edição da tabela de fixos
        self.__dlg_fix.show()

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def cbk_performances(self):
        """
        callback da opção edição de performances da janela principal
        """
        # já existe a dialog de edição da tabela de performances ?
        if self.__dlg_prf is None:
            # cria a dialog de edição da tabela de performances
            self.__dlg_prf = dlgprf.CDlgPrfDataNEW(self.__control, self)
            assert self.__dlg_prf
        else:
            self.setVisible(False)

        # exibe a dialog de edição da tabela de performances
        self.__dlg_prf.show()

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def cbk_sair(self):
        """
        callback da opção sair da janela principal
        """
        # cria um evento de quit
        l_evt = events.CQuit()
        assert l_evt

        # dissemina o evento
        self.__event.post(l_evt)

        # finaliza o sistema
        self.close()

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def cbk_trajetorias(self):
        """
        callback da opção edição de trajetórias da janela principal
        """
        # já existe a dialog de edição da tabela de trajetórias ?
        if self.__dlg_trj is None:
            # cria a dialog de edição da tabela de trajetórias
            self.__dlg_trj = dlgtrj.CDlgTrjDataNEW(self.__control, self)
            assert self.__dlg_trj
        else:
            self.setVisible(False)

        # exibe a dialog de edição da tabela de trajetórias
        self.__dlg_trj.show()

# < the end>---------------------------------------------------------------------------------------
