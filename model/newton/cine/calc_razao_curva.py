#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
calc_razao_curva

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
# import logging
import math

# model
import model.newton.defs_newton as ldefs

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------
def calc_razao_curva(f_atv, ff_pto_x, ff_pto_y, f_cine_data):
    """
    ajusta a razão de curva da aeronave

    @param f_atv: pointer para aeronave
    @param ff_pto_x: coordenada X do ponto
    @param ff_pto_y: coordenada Y do ponto
    @param f_cine_data: pointer para pilha
    """
    # logger
    # M_LOG.info("calc_razao_curva:>>")

    # check input
    assert f_atv
    assert f_cine_data

    # verifica condições para execução (II)
    if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):

        # cai fora...
        return False

    # curva pela esquerda ?
    if f_atv.f_atv_raz_crv < 0:

        # determina a proa
        lf_proa = f_atv.f_trf_pro_atu - 90.

    # senão, pela direita
    else:
        # determina a proa
        lf_proa = f_atv.f_trf_pro_atu - 270.

    # proa negativa ?
    if lf_proa < 0:

        # normaliza a proa
        lf_proa += 360.

    # converte para radianos
    lf_proa = math.radians(lf_proa)

    # calcula o raio de curva
    f_cine_data.f_raio_curva = abs(f_atv.f_atv_vel_gnd / math.radians(f_atv.f_atv_raz_crv))

    # calcula o centro de curva (x, y)
    lf_ccurva_x = f_atv.f_trf_x + (f_cine_data.f_raio_curva * math.sin(lf_proa))
    lf_ccurva_y = f_atv.f_trf_y + (f_cine_data.f_raio_curva * math.cos(lf_proa))

    # calcula a distância do ponto em relação ao centro da curva (x, y)
    lf_dst_pto_cc_x = ff_pto_x - lf_ccurva_x
    lf_dst_pto_cc_y = ff_pto_y - lf_ccurva_y

    # calcula a distância do ponto em relação ao centro da curva (em linha reta)
    f_cine_data.f_dst_pto_cc = math.sqrt((lf_dst_pto_cc_x ** 2) + (lf_dst_pto_cc_y ** 2))

    # calcula a nova razão curva
    if f_cine_data.f_dst_pto_cc < f_cine_data.f_raio_curva:

        # ajusta a razão ?
        if f_cine_data.v_ajusta_razao:

            # calcula a razão de curva
            lf_raz_crv = abs(f_atv.f_atv_vel_gnd / math.radians(f_cine_data.f_dst_pto_cc))

            if (lf_raz_crv > 0) and (lf_raz_crv <= 9.1961):

                if f_atv.f_atv_raz_crv < 0.:
                    f_atv.f_atv_raz_crv = -lf_raz_crv

                else:
                    f_atv.f_atv_raz_crv = lf_raz_crv

            else:
                f_atv.f_atv_raz_crv *= -1.

        else:
            f_atv.f_atv_raz_crv *= -1.

    # logger
    # M_LOG.info("calc_razao_curva:<<")

# < the end >--------------------------------------------------------------------------------------
