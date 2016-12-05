#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
control_dbedit

módulo controller do editor da base de dados

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

# model 
import model.model_dbedit as model

# view 
import view.dbedit.view_dbedit as view

# control 
import control.control_manager as control

import control.config.config_dbedit as config

# < class CControlDBEdit >--------------------------------------------------------------------------

class CControlDBEdit(control.CControlManager):
    """
    módulo controller do editor da base de dados
    coordinates communications between the model, views and controllers through the use of events
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        inicia o módulo controller do editor da base de dados
        """
        # initialize super class
        super(CControlDBEdit, self).__init__()

        # herdados de ControlManager
        # self.event     # event manager
        # self.config    # opções de configuração
        # self.model     # model manager
        # self.view      # view manager
        # self.voip      # biblioteca de VoIP

        # carrega o arquivo com as opções de configuração
        self.config = config.CConfigDBEdit("tracks.cfg")
        assert self.config

        # obtém o dicionário de configuração
        # self.__dct_config = self.config.dct_config
        # assert self.__dct_config

        # instancia o model
        self.model = model.CModelDBEdit(self)
        assert self.model

        # instancia a view
        self.view = view.CViewDBEdit(self)
        assert self.view

# < the end >--------------------------------------------------------------------------------------
