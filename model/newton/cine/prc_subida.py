#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
prc_subida

realiza a passagem da aeronave por todos os breakpoints que determinam uma subida

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

# model
import model.newton.defs_newton as ldefs

import model.newton.cine.abort_prc as abnd
import model.newton.cine.obtem_brk as obrk
import model.newton.cine.prc_dir_ponto as dp
import model.newton.cine.trata_associado as tass

# -------------------------------------------------------------------------------------------------
def prc_subida(f_atv, f_cine_data, f_stk_context):
    """
    realiza o procedimento de subida após o procedimento de decolagem
    
    @param f_atv: pointer to struct aeronaves
    @param f_cine_data: dados da cinemática
    @param f_stk_context: pointer to stack
    """
    # check input
    assert f_atv
    assert f_stk_context is not None

    # active flight ?
    if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):
        # logger
        l_log = logging.getLogger("prc_subida")
        l_log.setLevel(logging.ERROR)
        l_log.error("<E01: aeronave [{}/{}] não ativa.".format(f_atv.i_trf_id, f_atv.s_trf_ind))

        # abort procedure
        abnd.abort_prc(f_atv)
                                                
        # aeronave não ativa. cai fora...
        return False

    # pointer to subida
    l_sub = f_atv.ptr_trf_prc

    # subida ok ?
    if (l_sub is None) or (not l_sub.v_prc_ok):
        # logger
        l_log = logging.getLogger("prc_subida")
        l_log.setLevel(logging.ERROR)
        l_log.error("<E02: subida inexistente. aeronave:[{}/{}].".format(f_atv.i_trf_id, f_atv.s_trf_ind))

        # abort procedure
        abnd.abort_prc(f_atv)

        # subida inexistente. cai fora...
        return

    # fase de iniciação ?
    if ldefs.E_FASE_ZERO == f_atv.en_atv_fase:
        # inicia o contador de breakpoints
        f_cine_data.i_brk_ndx = 0

        # empilha o contexto futuro
        f_stk_context.append((f_atv.en_trf_fnc_ope, ldefs.E_FASE_SUBIDA, l_sub, None, 0))

        # salva a subida
        f_cine_data.ptr_sub = l_sub

        # obtém o aeródromo e pista da subida
        f_cine_data.ptr_aer = l_sub.ptr_sub_aer
        f_cine_data.ptr_pis = l_sub.ptr_sub_pis

        # carrega o contexto atual
        f_atv.ptr_trf_prc = l_sub.ptr_sub_prc_dec

        f_atv.en_trf_fnc_ope = ldefs.E_DECOLAGEM
        f_atv.en_atv_fase = ldefs.E_FASE_ZERO

    # fase subida ?
    elif ldefs.E_FASE_SUBIDA == f_atv.en_atv_fase:
        # inicia com o número do breakpoint atual
        l_brk = f_atv.ptr_atv_brk = l_sub.lst_sub_brk[f_cine_data.i_brk_ndx]

        # breakpoint ok ?
        if (l_brk is None) or (not l_brk.v_brk_ok):
            # logger
            l_log = logging.getLogger("prc_subida")
            l_log.setLevel(logging.ERROR)
            l_log.error("<E03: subida/breakpoint inexistente. aeronave:[{}/{}].".format(f_atv.i_trf_id, f_atv.s_trf_ind))

            # abort procedure
            abnd.abort_prc(f_atv)

            # subida/breakpoint inexistente. cai fora...
            return

        # obtém dados do breakpoint da subida
        obrk.obtem_brk(f_atv, l_brk, f_cine_data)

    # fase direcionamento a ponto ?
    elif ldefs.E_FASE_DIRPONTO == f_atv.en_atv_fase:
        # chegou ao breakpoint ?
        if dp.prc_dir_ponto(f_atv, f_cine_data.f_coord_x_brk, f_cine_data.f_coord_y_brk, f_cine_data):
            # próxima fase
            f_atv.en_atv_fase = ldefs.E_FASE_BREAKPOINT

            # obtém o breakpoint atual
            l_brk = f_atv.ptr_atv_brk

            # breakpoint ok ?
            if (l_brk is None) or (not l_brk.v_brk_ok):
                # logger
                l_log = logging.getLogger("prc_subida")
                l_log.setLevel(logging.ERROR)
                l_log.error("<E04: subida/breakpoint inexistente. aeronave:[{}/{}].".format(f_atv.i_atv_id, f_atv.s_atv_ind))

                # abort procedure
                abnd.abort_prc(f_atv)

                # subida/breakpoint inexistente. cai fora...
                return

            # trata o procedimento associado
            tass.trata_associado(f_atv, l_brk, f_cine_data.i_brk_ndx, f_stk_context)

    # fase rumo e altitude ?
    elif ldefs.E_FASE_RUMOALT == f_atv.en_atv_fase:
        # altitude atual(ft) é maior que a altitude máxima da TMA(ft) ?
        if (f_atv.f_atv_alt_atu * cdefs.D_CNV_M2FT) > ldefs.D_ALT_MAX_TMA:
            # ajusta a velocidade de demanda em função do nível de vôo
            f_atv.f_atv_vel_dem = f_atv.f_ptr_prf.f_prf_vel_crz  # calcIAS(f_atv.f_ptr_prf.f_prf_vel_crz, f_atv.f_atv_alt_atu, ldefs.D_EXE_VAR_TEMP_ISA)

        # proa e a altitude estão estabilizadas ?
        if (f_atv.f_atv_pro_atu == f_atv.f_atv_pro_dem) and (f_atv.f_atv_alt_atu == f_atv.f_atv_alt_dem):
            # nova fase
            f_atv.en_atv_fase = ldefs.E_FASE_BREAKPOINT

            # trata o procedimento associado
            tass.trata_associado(f_atv, l_brk, f_cine_data.i_brk_ndx, f_stk_context)

    # fase breakpoints ?
    elif ldefs.E_FASE_BREAKPOINT == f_atv.en_atv_fase:
        # é o último breakpoint da subida ?
        if f_atv.ptr_atv_brk == l_sub.lst_sub_brk[-1]:
            # reseta o flag altitude/velocidade
            f_atv.i_atv_change_alt_vel = 0

            # restaura pilha, se necessário
            tass.restaura_associado(f_atv, f_cine_data, f_stk_context)

        # otherwise, NÃO é o último breakpoint da subida...
        else:
            # próximo breakpoint
            f_cine_data.i_brk_ndx += 1
                                            
            # aponta para o próximo breakpoint
            l_brk = f_atv.ptr_atv_brk = l_sub.lst_sub_brk[f_cine_data.i_brk_ndx]
                                                                    
            # breakpoint ok ?
            if (l_brk is None) or (not l_brk.v_brk_ok):
                # logger
                l_log = logging.getLogger("prc_subida")
                l_log.setLevel(logging.ERROR)
                l_log.error("<E05: subida/breakpoint inexistente. aeronave:[{}/{}].".format(f_atv.i_atv_id, f_atv.s_atv_ind))

                # abort procedure
                abnd.abort_prc(f_atv)

                # subida/breakpoint inexistente. cai fora...
                return

            # obtém dados do breakpoint atual
            obrk.obtem_brk(f_atv, l_brk, f_cine_data)

    # otherwise, fase não identificada
    else:
        # logger
        l_log = logging.getLogger("prc_subida")
        l_log.setLevel(logging.ERROR)
        l_log.error("<E06: fase na subida não identificada.")
                
        # abort procedure
        abnd.abort_prc(f_atv)

# < the end >--------------------------------------------------------------------------------------
