#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
cine_model

the flight class. It holds information about a flight and the commands the flight has been given

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
import logging
import math

# libs
import libs.coords.coord_defs as cdefs

# model
import model.newton.defs_newton as ldefs

# import model.items.esp_trk as esptrk
import model.items.trj_new as trjnew

# control
import control.common.glb_defs as gdefs

# < class CCineModel >-----------------------------------------------------------------------------

class CCineModel(object):
    """
    the object holding all information concerning a flight
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_engine, f_control):
        """
        @param f_engine: flight engine da aeronave
        @param f_control: control manager
        """
        # check input
        assert f_engine
        assert f_control

        # init super class
        super(CCineModel, self).__init__()

        # salva o flight engine
        self.__engine = f_engine

        # salva a aeronave
        self.__atv = f_engine.atv
        assert self.__atv

        # salva dados da cinemática
        self.__cine_data = f_engine.cine_data
        assert self.__cine_data

        # salva a pilha
        self.__stk_context = f_engine.stk_context
        assert self.__stk_context is not None

        # obtém o relógio da simulação
        self.__sim_time = f_control.sim_time
        assert self.__sim_time

        # salva o socket de envio de ccc
        self.__sck_snd_cnfg = f_control.sck_snd_cnfg
        assert self.__sck_snd_cnfg

        # salva o socket de envio de pistas
        self.__sck_snd_trks = f_control.sck_snd_trks
        assert self.__sck_snd_trks

        # obtém o model manager
        l_model = f_control.model
        assert l_model

        # obtém o coordinate system
        self.__coords = l_model.coords
        assert self.__coords

        # dicionário de aeródromos
        self.__dct_aer = l_model.airspace.dct_aer
        assert self.__dct_aer

        # dicionário de fixos
        self.__dct_fix = l_model.airspace.dct_fix
        assert self.__dct_fix

        # dicionário de performances
        self.__dct_prf = l_model.dct_prf
        assert self.__dct_prf

        # dicionário de tráfegos
        self.__dct_trf = l_model.dct_trf
        assert self.__dct_prf

        # obtém o exercício
        self.__exe = l_model.exe
        assert self.__exe

        # salva dados de meteorologia
        # self.__exe_met = self.__exe.exe_met
        # assert self.__exe_met

    # ---------------------------------------------------------------------------------------------
    def send_trks(self):
        """
        DOCUMENT ME!
        """
        # clear to go
        assert self.__atv
        assert self.__sim_time
        assert self.__sck_snd_trks

        # aeronave ativa ?
        if ldefs.E_ATIVA != self.__atv.en_trf_est_atv:
            # cai fora...
            return

        # converte para lat/long
        lf_lat, lf_lng, lf_alt = self.__coords.xyz2geo(self.__atv.f_trf_x, self.__atv.f_trf_y, self.atv.f_trf_z)
        lf_alt = self.__atv.f_trf_alt_atu * cdefs.D_CNV_M2FT

        # monta o buffer de envio
        # ls_buff = str(gdefs.D_MSG_VRS) + gdefs.D_MSG_SEP + \
        #           str(gdefs.D_MSG_NEW) + gdefs.D_MSG_SEP + \
        #           str(self.__atv.i_trf_id) + gdefs.D_MSG_SEP + \
        #           str(self.__atv.ptr_trf_prf.s_prf_id) + gdefs.D_MSG_SEP + \
        #           str(self.__sim_time.obtem_hora_sim()) + gdefs.D_MSG_SEP + \
        #           str(self.__atv.get_status_envio()) + gdefs.D_MSG_SEP + \
        #           str(round(lf_lat, 6)) + gdefs.D_MSG_SEP + \
        #           str(round(lf_lng, 6)) + gdefs.D_MSG_SEP + \
        #           str(round(lf_alt, 1)) + gdefs.D_MSG_SEP + \
        #           str(round(self.__atv.f_trf_pro_atu, 1)) + gdefs.D_MSG_SEP + \
        #           str(round(self.__atv.f_trf_vel_atu * cdefs.D_CNV_MS2KT, 1))

        # monta o buffer de envio
        ls_buff = str(gdefs.D_MSG_VRS) + \
                  gdefs.D_MSG_SEP + str(gdefs.D_MSG_NEW) + \
                  gdefs.D_MSG_SEP + str(self.__atv.i_trf_id) + \
                  gdefs.D_MSG_SEP + str(self.__atv.i_trf_ssr) + \
                  gdefs.D_MSG_SEP + str(self.__atv.i_atv_spi) + \
                  gdefs.D_MSG_SEP + str(round(lf_alt, 1)) + \
                  gdefs.D_MSG_SEP + str(round(lf_lat, 6)) + \
                  gdefs.D_MSG_SEP + str(round(lf_lng, 6)) + \
                  gdefs.D_MSG_SEP + str(round(self.__atv.f_trf_vel_atu * cdefs.D_CNV_MS2KT, 1)) + \
                  gdefs.D_MSG_SEP + str(round(self.__atv.f_atv_raz_sub, 1)) + \
                  gdefs.D_MSG_SEP + str(round(self.__atv.f_trf_pro_atu, 1)) + \
                  gdefs.D_MSG_SEP + str(self.__atv.s_trf_ind) + \
                  gdefs.D_MSG_SEP + str(self.__atv.ptr_trf_prf.s_prf_id) + \
                  gdefs.D_MSG_SEP + str(self.__sim_time.obtem_hora_sim())

        # envia os dados de pista
        self.__sck_snd_trks.send_data(ls_buff)

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def atv(self):
        """
        get aeronave ativa
        """
        return self.__atv

    # ---------------------------------------------------------------------------------------------
    @property
    def cine_data(self):
        """
        get dados da cinemática
        """
        return self.__cine_data

    # ---------------------------------------------------------------------------------------------
    @property
    def coords(self):
        """
        get coordinate system
        """
        return self.__coords

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_aer(self):
        """
        get dicionário de aeródromos
        """
        return self.__dct_aer

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_fix(self):
        """
        get dicionário de fixos
        """
        return self.__dct_fix

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_prc(self):
        """
        get dicionário de procedimentos
        """
        return self.__dct_prc

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_prf(self):
        """
        get dicionário de performances
        """
        return self.__dct_prf

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_trf(self):
        """
        get dicionário de tráfegos
        """
        return self.__dct_trf

    # ---------------------------------------------------------------------------------------------
    @property
    def engine(self):
        """
        get flight engine
        """
        return self.__engine

    # ---------------------------------------------------------------------------------------------
    @property
    def exe(self):
        """
        get exercício
        """
        return self.__exe

    # ---------------------------------------------------------------------------------------------
    @property
    def sim_time(self):
        """
        get simulation time
        """
        return self.__sim_time

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_snd_cnfg(self):
        """
        get socket de envio de ccc
        """
        return self.__sck_snd_cnfg

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_snd_trks(self):
        """
        get socket de envio de pistas
        """
        return self.__sck_snd_trks

    # ---------------------------------------------------------------------------------------------
    @property
    def stk_context(self):
        """
        get stack context
        """
        return self.__stk_context

# < the end >--------------------------------------------------------------------------------------
