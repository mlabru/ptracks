#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
abort_prc

força a aeronave abandonar o procedimento

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

# python library
# import logging

# model
import model.newton.defs_newton as ldefs

# -------------------------------------------------------------------------------------------------
def abort_prc(f_atv):
    """
    abort procedure
    """
    # check input
    assert f_atv

    # abort procedure
    f_atv.f_atv_alt_dem = f_atv.f_trf_alt_atu
    f_atv.f_atv_pro_dem = f_atv.f_trf_pro_atu
    f_atv.f_atv_vel_dem = f_atv.f_trf_vel_atu

    # f_atv.f_atv_vel_mac_dem = f_atv.f_atv_vel_mac_atu

    f_atv.ptr_atv_brk = None
    f_atv.ptr_trf_prc = None

    f_atv.en_trf_fnc_ope = ldefs.E_MANUAL
    f_atv.en_atv_fase    = ldefs.E_FASE_ZERO

# < the end >--------------------------------------------------------------------------------------
