#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------------------------
prc_aproximacao

procedimento de aproximação de acordo com o aeródromo e pista estabelecidos

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

revision 0.2  2016/oct  mlabru
pep8 style conventions

revision 0.1  2015/nov  mlabru
initial version (Linux/Python)
--------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2016/10"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging

# control
# import control.control_debug as dbg

# model
import model.newton.defs_newton as ldefs

import model.newton.cine.abort_prc as abnd
import model.newton.cine.obtem_brk as obrk
import model.newton.cine.prc_dir_ponto as dp
import model.newton.cine.trata_associado as tass
import model.newton.cine.sentido_curva as scrv

# -------------------------------------------------------------------------------------------------
def __obtem_apx_per(f_atv, f_apx):
    """
    obtém a aproximação perdida

    @param f_atv: pointer to aeronave
    @param f_apx: pointer to aproximação

    @return True se encontrou a aproximação perdida, senão False (inexistente)
    """
    # check input
    assert f_atv
    assert f_apx

    # aproximação perdida ok ?
    if (f_apx.ptr_apx_prc_ape is not None) and (f_apx.ptr_apx_prc_ape.v_prc_ok):
        # inicia campo procedimento da aeronave com posição da ApxPerdida
        f_atv.ptr_trf_prc = f_apx.ptr_apx_prc_ape

        # aeródromo e pista estabelecidos existem. retorna sucesso na pesquisa
        return True

    # retorna condição de falha na pesquisa
    return False

# ------------------------------------------------------------------------------------------------
def __obtem_ils(f_atv, f_apx):
    """
    o procedimento ILS

    @param f_atv: pointer to aeronave
    @param f_apx: pointer to aproximação

    @return True se encontrou o ILS, senão False (inexistente)
    """
    # check input
    assert f_atv
    assert f_apx

    # ILS ok ?
    if (f_apx.ptr_apx_prc_ils is not None) and (f_apx.ptr_apx_prc_ils.v_prc_ok):
        # inicia campo procedimento da aeronave com posição do ILS
        f_atv.ptr_trf_prc = f_apx.ptr_apx_prc_ils

        # aeródromo e a pista estabelecidos existem. retorna sucesso na pesquisa
        return True

    # retorna condição de falha na pesquisa
    return False

# ------------------------------------------------------------------------------------------------
def __obtem_pouso(f_atv, f_apx):
    """
    obtém o Pouso

    @param f_atv: pointer to aeronave
    @param f_apx: pointer to aproximação

    @return True se encontrou o Pouso, senão False (inexistente)
    """
    # check input
    assert f_atv
    assert f_apx

    # pista de pouso ok ?
    if (f_apx.ptr_apx_pis is not None) and (f_apx.ptr_apx_pis.v_pst_ok):
        # ângulo mínimo para o pouso
        # i_pst_rumo (mlabru)
        lf_ang = abs(f_atv.f_trf_pro_atu - f_apx.ptr_apx_pis.f_pst_true)

        # tem condições de fazer pouso direto ?
        if lf_ang <= 15.:
            # inicia a nova fase na aproximação
            f_atv.en_atv_fase = ldefs.E_FASE_APXALINHAR

            # estabelece a proa a ser atingida (rumo da pista)
            # i_pst_rumo (mlabru)
            f_atv.f_atv_pro_dem = f_apx.ptr_apx_pis.f_pst_true

            # inicia a curva pelo menor lado
            scrv.sentido_curva(f_atv)

            # pointer do aeródromo
            f_atv.ptr_atv_aer = f_apx.ptr_apx_aer
            # pointer da pista
            f_atv.ptr_atv_pst = f_apx.ptr_apx_pis

            # coloca em procedimento de pouso
            f_atv.en_trf_fnc_ope = ldefs.E_POUSO

        # volta para fase inicial do procedimento de aproximação OU fase inicial do pouso
        f_atv.en_atv_fase = ldefs.E_FASE_ZERO

        # retorna sucesso na pesquisa
        return True

    # retorna condição de falha na pesquisa
    return False

