#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
cine_data

defines e constantes válidas localmente

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

revision 0.1  2014/out  mlabru
initial release (Python/Linux)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging

# model
import model.newton.defs_newton as ldefs
# import model.newton.cine.cine_item as item

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CCineData >------------------------------------------------------------------------------

class CCineData(object):
    """
    mantém as informações específicas sobre dados para cinemática da aeronave
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # logger
        # M_LOG.info("__init__:>>")

        # flag ajusta razão (bloqueia.ponto)
        self.__v_ajusta_razao = False

        # coordenadas do breakpoint (obtem.brk)
        self.__f_coord_x_brk = 0.
        self.__f_coord_y_brk = 0.

        # distância em x do passo da aeronave (dir.ponto, dados.dinamicos)
        self.__f_delta_x = 0.
        # distância em y do passo da aeronave (dir.ponto, dados.dinamicos)
        self.__f_delta_y = 0.

        # distância em x da aeronave ao fixo (dados.dinamicos)
        self.__f_dst_anv_fix_x = 0.
        # distância em y da aeronave ao fixo (dados.dinamicos)
        self.__f_dst_anv_fix_y = 0.

        # distância em x da aeronave ao ponto (dir.ponto)
        self.__f_dst_anv_pto_x = 0.
        # distância em y da aeronave ao ponto (dir.ponto)
        self.__f_dst_anv_pto_y = 0.

        # distância reta do ponto ao centro de curva (bloqueia.ponto)
        self.__f_dst_pto_cc = 0.

        # pointer para o aeródromo da subida/pouso (decolagem/pouso)
        self.__ptr_aer = None
        # pointer para a pista da subida/pouso (decolagem/pouso)
        self.__ptr_pis = None
        # pointer para a subida/pouso (decolagem/pouso)
        self.__ptr_sub = None

        # índice do breakpoint atual
        self.__i_brk_ndx = 0

        # flag interceptou fixo (dir.fixo)
        self.__v_interceptou_fixo = False

        # raio de curva (bloqueia.ponto)
        self.__f_raio_curva = 0.

        # tempo na perna de aproximação (prc_espera)
        self.__h_tempo = 0.

        # ângulo da perna de afastamento (prc_espera)
        self.__f_afasta = 0.

        # setor de entrada na espera (prc_espera)
        self.__i_setor_ent = 0
        self.__i_bloqueio_fixo = 0

        # razão de descida na espera (prc_espera)
        self.__f_raz_sub_des = 0.



        # distância da aeronave ao ponto de interceptação
        #self.__f_dst_anv_pto_int = 0.
        # distância do início de curva ao ponto de interceptação
        #self.__f_dst_pto_crv_pto_int = 0.
        # distância do ponto de início de curva a radial desejada
        #self.__f_dst_pto_crv_rad = 0.

        #self.__f_pto_ix = 0.
        #self.__f_pto_iy = 0.

        # ângulo de interceptação a reta do localizer
        #self.__f_angi_loc = 0.

        # lado da aeronave em realação a radial desejada
        #self.__i_lado_anv = 0

        #self.__v_rampa = False

        # logger
        # M_LOG.info("__init__:<<")

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def ptr_aer(self):
        """
        get aeródromo decolagem/pouso
        """
        return self.__ptr_aer

    @ptr_aer.setter
    def ptr_aer(self, f_val):
        """
        set aeródromo decolagem/pouso
        """
        self.__ptr_aer = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_afasta(self):
        """
        get ângulo da perna de afastamento (prc_espera)
        """
        return self.__f_afasta

    @f_afasta.setter
    def f_afasta(self, f_val):
        """
        set ângulo da perna de afastamento (prc_espera)
        """
        self.__f_afasta = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def v_ajusta_razao(self):
        """
        get flag ajusta razao de curva
        """
        return self.__v_ajusta_razao

    @v_ajusta_razao.setter
    def v_ajusta_razao(self, f_val):
        """
        set flag ajusta razao de curva
        """
        self.__v_ajusta_razao = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def i_bloqueio_fixo(self):
        """
        get 
        """
        return self.__i_bloqueio_fixo

    @i_bloqueio_fixo.setter
    def i_bloqueio_fixo(self, f_val):
        """
        set 
        """
        self.__i_bloqueio_fixo = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def i_brk_ndx(self):
        """
        get índice do breakpoint atual
        """
        return self.__i_brk_ndx

    @i_brk_ndx.setter
    def i_brk_ndx(self, f_val):
        """
        set índice do breakpoint atual
        """
        self.__i_brk_ndx = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_coord_x_brk(self):
        """
        get coordenada x do breakpoint
        """
        return self.__f_coord_x_brk

    @f_coord_x_brk.setter
    def f_coord_x_brk(self, f_val):
        """
        set coordenada x do breakpoint
        """
        self.__f_coord_x_brk = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_coord_y_brk(self):
        """
        get coordenada y do breakpoint
        """
        return self.__f_coord_y_brk

    @f_coord_y_brk.setter
    def f_coord_y_brk(self, f_val):
        """
        set coordenada y do breakpoint
        """
        self.__f_coord_y_brk = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_delta_x(self):
        """
        get distância x do passo da aeronave
        """
        return self.__f_delta_x

    @f_delta_x.setter
    def f_delta_x(self, f_val):
        """
        set distância x do passo da aeronave
        """
        self.__f_delta_x = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_delta_y(self):
        """
        get distância y do passo da aeronave
        """
        return self.__f_delta_y

    @f_delta_y.setter
    def f_delta_y(self, f_val):
        """
        set distância y do passo da aeronave
        """
        self.__f_delta_y = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_dst_anv_fix_x(self):
        """
        get distância x da aeronave ao fixo
        """
        return self.__f_dst_anv_fix_x

    @f_dst_anv_fix_x.setter
    def f_dst_anv_fix_x(self, f_val):
        """
        set distância X da aeronave ao fixo
        """
        self.__f_dst_anv_fix_x = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_dst_anv_fix_y(self):
        """
        get distância y da aeronave ao fixo
        """
        return self.__f_dst_anv_fix_y

    @f_dst_anv_fix_y.setter
    def f_dst_anv_fix_y(self, f_val):
        """
        set distância y da aeronave ao fixo
        """
        self.__f_dst_anv_fix_y = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_dst_anv_pto_x(self):
        """
        get distância x da aeronave ao ponto
        """
        return self.__f_dst_anv_pto_x

    @f_dst_anv_pto_x.setter
    def f_dst_anv_pto_x(self, f_val):
        """
        set distância x da aeronave ao ponto
        """
        self.__f_dst_anv_pto_x = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_dst_anv_pto_y(self):
        """
        get distância y da aeronave ao ponto
        """
        return self.__f_dst_anv_pto_y

    @f_dst_anv_pto_y.setter
    def f_dst_anv_pto_y(self, f_val):
        """
        set distância y da aeronave ao ponto
        """
        self.__f_dst_anv_pto_y = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_dst_pto_cc(self):
        """
        get distância reta do ponto ao centro de curva
        """
        return self.__f_dst_pto_cc

    @f_dst_pto_cc.setter
    def f_dst_pto_cc(self, f_val):
        """
        set distância reta do ponto ao centro de curva
        """
        self.__f_dst_pto_cc = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def v_interceptou_fixo(self):
        """
        get flag interceptou fixo
        """
        return self.__v_interceptou_fixo

    @v_interceptou_fixo.setter
    def v_interceptou_fixo(self, f_val):
        """
        set flag interceptou fixo
        """
        self.__v_interceptou_fixo = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def ptr_pis(self):
        """
        get pista decolagem/pouso
        """
        return self.__ptr_pis

    @ptr_pis.setter
    def ptr_pis(self, f_val):
        """
        set pista decolagem/pouso
        """
        self.__ptr_pis = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_raio_curva(self):
        """
        get raio de curva
        """
        return self.__f_raio_curva

    @f_raio_curva.setter
    def f_raio_curva(self, f_val):
        """
        set raio de curva
        """
        self.__f_raio_curva = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_raz_sub_des(self):
        """
        get razão de descida na espera (prc_espera)
        """
        return self.__f_raz_sub_des

    @f_raz_sub_des.setter
    def f_raz_sub_des(self, f_val):
        """
        set razão de descida na espera (prc_espera)
        """
        self.__f_raz_sub_des = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def i_setor_ent(self):
        """
        get setor de entrada na espera (prc_espera)
        """
        return self.__i_setor_ent

    @i_setor_ent.setter
    def i_setor_ent(self, f_val):
        """
        set setor de entrada na espera (prc_espera)
        """
        self.__i_setor_ent = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def ptr_sub(self):
        """
        get subida
        """
        return self.__ptr_sub

    @ptr_sub.setter
    def ptr_sub(self, f_val):
        """
        set subida
        """
        self.__ptr_sub = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def h_tempo(self):
        """
        get tempo na perna de aproximação (prc_espera)
        """
        return self.__h_tempo

    @h_tempo.setter
    def h_tempo(self, f_val):
        """
        set tempo na perna de aproximação (prc_espera)
        """
        self.__h_tempo = f_val

# < the end >--------------------------------------------------------------------------------------
