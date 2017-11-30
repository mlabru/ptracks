#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
viewport

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

revision 0.2  2015/dez  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2016/01"

# < imports >--------------------------------------------------------------------------------------

# python library
import math

# model
import libs.coords.coord_defs as cdefs
import libs.coords.pos_lat_lng as pll
import libs.coords.pos_xy as pxy

# < class CViewport >------------------------------------------------------------------------------

class CViewport(object):
    """
    viewport
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fi_w, fi_h):
        """
        constructor
        """
        # inicia a super classe
        super(CViewport, self).__init__()

        # largura e altura da viewport
        self.__f_width = float(fi_w)
        self.__f_height = float(fi_h)

        # coordenada do centro da viewport
        self.__center = pll.CPosLatLng()
        assert self.__center is not None

        self.__f_blip_size = fi_w / 220.
        self.__f_zoom = 160.

    # ---------------------------------------------------------------------------------------------
    def translate_pos(self, f_pos):
        """
        translate pos
        """
        # check input
        assert f_pos

        # create answer
        l_xy = pxy.CPosXY()
        assert l_xy is not None

        # lat/lng
        lf_delta_lat = (f_pos.f_lat - self.__center.f_lat) * cdefs.D_CNV_GR2NM
        lf_delta_lng = (f_pos.f_lng - self.__center.f_lng) * cdefs.D_CNV_GR2NM

        # escala
        lf_esc = self.__f_width / self.__f_zoom

        # convert to x/y
        l_xy.f_y = self.__f_height / 2. - lf_delta_lat * lf_esc
        l_xy.f_x = self.__f_width / 2. + lf_delta_lng * math.cos(math.radians(self.__center.f_lat)) * lf_esc

        # return
        return l_xy

    # ---------------------------------------------------------------------------------------------
    def translate_xy(self, f_xy):
        """
        translate xy
        """
        # check input
        assert f_xy

        # create answer
        l_pos = pll.CPosLatLng()
        assert l_pos is not None

        # get x/y
        lf_delta_x = (f_xy.f_x - self.__f_width / 2.) / cdefs.D_CNV_GR2NM
        lf_delta_y = (f_xy.f_y - self.__f_height / 2.) / cdefs.D_CNV_GR2NM

        # escala
        lf_esc = float(self.__f_zoom / self.__f_width)

        # calculate lat/lng
        l_pos.f_lat = self.__center.f_lat - lf_delta_y * lf_esc
        l_pos.f_lng = self.__center.f_lng + lf_delta_x / math.cos(math.radians(self.__center.f_lat)) * lf_esc

        # return
        return l_pos

    # ---------------------------------------------------------------------------------------------
    def update_size(self, fi_w, fi_h):
        """
        update size
        """
        # set size
        self.__f_width = float(fi_w)
        self.__f_height = float(fi_h)

        # set blip size
        self.__f_blip_size = fi_h / 140.

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def f_blip_size(self):
        return self.__f_blip_size

    @f_blip_size.setter
    def f_blip_size(self, f_val):
        self.__f_blip_size = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def center(self):
        return self.__center

    @center.setter
    def center(self, f_val):
        self.__center = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def ppnm(self):
        return float(self.__f_width) / float(self.__f_zoom)

    # ---------------------------------------------------------------------------------------------
    @property
    def f_zoom(self):
        return self.__f_zoom

    @f_zoom.setter
    def f_zoom(self, f_val):

        # check input
        if f_val < 20:
            f_val = 20

        elif f_val > 420:
            f_val = 420

        self.__f_zoom = float(f_val)

# < the end >--------------------------------------------------------------------------------------
