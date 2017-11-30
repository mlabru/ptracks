#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
view_manager

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

revision 0.3  2016/ago  mlabru
pequenas correções e otimizações

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.3$"
__author__ = "Milton Abrunhosa"
__date__ = "2016/08"

# < class CViewManager >---------------------------------------------------------------------------

class CViewManager(object):
    """
    handles all interaction with user. This class is the interface
    It draws the scope on the screen and handles all mouse input
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control):
        """
        @param f_control: control
        """
        # check input
        assert f_control

        # control
        self.__control = f_control

        # register as listener
        f_control.event.register_listener(self)

    # ---------------------------------------------------------------------------------------------
    def notify(self, f_event):
        """
        callback de tratamento de eventos recebidos

        @param f_event: evento recebido
        """
        # return
        return

    # ---------------------------------------------------------------------------------------------
    def run(self):
        """
        run
        """
        # return
        return

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def app(self):
        return self.__control.app

    @app.setter
    def app(self, f_val):

        # check input
        assert f_val

        # app
        self.__control.app = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def config(self):
        return self.__control.config

    @config.setter
    def config(self, f_val):

        # check input
        assert f_val

        # config
        self.__control.config = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_config(self):
        return self.__control.config.dct_config

    @dct_config.setter
    def dct_config(self, f_val):

        # check input
        assert f_val

        # configuration dictionary
        self.__control.config.dct_config = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def control(self):
        return self.__control

    @control.setter
    def control(self, f_val):

        # check input
        assert f_val

        # control
        self.__control = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def event(self):
        return self.__control.event

    @event.setter
    def event(self, f_val):

        # check input
        assert f_val

        # event
        self.__control.event = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def model(self):
        return self.__control.model

    @model.setter
    def model(self, f_val):

        # check input
        assert f_val

        # model
        self.__control.model = f_val

# < the end >--------------------------------------------------------------------------------------
