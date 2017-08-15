#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
model_adapter

interface to newton

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

revision 0.1  2017/abr  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/04"

# < imports >--------------------------------------------------------------------------------------

# python library
import os
import sys

# libs
import libs.coords.coord_sys as coords
import libs.geomag.geomag.geomag.geomag as gm

# model
import model.model_manager as model
import model.core.location as cloc

# control
import control.events.events_basic as event

# < class CModelAdapter >--------------------------------------------------------------------------

class CModelAdapter(model.CModelManager):
    """
    adapter model object
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control):
        """
        constructor
        
        @param f_control: control
        """
        # init super class
        super(CModelAdapter, self).__init__(f_control)

        # herdados de CModelManager
        # self.app           # the application
        # self.config        # config manager
        # self.dct_config    # dicionário de configuração
        # self.control       # control
        # self.event         # event manager

        # obtém as coordenadas de referência
        lf_ref_lat = float(self.dct_config["map.lat"])
        lf_ref_lng = float(self.dct_config["map.lng"])
        lf_dcl_mag = float(self.dct_config["map.dcl"])

        # coordinate system
        self.__coords = coords.CCoordSys(lf_ref_lat, lf_ref_lng, lf_dcl_mag)
        assert self.__coords

        # create magnectic converter
        self.__geomag = gm.GeoMag("data/tabs/WMM.COF")
        assert self.__geomag

        # create CORE location
        self.__core_location = cloc.CLocation()
        assert self.__core_location

        # configure reference point
        self.__core_location.configure_values("0|0|{}|{}|2|50000".format(lf_ref_lat, lf_ref_lng))

    # ---------------------------------------------------------------------------------------------
    def notify(self, f_evt):
        """
        callback de tratamento de eventos recebidos

        @param f_evt: evento recebido
        """
        # return
        return
        
    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def coords(self):
        return self.__coords

    @coords.setter
    def coords(self, f_val):
        self.__coords = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def core_location(self):
        return self.__core_location

    # ---------------------------------------------------------------------------------------------
    @property
    def geomag(self):
        return self.__geomag

# < the end >--------------------------------------------------------------------------------------
