#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
view_dbedit.
code for the view manager.

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
__date__ = "2015/12"

# < imports >--------------------------------------------------------------------------------------

# python library
# import logging
import os
import sys

# PyQt library
from PyQt4 import QtGui

# view
import view.view_manager as view

# view / dbEdit
import view.dbedit.wnd_main_dbedit as wmain

# control / events
import control.events.events_basic as events

# < module data >----------------------------------------------------------------------------------

# logging level
# M_LOG_LVL = logging.DEBUG

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(M_LOG_LVL)

# < class CViewDBEdit >----------------------------------------------------------------------------


class CViewDBEdit(view.CViewManager):
    """
    módulo view do editor da base de dados.  É a classe de interface.  Trata as interações com o
    usuário.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_control):
        """
        @param f_control: control manager
        """
        # logger
        # M_LOG.info("__init__:>>")   
                
        # check input parameters
        assert f_control

        # inicia a super classe
        super(CViewDBEdit, self).__init__(f_control)

        # herdados de CViewManager
        # self.config        # config manager
        # self.dct_config    # dicionário de configuração
        # self.control       # control manager
        # self.event         # event manager
        # self.model         # model manager

        # cria a aplicação
        self.__app = QtGui.QApplication(sys.argv)
        assert self.__app

        # parâmetros
        self.__app.setOrganizationName("ICEA")
        self.__app.setOrganizationDomain("pbca.icea.br")
        self.__app.setApplicationName("dbEdit")
        self.__app.setWindowIcon(QtGui.QIcon(os.path.join(self.dct_config["dir.img"], "icon.png")))

        # cria o menu principal
        self.__wmain = wmain.CWndMainDBEdit(f_control)
        assert self.__wmain

        # configura estado inicial
        # self._szState = "intro"

        # flag started
        # self._bStarted = False

        # logger
        # M_LOG.info("__init__:<<")   
                
    # ---------------------------------------------------------------------------------------------

    def notify(self, f_event):
        """
        callback de recebimento de eventos.

        @param f_event: event
        """
        # logger
        # M_LOG.info("notify:>>")   
                
        # check input parameters
        assert f_event

        if isinstance(f_event, events.CTick):
            pass

        # logger
        # M_LOG.info("notify:<<")   
                
    # ---------------------------------------------------------------------------------------------

    def run(self):
        """
        executa a aplicação
        """
        # logger
        # M_LOG.info("run:>>")   
                
        # verifica condições de execução
        assert self.__app
        assert self.__wmain

        # exibe o menu principal
        self.__wmain.show()

        # processa a aplicação
        self.__app.exec_()

        # logger
        # M_LOG.info("run:<<")   
                
# < the end >--------------------------------------------------------------------------------------
