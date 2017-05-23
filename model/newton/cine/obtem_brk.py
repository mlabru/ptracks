#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
obtem_brk

obtém os breakpoints para os procedimetos de Aproximação, Aproximação Perdida, Subida e Trajetória

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

# libs
import libs.coords.coord_defs as cdefs

# model
import model.newton.defs_newton as ldefs
import model.newton.cine.abort_prc as abnd
import model.newton.cine.sentido_curva as scrv

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------
def obtem_brk(f_atv, f_brk, f_cine_data):
    """
    @param f_atv: pointer to struct aeronaves
    @param f_brk: pointer to struct breakpoints
    @param f_cine_data: pointer to kinematic data
    """
    # logger
    # M_LOG.info("obtem_brk:>>")

    # check input
    assert f_atv
    assert f_cine_data

    # active flight ?
    if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):
        # logger
        l_log = logging.getLogger("obtem_brk")
        l_log.setLevel(logging.ERROR)
        l_log.error(u"<E01: aeronave não ativa.")

        # cai fora...
        return

    # performance ok ?
    if (f_atv.ptr_trf_prf is None) or (not f_atv.ptr_trf_prf.v_prf_ok):
        # logger
        l_log = logging.getLogger("obtem_brk")
        l_log.setLevel(logging.ERROR)
        l_log.error(u"<E02: performance não existe.")

        # cai fora...
        return

    # breakpoint ok ?
    if (f_brk is None) or (not f_brk.v_brk_ok):
        # logger
        l_log = logging.getLogger("obtem_brk::obtem_brk")
        l_log.setLevel(logging.ERROR)
        l_log.error(u"<E03: breakpoint inexistente. aeronave:[{}/{}].".format(f_atv.i_trf_id, f_atv.s_trf_ind))

        # não encontrou o breakpoint, força a abandonar o procedimento
        abnd.abort_prc(f_atv)

        # cai fora...
        return

    # + se a altitude NÃO foi alterada (i_atv_change_alt_vel = 0 ou 2)
    #   - obtém a altitude do breakpoint

    # + se a altitude foi alterada (i_atv_change_alt_vel = 1 ou 3)
    #   - mantém a altitude inserida pelo piloto e despreza as altitudes dos próximos pontos

    # i_atv_change_alt_vel = 0 > normal (sem alteração velocidade/altitude)
    # i_atv_change_alt_vel = 1 > mudou apenas a altitude
    # i_atv_change_alt_vel = 2 > mudou apenas a velocidade
    # i_atv_change_alt_vel = 3 > mudou ambas

    # subida ou trajetória ?
    if f_atv.en_trf_fnc_ope in [ldefs.E_SUBIDA, ldefs.E_TRAJETORIA]:
        # checa de onde obter a altitude
        # do breakpoint, da altitude de trajetória do tráfego ou da performance da aeronave

        # altitude NÃO foi alterada ?
        if (0 == f_atv.i_atv_change_alt_vel) or (2 == f_atv.i_atv_change_alt_vel):
            # é uma subida ?
            if ldefs.E_SUBIDA == f_atv.en_trf_fnc_ope:
                # breakpoint tem altitude ?
                if f_brk.f_brk_alt > 0.:
                    # altitude do breakpoint maior (ou igual) ao teto de serviço ?
                    if f_brk.f_brk_alt >= f_atv.ptr_trf_prf.f_prf_teto_sv:
                        # demanda o teto de serviço
                        f_atv.f_atv_alt_dem = f_atv.ptr_trf_prf.f_prf_teto_sv

                    # otherwise, altitude abaixo do teto de serviço...
                    else:
                        # se altitude do ponto maior que altitude de trajetória do tráfego
                        if (f_brk.f_brk_alt > f_atv.f_trf_alt_trj) and (f_atv.f_trf_alt_trj > 0.):
                            # demanda a altitude de trajetória do tráfego
                            f_atv.f_atv_alt_dem = f_atv.f_trf_alt_trj

                        # otherwise,...
                        else:
                            # demanda a altitude do breakpoint
                            f_atv.f_atv_alt_dem = f_brk.f_brk_alt

            # é uma trajetória ?
            elif ldefs.E_TRAJETORIA == f_atv.en_trf_fnc_ope:
                # M_LOG.debug("obtem_brk:f_brk_alt:[{}].".format(f_brk.f_brk_alt))

                # breakpoint tem altitude ?
                if f_brk.f_brk_alt > 0.:
                    # altitude do breakpoint maior (ou igual) ao teto de serviço ?
                    if f_brk.f_brk_alt >= f_atv.ptr_trf_prf.f_prf_teto_sv:
                        # demanda o teto de serviço
                        f_atv.f_atv_alt_dem = f_atv.ptr_trf_prf.f_prf_teto_sv

                    # otherwise, abaixo do teto de serviço
                    else:
                        # demanda a altitude do breakpoint
                        f_atv.f_atv_alt_dem = f_brk.f_brk_alt

                # otherwise, breakpoint não tem altitude
                else:
                    # altitude de trajetória tem dado ?
                    if f_atv.f_trf_alt_trj > 0.:
                        # demanda a altitude de trajetória do tráfego
                        f_atv.f_atv_alt_dem = f_atv.f_trf_alt_trj

    # otherwise, não é subida nem trajetória...
    else:
        # demanda a altitude do breakpoint ou o teto de serviço, quem for menor
        f_atv.f_atv_alt_dem = min(f_brk.f_brk_alt, f_atv.ptr_trf_prf.f_prf_teto_sv)

    # coordenada é do tipo 'T' (temporal) ?
    if f_brk.i_brk_t > 0:
        pass
        '''# aponta o fixo de referência
        # FIXO * l_pFix = None ; # &f_pAtm.AtmFix [ (int)f_brk.f_brk_x ] ;   # !!!REVER!!!

        # calcula a projeção do ponto
        f_cine_data.fCoordXBkp = l_pFix.fFixX + ( f_atv.f_trf_vel_atu * f_brk.i_brk_t * sinf ( f_brk.f_brk_y ))
        f_cine_data.fCoordYBkp = l_pFix.fFixY + ( f_atv.f_trf_vel_atu * f_brk.i_brk_t * cosf ( f_brk.f_brk_y ))
        '''
    # coordenada é do tipo 'R' (rumo e altitude)
    elif f_brk.i_brk_t < 0:
        pass
        '''# é razão ou gradiente ?
        if f_brk.f_brk_x <= 0.:
            # obtém a razão de subida
            f_atv.f_atv_raz_sub = f_atv.ptr_trf_prf.f_prf_raz_sub_crz

        # otherwise,...
        else:
            # o gradiente é uma porcentagem e uma razão de subida um valor inteiro. O
            # gradiente nunca é maior que 10%.  A razão de subida sempre é maior que
            # 100ft/min. Assumir que valores maiores que 10 é razão de subida e valores
            # menores ou iguais a 10 é gradiente.
            # ref: Tratamento do Gradiente de Subida conforme MMA 100-31, pag.108.

            # é gradiente ?
            if f_brk.f_brk_x <= 10.:
                # aplica a forma simplificada do gradiente    !!!REVER!!!
                li_val = int(f_atv.f_trf_vel_atu * f_brk.f_brk_x)

                # calcula o módulo 50
                li_mod = li_val % 50

                if li_mod > 0:
                    # se não for múltiplo de 50, arrendondar para o múltiplo mais próximo
                    if li_mod < 26:
                        li_val -= li_mod

                    else:
                        li_val += 50 - li_mod

                # armazena o gradiente aplicado o múltiplo de 50
                f_atv.f_atv_raz_sub = float(li_val)

            # otherwise, é uma razão de subida
            else:
                # armazena a razão de subida (ft/min -> m/s)
                f_atv.f_atv_raz_sub = f_brk.f_brk_x * cdefs.D_CNV_FT2M / 60.

        # obtém o rumo
        f_atv.f_atv_pro_dem = math.degrees(f_brk.f_brk_y)

        # calcula a curva pelo menor lado
        scrv.sentido_curva(f_atv)
        '''
    # otherwise, 0 == f_brk.i_brk_t
    else:
        # armazena na pilha as coordenadas cartesianas do breakpoint
        f_cine_data.f_coord_x_brk = f_brk.f_brk_x
        f_cine_data.f_coord_y_brk = f_brk.f_brk_y
        # M_LOG.debug("obtem_brk:f_cine_data.f_brk_x:[{}] f_cine_data.f_brk_y:[{}]".format(f_cine_data.f_coord_x_brk, f_cine_data.f_coord_y_brk))

    # trata o procedimento que chamou a rotina

    # trajetória ?
    if ldefs.E_TRAJETORIA == f_atv.en_trf_fnc_ope:
        # checks
        assert f_atv.ptr_trf_prc
        assert f_atv.ptr_trf_prc.v_prc_ok

        # + se a velocidade NÃO foi alterada (i_atv_change_alt_vel = 0 ou 1)
        #   - obtém a velocidade do breakpoint

        # + se a velocidade foi alterada (i_atv_change_alt_vel = 2 ou 3)
        #   - mantém a velocidade inserida pelo piloto e despreza as velocidades dos próximos pontos

        # i_atv_change_alt_vel = 0 > normal (sem alteração velocidade/altitude)
        # i_atv_change_alt_vel = 1 > mudou apenas a altitude,
        # i_atv_change_alt_vel = 2 > mudou apenas a velocidade
        # i_atv_change_alt_vel = 3 > mudou ambas

        # checa de onde obter a velocidade
        # do breakpoint, velocidade do tráfego ou performance

        # velocidade NÃO foi alterada ?
        if (0 == f_atv.i_atv_change_alt_vel) or (1 == f_atv.i_atv_change_alt_vel):
            # star ?
            if f_atv.ptr_trf_prc.v_trj_star:
                # breakpoint tem velocidade ?
                if f_brk.f_brk_vel > 0.:
                    # converte a VelMaxCrz para IAS
                    lf_vel = f_atv.ptr_trf_prf.f_prf_vel_max_crz  # calcIAS(f_atv.ptr_trf_prf.f_prf_vel_max_crz, f_atv.f_atv_alt_dem, Exercicio.fExeVarTempISA)

                    # demanda a velocidade do breakpoint ou VelMaxCrz (IAS) o que for menor
                    f_atv.f_atv_vel_dem = min(f_brk.f_brk_vel, lf_vel)

            # otherwise, é trajetória ACC...
            else:
                # velocidade de trajetória do tráfego tem dado ?
                if f_atv.f_trf_vel_trj > 0.:
                    # demanda a velocidade de trajetória do tráfego (convertido para IAS na conversão)
                    f_atv.f_atv_vel_dem = f_atv.f_trf_vel_trj

                # otherwise, não tem velocidade de trajetória do tráfego...
                else:
                    # breakpoint tem velocidade ?
                    if f_brk.f_brk_vel > 0.:
                        # velocidade do breakpoint extrapolou o limite da performance ?
                        if f_brk.f_brk_vel > f_atv.ptr_trf_prf.f_prf_vel_max_crz:
                            # demanda a VelMaxCrz convertida para IAS
                            f_atv.f_atv_vel_dem = f_atv.ptr_trf_prf.f_prf_vel_max_crz  # calcIAS(f_atv.ptr_trf_prf.fAtrPrfVelMaxCrz, f_atv.f_atv_alt_dem, Exercicio.fExeVarTempISA)

                        # velocidade do breakpoint abaixo do limite da performance...
                        else:
                            # demanda a velocidade do breakpoint convertida para IAS
                            f_atv.f_atv_vel_dem = f_brk.f_brk_vel  # calcIAS(f_brk.f_brk_vel, f_atv.f_atv_alt_dem, Exercicio.fExeVarTempISA)

                    # otherwise, breakpoint não tem velocidade...
                    else:
                        # demanda a velocidade atual do tráfego
                        f_atv.f_atv_vel_dem = f_atv.f_trf_vel_atu

            # força cálculo do MACH
            # f_atv.vAnvISOMACH = False

        # ajustar a razão de subida ou descida da aeronave em trajetória

        # aeronave descendo ?
        if f_atv.f_trf_alt_atu > f_atv.f_atv_alt_dem:
            # aplica a razão de descida em cruzeiro
            f_atv.f_atv_raz_sub = f_atv.ptr_trf_prf.f_prf_raz_des_crz

        # aeronave subindo ?
        elif f_atv.f_trf_alt_atu < f_atv.f_atv_alt_dem:
            # aplica a razão de subida em cruzeiro
            f_atv.f_atv_raz_sub = f_atv.ptr_trf_prf.f_prf_raz_sub_crz

        # aeronave nivelada ?
        elif f_atv.f_trf_alt_atu == f_atv.f_atv_alt_dem:
            # não aplica a razão de subida ou descida
            f_atv.f_atv_raz_sub = 0.

    # subida ?
    elif ldefs.E_SUBIDA == f_atv.en_trf_fnc_ope:
        # teste de altimetria para corrigir o caso em que a aeronave ao cumprir pontos sem o
        # valor da "altitude", ela possa manter o valor da última altitude de demanda. Com a
        # "altitude do breakpoint sem valor", forçava a aeronave a entrar na condição de vôo
        # abaixo de 10000FT, o que não é correto, pois, a mesma já cumpriu esta etapa do vôo

        # obtém altitude do ponto atual
        lf_brk_alt = f_brk.f_brk_alt

        # extrapolou o limite da performance ?
        if f_brk.f_brk_alt > f_atv.ptr_trf_prf.f_prf_teto_sv:
            # ajusta a altitude pela performance
            lf_brk_alt = f_atv.ptr_trf_prf.f_prf_teto_sv

        # breakpoint NÃO tem altitude ?
        if 0 == lf_brk_alt:
            # mantém a altitude de demanda do ponto anterior
            lf_brk_alt = f_atv.f_atv_alt_dem

        # converte a velocidade de cruzeiro da performance para IAS
        lf_vel = f_atv.ptr_trf_prf.f_prf_vel_crz  # calcIAS(f_atv.ptr_trf_prf.f_prf_vel_crz, f_atv.f_atv_alt_dem, Exercicio.fExeVarTempISA)

        # altitude do breakpoint é menor (ou igual) que altitude máxima na TMA ?
        if (lf_brk_alt * cdefs.D_CNV_M2FT) <= ldefs.D_ALT_MAX_TMA:
            # velocidade de subida na DEP é maior que 250KT ?
            if f_atv.ptr_trf_prf.f_prf_vel_sub_dec >= ldefs.D_VEL_MAX_TMA:
                # velocidade NÃO foi alterada ?
                if (0 == f_atv.i_atv_change_alt_vel) or (1 == f_atv.i_atv_change_alt_vel):
                    # velocidade do breakpoint é valida ?
                    if 0. < f_brk.f_brk_vel <= ldefs.D_VEL_MAX_TMA:
                        # demanda a velocidade da performance ou a velocidade do breakpoint, o que for menor
                        f_atv.f_atv_vel_dem = min(lf_vel, f_brk.f_brk_vel)

                    # otherwise, inválida...
                    else:
                        # demanda a velocidade da performance ou a velocidade limite 250KT, o que for menor
                        f_atv.f_atv_vel_dem = min(lf_vel, ldefs.D_VEL_MAX_TMA)

            # otherwise, velocidade de subida na DEP está abaixo de 250KT
            else:
                # velocidade NÃO foi alterada ?
                if (0 == f_atv.i_atv_change_alt_vel) or (1 == f_atv.i_atv_change_alt_vel):
                    # velocidade do breakpoint é valida ?
                    if 0. < f_brk.f_brk_vel <= ldefs.D_VEL_MAX_TMA:
                        # demanda a velocidade da performance ou a velocidade do breakpoint, o que for menor
                        f_atv.f_atv_vel_dem = min(lf_vel, f_brk.f_brk_vel)

                    # otherwise, inválida...
                    else:
                        # demanda a velocidade da performance ou a velocidade limite 250KT, o que for menor
                        f_atv.f_atv_vel_dem = min(lf_vel, f_brk.f_brk_vel)

        # otherwise, altitude do breakpoint é maior que a altitude máxima na TMA...
        else:
            # velocidade NÃO foi alterada ?
            if (0 == f_atv.i_atv_change_alt_vel) or (1 == f_atv.i_atv_change_alt_vel):
                # breakpoint tem velocidade ?
                if f_brk.f_brk_vel > 0.:
                    # demanda a velocidade da performance ou velocidade do breakpoint, o que for menor
                    f_atv.f_atv_vel_dem = min(lf_vel, f_brk.f_brk_vel)

                # velocidade da performance maior que velocidade de demanda atual ?
                elif lf_vel > f_atv.f_atv_vel_dem:
                    # demanda a velocidade da performance (cruzeiro)
                    f_atv.f_atv_vel_dem = lf_vel

        # coordenada cartesiana ou temporal ?
        if f_brk.i_brk_t >= 0:
            # obtém a razão de subida de cruzeiro
            f_atv.f_atv_raz_sub = f_atv.ptr_trf_prf.f_prf_raz_sub_crz

        # tem gradiente entre os pontos ?
        if 0. != f_brk.f_brk_raz_vel:
            # calcula a razão de subida em função do gradiente
            f_atv.f_atv_raz_sub += f_atv.f_trf_vel_atu * f_brk.f_brk_raz_vel

        # otherwise, NÃO tem gradiente entre os pontos...
        else:
            # obtém a razão de subida da performance
            f_atv.f_atv_raz_sub = f_atv.ptr_trf_prf.f_prf_raz_sub_crz

    # aproximação ou aproximação perdida
    elif f_atv.en_trf_fnc_ope in [ldefs.E_APROXIMACAO, ldefs.E_APXPERDIDA]:
        # aproximação perdida ?
        if ldefs.E_APXPERDIDA == f_atv.en_trf_fnc_ope:
            # demanda a velocidade de subida na decolagem
            f_atv.f_atv_vel_dem = f_atv.ptr_trf_prf.f_prf_vel_sub_dec
            # former case, fall throught to next item

        # coordenada cartesiana ou temporal ?
        if f_brk.i_brk_t >= 0:
            # desacelerando ?
            if f_brk.f_brk_raz_vel <= 0.:
                # razão de desaceleração de descida na aproximação
                f_atv.f_atv_raz_sub = f_atv.ptr_trf_prf.f_prf_raz_des_apx

            # otherwise, acelerando...
            else:
                # razão de velocidade
                f_atv.f_atv_raz_sub = f_brk.f_brk_raz_vel

    # otherwise, função operacional não reconhecida...
    else:
        # logger
        l_log = logging.getLogger("obtem_brk::obtem_brk")
        l_log.setLevel(logging.ERROR)
        l_log.error(u"<E04: função operacional [{}] não reconhecida.".format(ldefs.DCT_FNC_OPE[f_atv.en_trf_fnc_ope]))

    # cooredenada coordenadas rumo/azimute ?
    if f_brk.i_brk_t < 0:
        # seleciona próxima fase
        f_atv.en_atv_fase = ldefs.E_FASE_RUMOALT

    # otherwise, outro tipo de coordenada...
    else:
        # seleciona próxima fase
        f_atv.en_atv_fase = ldefs.E_FASE_DIRPONTO

    # logger
    # M_LOG.info("obtem_brk:<<")

# < the end >--------------------------------------------------------------------------------------
