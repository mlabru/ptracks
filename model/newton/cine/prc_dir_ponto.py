#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
prc_dir_ponto

DOCUMENT ME!

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

# model
import model.newton.defs_newton as ldefs

import model.newton.cine.abort_prc as abnd
import model.newton.cine.calc_proa_demanda as cpd
import model.newton.cine.calc_razao_curva as razc
import model.newton.cine.sentido_curva as scrv

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------
def prc_dir_ponto(f_atv, ff_pto_lng, ff_pto_lat, f_cine_data):
    """
    procedimento de direcionamento a ponto
    
    @param f_atv: ponteiro para struct aeronaves
    @param ff_pto_lng: longitude do ponto
    @param ff_pto_lat: latitude do ponto
    @param f_cine_data: ponteiro para pilha
    
    @return True se aeronave atingiu ponto, senão False
    """
    # logger
    # M_LOG.info("prc_dir_ponto:>>") 
                
    # check input
    assert f_atv
    assert f_cine_data

    # active flight ?
    if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):
        # logger
        l_log = logging.getLogger("prc_dir_ponto")
        l_log.setLevel(logging.ERROR)
        l_log.error("<E01: aeronave não ativa.")
                                
        # abort procedure
        abnd.abort_prc(f_atv)

        # cai fora...
        return None

    # calcula raio do cone de tolerância
    lf_pto_rcone = f_atv.f_trf_alt_atu * math.tan(math.radians(10))

    # calcula distância da aeronave ao ponto (x, y)
    f_cine_data.f_dst_anv_pto_x = ff_pto_lng - f_atv.f_trf_x
    f_cine_data.f_dst_anv_pto_y = ff_pto_lat - f_atv.f_trf_y

    # calcula distância euclidiana da aeronave ao ponto (linha reta)
    lf_dst_anv_pto = math.sqrt((f_cine_data.f_dst_anv_pto_x ** 2) + (f_cine_data.f_dst_anv_pto_y ** 2))

    # calcula distância euclidiana do passo da aeronave (linha reta)
    lf_passo_anv = math.sqrt((f_cine_data.f_delta_x ** 2) + (f_cine_data.f_delta_y ** 2))

    # (distância ao ponto <= raio de tolerância) ou (distância ao ponto <= passo da aeronave) ? (aeronave vai ultrapassar o ponto)
    if (lf_dst_anv_pto <= lf_pto_rcone) or (lf_dst_anv_pto <= lf_passo_anv):
        # logger
        # M_LOG.info(u"prc_dir_ponto:<E02: aeronave atingiu o ponto.") 

        # sinaliza que aeronave ATINGIU o ponto
        return True

    # calcula nova proa de demanda
    f_atv.f_atv_pro_dem = cpd.calc_proa_demanda(f_cine_data.f_dst_anv_pto_x, f_cine_data.f_dst_anv_pto_y)
    # M_LOG.debug("__ckeck_ok:f_atv_pro_dem:[{}]".format(f_atv.f_atv_pro_dem)) 

    # em curva ?
    if f_atv.f_atv_pro_dem != f_atv.f_trf_pro_atu:
        # calcula sentido de curva pelo menor ângulo
        scrv.sentido_curva(f_atv)

        # faz o bloqueio do ponto próximo
        razc.calc_razao_curva(f_atv, ff_pto_lng, ff_pto_lat, f_cine_data)

    # logger
    # M_LOG.info("prc_dir_ponto:<<") 
                
    # sinaliza que aeronave ainda NÂO atingiu o ponto
    return False

# < the end >--------------------------------------------------------------------------------------
