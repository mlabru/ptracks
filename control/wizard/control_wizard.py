#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
control_wizard

this main class load from one configuration file (default tracks.cfg) all the configured tables
and start the editor

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
import model.wizard.model_wizard as model

# view 
import view.wizard.view_wizard as view

# control 
import control.control_manager as control

import control.config.config_wizard as config

# < class CControlWizard >-------------------------------------------------------------------------

class CControlWizard(control.CControlManager):
    """
    controller do configuration wizard
    coordena as comunicações entre o modelo, as views e controle usando eventos
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        inicia o módulo controller do configuration wizard
        """
        # init super class
        super(CControlWizard, self).__init__()

        # herdados de CControlManager
        # self.config    # opções de configuração
        # self.event     # event manager
        # self.model     # model manager
        # self.view      # view manager
        # self.voip      # biblioteca de VoIP

        # carrega o arquivo com as opções de configuração
        self.config = config.CConfigWizard("tracks.cfg")
        assert self.config

        # obtém o dicionário de configuração
        # self.__dct_config = self.config.dct_config
        # assert self.__dct_config

        # instancia o model
        self.model = model.CModelWizard(self)
        assert self.model

        # instancia a view
        self.view = view.CViewWizard(self)
        assert self.view

# < the end >--------------------------------------------------------------------------------------