# -------------------------------------------------------------------------------------------------
def prc_aproximacao(f_atv, f_cine_data, f_stk_context):
    """
    realiza o procedimento de aproximação

    @param f_atv: pointer to aeronave
    @param f_cine_data: dados da cinemática
    @param f_stk_context: pointer to stack
    """
    # check input
    assert f_atv

    # active flight ?
    if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):
        # logger
        l_log = logging.getLogger("prc_aproximacao")
        l_log.setLevel(logging.ERROR)
        l_log.error(u"<E01: aeronave não ativa.")

        # abort procedure
        abnd.abort_prc(f_atv)

        # cai fora...
        return

    # performance ok ?
    if (f_atv.ptr_trf_prf is None) or (not f_atv.ptr_trf_prf.v_prf_ok):
        # logger
        l_log = logging.getLogger("prc_aproximacao")
        l_log.setLevel(logging.ERROR)
        l_log.error(u"<E02: performance não existe.")

        # abort procedure
        abnd.abort_prc(f_atv)

        # cai fora...
        return

    # pointer to aproximação
    l_apx = f_atv.ptr_trf_prc

    # aproximação ok ?
    if (l_apx is None) or (not l_apx.v_prc_ok):
        # logger
        l_log = logging.getLogger("prc_aproximacao")
        l_log.setLevel(logging.ERROR)
        l_log.error(u"<E03: aproximação inexistente. aeronave:[{}/{}].".format(f_atv.i_trf_id, f_atv.s_trf_ind))

        # abort procedure
        abnd.abort_prc(f_atv)

        # return
        return

    # variáveis locais
    l_brk = None

    # fase de preparação dos dados para o procedimento ?
    if ldefs.E_FASE_ZERO == f_atv.en_atv_fase:
        # inicia o index de breakpoints
        f_cine_data.i_brk_ndx = 0

        # inicia com dados do primeiro breakpoint
        l_brk = f_atv.ptr_atv_brk = l_apx.lst_apx_brk[0]

        # breakpoint ok ?
        if (l_brk is None) or (not l_brk.v_brk_ok):
            # logger
            l_log = logging.getLogger("prc_aproximacao")
            l_log.setLevel(logging.ERROR)
            l_log.error(u"<E04: fase zero. apx/breakpoint inexistente. aeronave:[{}/{}].".format(f_atv.i_trf_id, f_atv.s_trf_ind))

            # abort procedure
            abnd.abort_prc(f_atv)

            # return
            return

        # obtém dados do breakpoint
        obrk.obtem_brk(f_atv, l_brk, f_cine_data)

    # fase de direcionamento aos breakpoints do procedimento ?
    elif ldefs.E_FASE_DIRPONTO == f_atv.en_atv_fase:
        # interceptou o breakpoint ?
        if dp.prc_dir_ponto(f_atv, f_cine_data.f_coord_x_brk, f_cine_data.f_coord_y_brk, f_cine_data):
            # se não houver um procedimento associado, faz uma espera, senão executa o procedimento
            f_atv.en_atv_fase = ldefs.E_FASE_ESPERA if f_atv.ptr_atv_brk is not None else ldefs.E_FASE_ASSOCIADO

    # fase rumo e altitude ?
    elif ldefs.E_FASE_RUMOALT == f_atv.en_atv_fase:
        # atingiu a proa e a altitude de demanda estabelecidas ?
        if (f_atv.f_trf_pro_atu == f_atv.f_atv_pro_dem) and (f_atv.f_trf_alt_atu == f_atv.f_atv_alt_dem):
            # se não houver um procedimento associado, faz uma espera, senão executa o procedimento
            f_atv.en_atv_fase = ldefs.E_FASE_ESPERA if f_atv.ptr_atv_brk is not None else ldefs.E_FASE_ASSOCIADO

    # fase de espera ? (mantém a aeronave em orbita até alcançar a altitude do breakpoint)
    elif ldefs.E_FASE_ESPERA == f_atv.en_atv_fase:
        # dados do breakpoint
        l_brk = f_atv.ptr_atv_brk
        assert l_brk

        # NÃO atingiu a altitude do breakpoint ?
        if f_atv.f_trf_alt_atu != l_brk.f_brk_alt:
            # obtém dados do breakpoint (Espera com altitude de demanda)
            obrk.obtem_brk(f_atv, l_brk, f_cine_data)

            # empilha o contexto atual devido a mudança na função operacional
            f_stk_context.append((f_atv.en_trf_fnc_ope, ldefs.E_FASE_ASSOCIADO, f_atv.ptr_trf_prc, f_atv.ptr_atv_brk, f_cine_data.i_brk_ndx))

            # salva a função operacional atual
            f_atv.en_trf_fnc_ope_ant = ldefs.E_APROXIMACAO

            # estabelece a nova função operacional e a nova fase por não ter atingido a altitude do breakpoint
            f_atv.en_trf_fnc_ope = ldefs.E_ESPERA
            f_atv.en_atv_fase = ldefs.E_FASE_ZERO
            f_atv.ptr_trf_prc = l_apx.ptr_apx_prc_esp

        # otherwise, atingiu a altitude do breakpoint...
        else:
            # estabelece nova velocidade de demanda e sinaliza nova fase
            f_atv.f_atv_vel_dem = f_atv.ptr_trf_prf.f_prf_vel_apx
            f_atv.en_atv_fase   = ldefs.E_FASE_ASSOCIADO

    # fase associado ? (identifica se houve encadeamento de outros procedimentos)
    elif ldefs.E_FASE_ASSOCIADO == f_atv.en_atv_fase:
        # dados do breakpoint
        l_brk = f_atv.ptr_atv_brk
        assert l_brk

        # sinaliza nova fase
        f_atv.en_atv_fase = ldefs.E_FASE_BREAKPOINT

        # existe procedimento associado (APX, APE, TRJ, ESP...) ao breakpoint ?
        if tass.trata_associado(f_atv, l_brk, f_cine_data.i_brk_ndx, f_stk_context):
            # é o último breakpoint da aproximação atual ?
            if f_atv.ptr_atv_brk == l_apx.lst_apx_brk[-1]:
                f_cine_data.i_brk_ndx -= 1

    # já passou por todos os breakpoints ?
    elif ldefs.E_FASE_BREAKPOINT == f_atv.en_atv_fase:
        # é o último breakpoint da aproximação atual ?
        if f_atv.ptr_atv_brk == l_apx.lst_apx_brk[-1]:
            # possível ILS ?
            if l_apx.ptr_apx_prc_ils is not None:
                # ils ok ?
                if __obtem_ils(f_atv, l_apx):
                    # coloca em procedimento de ILS
                    f_atv.en_trf_fnc_ope = ldefs.E_ILS
                    f_atv.en_atv_fase = ldefs.E_FASE_ZERO

                # otherwise, ils not ok...
                else:
                    # coloca em manual
                    f_atv.en_trf_fnc_ope = ldefs.E_MANUAL

            # pode fazer aproximação perdida caso não esteja em condições para aproximação ?
            if l_apx.ptr_apx_prc_ape is not None:
                # dados do breakpoint
                l_brk = f_atv.ptr_atv_brk
                assert l_brk

                # está em condição de pouso ?
                if (abs(f_atv.f_trf_alt_atu - l_brk.f_brk_alt) <= 0.01) and (abs(f_atv.f_trf_vel_atu - f_atv.ptr_trf_prf.f_prf_vel_apx) <= 0.01):
                    # pouso ok ?
                    if not __obtem_pouso(f_atv, l_apx):
                        # coloca em manual
                        f_atv.en_trf_fnc_ope = ldefs.E_MANUAL

                # otherwise, NÃO está em condição de pouso...
                else:
                    # aproximação perdida ok ?
                    if __obtem_apx_per(f_atv, l_apx):
                        # prepara para procedimento de aproximação perdida
                        f_atv.en_trf_fnc_ope = ldefs.E_APXPERDIDA
                        f_atv.en_atv_fase = ldefs.E_FASE_ZERO

                    # otherwise, aproximação perdida not ok...
                    else:
                        # coloca em manual
                        f_atv.en_trf_fnc_ope = ldefs.E_MANUAL

            # otherwise, NÃO pode fazer aproximação perdida nem ILS, faz pouso forçado...
            else:
                # pouso ok ?
                if not __obtem_pouso(f_atv, l_apx):
                    # coloca em manual
                    f_atv.en_trf_fnc_ope = ldefs.E_MANUAL

        # otherwise, não é o último breakpoint
        else:
            # próximo breakpoint
            f_cine_data.i_brk_ndx += 1

            # aponta para o próximo breakpoint
            l_brk = f_atv.ptr_atv_brk = l_apx.lst_apx_brk[f_cine_data.i_brk_ndx]

            # breakpoint ok ?
            if (l_brk is None) or (not l_brk.v_brk_ok):
                # logger
                l_log = logging.getLogger("prc_aproximacao")
                l_log.setLevel(logging.ERROR)
                l_log.error(u"<E05: fase breakpoint. apx/breakpoint inexistente. aeronave:[{}/{}].".format(f_atv.i_trf_id, f_atv.s_trf_ind))

                # abort procedure
                abnd.abort_prc(f_atv)

                # apx/breakpoint inexistente. cai fora...
                return

            # obtém dados do breakpoint
            obrk.obtem_brk(f_atv, l_brk, f_cine_data)

    # otherwise,...
    else:
        # logger
        l_log = logging.getLogger("prc_aproximacao")
        l_log.setLevel(logging.ERROR)
        l_log.error(u"<E06: fase da aproximação não identificada. fase:[{}].".format(ldefs.DCT_FASE[f_atv.en_atv_fase]))

# < the end >--------------------------------------------------------------------------------------
