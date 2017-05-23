#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
sentido_curva

calcula o sentido da curva pelo "menor ângulo"

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

# model
import model.newton.defs_newton as ldefs

# -------------------------------------------------------------------------------------------------
def sent_crv(ff_proa_atu, ff_proa_dem):
    """
    rotina para calcular o sentido da curva pelo "menor ângulo"
    
    @param ff_proa_atu: proa básica ou atual
    @param ff_proa_dem: proa desejada ou de demanda
    
    @return E_DIREITA = curva pela direita ou E_ESQUERDA = curva pela esquerda
    """
    # diferença entre proas
    ff_diff = abs(ff_proa_dem - ff_proa_atu)

    # maior que 180. ?
    if ff_diff > 180.:
        # garante menor ângulo entre proas
        ff_diff = 360. - ff_diff

    # calcula a proa a seguir
    lf_dem_calc = ff_proa_atu + ff_diff

    # normaliza
    if lf_dem_calc >= 360.:
        lf_dem_calc -= 360.

    # se ff_proa_calc for a ff_proa_dem, alcança no sentido horário
    if abs(lf_dem_calc - ff_proa_dem) <= 0.01:
        # curva pela direita
        return ldefs.E_DIREITA

    # curva pela esquerda
    return ldefs.E_ESQUERDA

# -------------------------------------------------------------------------------------------------
def sentido_curva(f_atv):
    """
    rotina para calcular o sentido da "curva pelo menor caminho"
    
    @param f_atv: pointer para a aeronave
    """
    # check input
    assert f_atv

    # verifica condições para execução
    if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):
        # cai fora...
        return None

    # calcula diferença de proa
    lf_ang_dif_proa = f_atv.f_atv_pro_dem - f_atv.f_trf_pro_atu

    # positiva ?
    if lf_ang_dif_proa >= 0.:
        if lf_ang_dif_proa >= 180.:
            # curva esquerda
            f_atv.f_atv_raz_crv = -abs(f_atv.f_atv_raz_crv)

            # curva pela esquerda (negativo)
            return ldefs.E_ESQUERDA

        # senão,...
        else:
            # curva direita
            f_atv.f_atv_raz_crv = abs(f_atv.f_atv_raz_crv)

            # curva pela direita (positivo)
            return ldefs.E_DIREITA

    # senão, negativa
    else:
        # ignora sinal
        lf_ang_dif_proa = abs(lf_ang_dif_proa)

        if lf_ang_dif_proa >= 180.:

            # curva direita (positivo)
            f_atv.f_atv_raz_crv = abs(f_atv.f_atv_raz_crv)

            # curva pela direita
            return ldefs.E_DIREITA

        # senão,...
        else:
            # curva esquerda (negativo)
            f_atv.f_atv_raz_crv = -abs(f_atv.f_atv_raz_crv)

            # curva pela esquerda
            return ldefs.E_ESQUERDA

    # nunca deverá passar por aqui !!!
    return None

# < the end >--------------------------------------------------------------------------------------
