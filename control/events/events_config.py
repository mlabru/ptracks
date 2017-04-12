#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
events_config

generic event superclass. What follows is a list of all events. None of these classes should
perform any tasks, as that could introduce vulnerabilities

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
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# control
import control.events.events_model as model

# < class CConfigExe >-----------------------------------------------------------------------------

class CConfigExe(model.CEventsModel):
    """
    CConfigExe event class
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, ls_exe):
        """
        constructor
        """
        # init super class
        super(CConfigExe, self).__init__()

        # herdados de CEventsModel
        # self.s_name    # event name

        # event name
        self.s_name = "ConfigExe event"

        # indicativo do exercício
        self.__s_exe = ls_exe

    # ---------------------------------------------------------------------------------------------
    @property
    def s_exe(self):
        """
        get exercício
        """
        return self.__s_exe

# < class CConfigHora >----------------------------------------------------------------------------

class CConfigHora(model.CEventsModel):
    """
    CConfigHora event class
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, lt_hora):
        """
        constructor
        """
        # init super class
        super(CConfigHora, self).__init__()

        # herdados de CEventsModel
        # self.s_name    # event name

        # event name
        self.s_name = "ConfigHora event"

        # tupla da hora
        self.__t_hora = lt_hora

    # ---------------------------------------------------------------------------------------------
    @property
    def t_hora(self):
        """
        get horário
        """
        return self.__t_hora

# < the end >--------------------------------------------------------------------------------------
