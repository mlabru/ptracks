#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
trata_associado

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

# model
import model.newton.defs_newton as ldefs
import model.newton.cine.abort_prc as abnd

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# ---------------------------------------------------------------------------------------------
def restaura_associado(f_atv, f_cine_data, f_stk_context):
    """
    restaura o procedimento associado e o contexto da pilha

    @param f_atv: pointer to aeronave
    @param f_cine_data: kinematics data
    @param f_stk_context: pointer to stack
    """
    # logger
    # M_LOG.info("restaura_associado:>>")

    # check input
    assert f_atv
    assert f_stk_context is not None

    # active flight ?
    if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):
        # logger
        l_log = logging.getLogger("restaura_associado")
        l_log.setLevel(logging.ERROR) 
        l_log.error(u"<E01: aeronave não ativa.")

        # abort procedure
        abnd.abort_prc(f_atv)
                                
        # cai fora...
        return False

    # stack not empty ?
    if len(f_stk_context) > 0:
        # pop context
        # f_atv.en_atv_brk_ptr = f_stk_context.pop()
        f_atv.en_trf_fnc_ope, f_atv.en_atv_fase, f_atv.ptr_trf_prc, f_atv.ptr_atv_brk, f_cine_data.i_brk_ndx = f_stk_context.pop()

        # M_LOG.debug("restaura_associado:fnc_ope/fase:[{}]/[{}]".format(ldefs.DCT_FNC_OPE[f_atv.en_trf_fnc_ope], ldefs.DCT_FASE[f_atv.en_atv_fase]))
        # M_LOG.debug("restaura_associado:ptr_trf_prc:[{}]".format(f_atv.ptr_trf_prc))
        # M_LOG.debug("restaura_associado:ptr_atv_brk:[{}]".format(f_atv.ptr_atv_brk))
        # M_LOG.debug("restaura_associado:i_brk_ndx:[{}]".format(f_cine_data.i_brk_ndx))

        # cai fora...
        return True

    # coloca a aeronave em manual
    f_atv.en_trf_fnc_ope = ldefs.E_MANUAL

    # volta a fase de verificar condições
    f_atv.en_atv_fase = ldefs.E_FASE_ZERO

    # logger
    # M_LOG.info("restaura_associado:<<")

    # cai fora...
    return False

# -------------------------------------------------------------------------------------------------
def trata_associado(f_atv, f_brk, fi_brk_ndx, f_stk_context):
    """
    armazena na pilha o procedimento associado
    
    @param f_atv: pointer to aeronave
    @param f_brk: pointer to breakpoint
    @param fi_brk_ndx: índice do breakpoint atual
    @param f_stk_context: pointer to stack
    
    @return True se armazenou dados da aeronave na pilha, senão False
    """
    # logger
    # M_LOG.info("trata_associado:>>")

    # check input
    assert f_atv
    assert f_stk_context is not None

    # active flight ?
    if not f_atv.v_atv_ok or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):
        # logger
        l_log = logging.getLogger("trata_associado")
        l_log.setLevel(logging.ERROR) 
        l_log.error(u"<E01: aeronave não ativa.")

        # abort procedure
        abnd.abort_prc(f_atv)
                                
        # cai fora...
        return False

    # M_LOG.debug("trata_associado:: bkp:[{}] f_brk.ptr_brk_prc:[{}]".format(f_brk.i_brk_id, f_brk.ptr_brk_prc))

    # existe um procedimento associado ?
    if (f_brk.ptr_brk_prc is not None) and (ldefs.E_NOPROC != f_brk.ptr_brk_prc):  # and (0 != f_brk.BkpNumProc):
        # push actual context
        f_stk_context.append((f_atv.en_trf_fnc_ope, f_atv.en_atv_fase, f_atv.ptr_trf_prc, f_atv.ptr_atv_brk, fi_brk_ndx))

        # M_LOG.debug("trata_associado::fnc_ope/fase(A):[{}]/[{}]".format(ldefs.DCT_FNC_OPE[f_atv.en_trf_fnc_ope], ldefs.DCT_FASE[f_atv.en_atv_fase]))
        # M_LOG.debug("trata_associado::ptr_trf_prc(A):[{}]".format(f_atv.ptr_trf_prc))
        # M_LOG.debug("trata_associado::ptr_atv_brk(A):[{}]".format(f_atv.ptr_atv_brk))

        # load new context
        f_atv.en_trf_fnc_ope = f_brk.en_brk_fnc_ope
        f_atv.en_atv_fase = ldefs.E_FASE_ZERO
        f_atv.ptr_trf_prc = f_brk.ptr_brk_prc

        # M_LOG.debug("trata_associado::fnc_ope/fase(D):[{}]/[{}]".format(ldefs.DCT_FNC_OPE[f_atv.en_trf_fnc_ope], ldefs.DCT_FASE[f_atv.en_atv_fase]))
        # M_LOG.debug("trata_associado::ptr_trf_prc(D):[{}]".format(f_atv.ptr_trf_prc))
        # M_LOG.debug("trata_associado::ptr_atv_brk(D):[{}]".format(f_atv.ptr_atv_brk))

        # EXISTE procedimento associado ao breakpoint
        return True

    # logger
    # M_LOG.info("trata_associado:<<")

    # NÂO existe procedimento associado ao breakpoint
    return False

# < the end >--------------------------------------------------------------------------------------
