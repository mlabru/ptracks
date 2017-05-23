#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dados_dinamicos

atualiza os dados dinâmicos da aeronave

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
import model.common.glb_data as gdata
import model.newton.defs_newton as ldefs

import model.newton.cine.calc_proa_demanda as cpd

# control
import control.control_debug as cdbg

# -------------------------------------------------------------------------------------------------
def __atualiza_altitude(f_atv, fl_delta_t, ff_vel_med):
    """
    atualiza a altitude da aeronave
    
    @param f_atv: pointer para struct aeronaves
    @param fl_delta_t: delta de tempo desde a ultima atualização
    @param ff_vel_med: velocidade média

    @return o ângulo calculado e o flag 'on demand'
    """
    # check input
    assert f_atv

    # checks
    if (ldefs.E_ATIVA != f_atv.en_trf_est_atv) or (not f_atv.v_atv_ok):
        # logger
        l_log = logging.getLogger("dados_dinamicos::__atualiza_altitude")
        l_log.setLevel(logging.ERROR) 
        l_log.error(u"<E01: aeronave não ativa.")
                        
        # cai fora...
        return 0, False

    # cdbg.M_DBG.debug("alt. atual..:[{}]".format(f_atv.f_trf_alt_atu))
    # cdbg.M_DBG.debug("alt. demanda:[{}]".format(f_atv.f_atv_alt_dem))

    # está variando a altitude ?
    if f_atv.f_trf_alt_atu != f_atv.f_atv_alt_dem:
        # em acidente (A), na final (F) ou toque (T) ?
        if f_atv.c_atv_status_voo in ['A', 'F', 'T']:
            # obtém a razão de descida atual (performance)
            # lf_vel_z = f_atv.ptr_trf_prf.f_prf_raz_des_apx
            lf_vel_z = f_atv.f_atv_raz_sub
            # cdbg.M_DBG.debug("razão de descida: " + str(lf_vel_z))

        # está subindo ?
        elif f_atv.f_trf_alt_atu < f_atv.f_atv_alt_dem:
            # obtém a razão de subida (performance)
            # lf_vel_z = f_atv.ptr_trf_prf.f_prf_raz_sub_crz
            lf_vel_z = f_atv.f_atv_raz_sub
            # cdbg.M_DBG.debug("razão de subida: " + str(lf_vel_z))

        # otherwise, está descendo
        else:
            # obtém a razão de descida (performance)
            # lf_vel_z = f_atv.ptr_trf_prf.f_prf_raz_des_crz
            lf_vel_z = f_atv.f_atv_raz_sub
            # cdbg.M_DBG.debug("razão de descida: " + str(lf_vel_z))

        # está subindo ?
        if f_atv.f_trf_alt_atu < f_atv.f_atv_alt_dem:
            # calcula a nova altitude (z = zo + vt)
            f_atv.f_trf_alt_atu += lf_vel_z * fl_delta_t

            # se ultrapassou a demanda, assume a demanda
            f_atv.f_trf_alt_atu = min(f_atv.f_trf_alt_atu, f_atv.f_atv_alt_dem)
            '''
            # aeronaves em subida, acima de FL280 (inclusive), devem manter o MACH constante, exceto
            # quando houver ordens de mudança de IAS ou MACH do Piloto
            if (ldefs.E_TRAJETORIA != f_atv.en_trf_fnc_ope) and (ldefs.E_SUBIDA != f_atv.en_trf_fnc_ope):
                # verifica se o nível está acima do FL280 e se houve uma ordem de mudança de IAS ou MACH do piloto
                if (f_atv.f_trf_alt_atu >= f_pExe.fExeNivRefMacCons) and (f_atv.f_atv_vel_mac_atu == f_atv.f_atv_vel_mac_dem):
                    # mantém o "MACH constante" na subida apartir do FL280
                    if f_atv.vAnvISOMACH:
                        # calcula e atualiza o IAS de demanda em função do MACH
                        f_atv.f_atv_vel_dem = calcIASDemanda(f_atv.f_atv_vel_mac_atu, f_atv.f_trf_alt_atu, gdata.G_EXE_VAR_TEMP_ISA)

                    else:
                        # calcula TAS e MACH porque houve uma ordem de mudança de IAS do Piloto
                        f_atv.f_atv_vel_tas = calcTAS (f_atv.f_trf_vel_atu, f_atv.f_trf_alt_atu, gdata.G_EXE_VAR_TEMP_ISA)
                        f_atv.f_atv_vel_mac_dem = calcMACH(f_atv.f_atv_vel_tas, f_atv.f_trf_alt_atu, gdata.G_EXE_VAR_TEMP_ISA)

                else:
                    # calcula a velocidade MACH de demanda para manter IAS constante
                    if f_atv.f_trf_alt_atu < f_pExe.fExeNivRefMacCons:
                        l_fVelTAS = calcTAS(f_atv.f_trf_vel_atu, f_atv.f_trf_alt_atu, gdata.G_EXE_VAR_TEMP_ISA)
                        f_atv.f_atv_vel_mac_dem = calcMACH(l_fVelTAS, f_atv.f_trf_alt_atu, gdata.G_EXE_VAR_TEMP_ISA)

            else:
                f_atv.f_atv_vel_tas = calcTAS (f_atv.f_trf_vel_atu, f_atv.f_trf_alt_atu, gdata.G_EXE_VAR_TEMP_ISA)
                f_atv.f_atv_vel_mac_dem = calcMACH(f_atv.f_atv_vel_tas, f_atv.f_trf_alt_atu, gdata.G_EXE_VAR_TEMP_ISA)
            '''
        # otherwise, está descendo
        else:
            # calcula a nova altitude (z = zo - vt)
            f_atv.f_trf_alt_atu -= lf_vel_z * fl_delta_t

            # se ultrapassou a demanda, assume a demanda
            f_atv.f_trf_alt_atu = max(f_atv.f_trf_alt_atu, f_atv.f_atv_alt_dem)
            '''
            # aeronaves em descida, acima de FL280 (inclusive), devem manter o MACH constante,
            # exceto quando houver ordens de mudança de IAS ou MACH do piloto ou procedimento automático
            if (ldefs.E_TRAJETORIA != f_atv.en_trf_fnc_ope) and (ldefs.E_SUBIDA != f_atv.en_trf_fnc_ope):
                # verifica se o nível está acima do FL280 e se houve uma ordem de mudança de IAS ou MACH do Piloto
                if ((f_atv.f_trf_alt_atu >= f_pExe.fExeNivRefMacCons) and (f_atv.f_atv_vel_mac_atu == f_atv.f_atv_vel_mac_dem):
                    # mantem o "MACH constante" na descida até o FL280
                    if f_atv.vAnvISOMACH:
                        # calcula e atualiza o IAS de demanda em função do MACH
                        f_atv.f_atv_vel_dem = calcIASDemanda(f_atv.f_atv_vel_mac_atu, f_atv.f_trf_alt_atu, gdata.G_EXE_VAR_TEMP_ISA)

                    else:
                        # calcula TAS e MACH pois houve uma ordem de mudança de IAS do Piloto
                        f_atv.f_atv_vel_tas = calcTAS (f_atv.f_trf_vel_atu, f_atv.f_trf_alt_atu, gdata.G_EXE_VAR_TEMP_ISA)
                        f_atv.f_atv_vel_mac_dem = calcMACH(f_atv.f_atv_vel_tas, f_atv.f_trf_alt_atu, gdata.G_EXE_VAR_TEMP_ISA)

                else:
                    # calcula a velocidade MACH de demanda para manter IAS constante
                    if f_atv.f_trf_alt_atu < f_pExe.fExeNivRefMacCons:
                        l_fVelTAS = calcTAS(f_atv.f_trf_vel_atu, f_atv.f_trf_alt_atu, gdata.G_EXE_VAR_TEMP_ISA)
                        f_atv.f_atv_vel_mac_dem = calcMACH(l_fVelTAS, f_atv.f_trf_alt_atu, gdata.G_EXE_VAR_TEMP_ISA)

            else:
                f_atv.f_atv_vel_tas = calcTAS (f_atv.f_trf_vel_atu, f_atv.f_trf_alt_atu, gdata.G_EXE_VAR_TEMP_ISA)
                f_atv.f_atv_vel_mac_dem = calcMACH(f_atv.f_atv_vel_tas, f_atv.f_trf_alt_atu, gdata.G_EXE_VAR_TEMP_ISA)
            '''
        # !REVER!
        # cdbg.M_DBG.debug("lf_vel_z.........: " + str(lf_vel_z))
        # cdbg.M_DBG.debug("ff_vel_med.......: " + str(ff_vel_med))

        # originalmente sem teste !
        if lf_vel_z < ff_vel_med:
            # cdbg.M_DBG.debug("ângulo de ataque: " + str(lf_vel_z / ff_vel_med))

            # calcula o ângulo de ataque (atitude)
            lf_alfa = math.asin(lf_vel_z / ff_vel_med)  # este é o original...

        # otherwise,... 
        else:
            # cdbg.M_DBG.debug("ângulo de ataque: " + str(ff_vel_med / lf_vel_z))

            # calcula o ângulo de ataque (atitude)
            lf_alfa = math.asin(ff_vel_med / lf_vel_z)  # alterado para "dar certo..."

        # seta flag 'on demand'
        lv_flag = True

    # otherwise, vôo nivelado
    else:
        # vôo nivelado, sem ângulo de ataque
        lf_alfa = 0.

        # seta flag 'on demand'
        lv_flag = False

    # retorna o ângulo calculado e o flag 'on demand'
    return lf_alfa, lv_flag

# -------------------------------------------------------------------------------------------------
def __atualiza_mach(f_atv):
    """
    atualiza a velocidade MACH atual da aeronave
    
    @param f_atv: pointer para struct aeronaves
    """
    # check input
    assert f_atv

    # checks
    if (ldefs.E_ATIVA != f_atv.en_trf_est_atv) or (not f_atv.v_atv_ok):
        # logger
        l_log = logging.getLogger("dados_dinamicos::__atualiza_mach")
        l_log.setLevel(logging.ERROR) 
        l_log.error(u"<E01: aeronave não ativa.")
                        
        # cai fora...
        return

    # variáveis locais
    lv_desacelera = False

    lf_vel_ias = 0.

    # atualiza a velocidade MACH atual da aeronave

    # diminui a velocidade ?
    if f_atv.f_atv_vel_mac_atu > f_atv.f_atv_vel_mac_dem:
        # diminui a velocidade da aeronave (v = vo - at)
        lf_vel_ias = f_atv.f_trf_vel_atu - f_atv.f_atv_acel

        # sinaliza condição de desaceleração
        lv_desacelera = True

    # aumente a velocidade ?
    elif f_atv.f_atv_vel_mac_atu < f_atv.f_atv_vel_mac_dem:
        # aumenta a velocidade da aeronave (v = vo + at)
        lf_vel_ias = f_atv.f_trf_vel_atu + f_atv.f_atv_acel

        # sinaliza condição de aceleração
        lv_desacelera = False

    # calcula e atualiza a velocidade TAS (true airspeed) da aeronave
    f_atv.f_atv_vel_tas = calcTAS(lf_vel_ias, f_atv.f_trf_alt_atu, gdata.G_EXE_VAR_TEMP_ISA)

    # calcula a velocidade MACH atual
    f_atv.f_atv_vel_mac_atu = calcMACH(f_atv.f_atv_vel_tas, f_atv.f_trf_alt_atu, gdata.G_EXE_VAR_TEMP_ISA)

    # aeronave desacelerando ?
    if lv_desacelera:
        # se ultrapassou a demanda ?
        if f_atv.f_atv_vel_mac_atu < f_atv.f_atv_vel_mac_dem:
            # assume a velocidade de demanda
            f_atv.f_atv_vel_mac_atu = f_atv.f_atv_vel_mac_dem

    # otherwise, acelerando...ultrapassou a demanda ?
    elif f_atv.f_atv_vel_mac_atu > f_atv.f_atv_vel_mac_dem:
        # assume a velocidade de demanda
        f_atv.f_atv_vel_mac_atu = f_atv.f_atv_vel_mac_dem

    # atualiza a velocidade atual
    f_atv.f_trf_vel_atu = calcIASDemanda(f_atv.f_atv_vel_mac_atu, f_atv.f_trf_alt_atu, gdata.G_EXE_VAR_TEMP_ISA)

    # atualiza velocidade de demanda da aeronave
    f_atv.f_atv_vel_dem = f_atv.f_trf_vel_atu

# -------------------------------------------------------------------------------------------------
def __atualiza_posicao(f_atv, f_cine_data, fl_delta_t, ff_vel_med, ff_alfa):
    """
    DOCUMENT ME!

    @param fl_delta_t: delta de tempo desde a ultima atualização
    @param ff_vel_med: velocidade media
    @param ff_alfa: ângulo de ataque (atitude)
    """
    # check input
    assert f_atv
    assert f_cine_data

    # checks
    if (ldefs.E_ATIVA != f_atv.en_trf_est_atv) or (not f_atv.v_atv_ok):
        # logger
        l_log = logging.getLogger("dados_dinamicos::__atualiza_posicao")
        l_log.setLevel(logging.ERROR) 
        l_log.error(u"<E01: aeronave não ativa.")
                        
        # cai fora...
        return

    # cdbg.M_DBG.debug("Tempo decorrido.: " + str(fl_delta_t))
    # cdbg.M_DBG.debug("Velocidade média: " + str(ff_vel_med))
    # cdbg.M_DBG.debug("Angulo de ataque: " + str(ff_alfa))
    # cdbg.M_DBG.debug("PosicaoAtu......: " + str((f_atv.f_trf_x, f_atv.f_trf_y)))

    # vôo nivelado ?
    if f_atv.f_trf_alt_atu == f_atv.f_atv_alt_dem:
        # atualiza a velocidade de solo da aeronave
        f_atv.f_atv_vel_gnd = f_atv.f_atv_vel_tas
        # cdbg.M_DBG.debug("vel. gnd:[{}]".format(f_atv.f_atv_vel_gnd))

    # otherwise,subindo ou descendo
    else:
        # calcula componente horizontal da velocidade (m/s)
        lf_vel_anv = (f_atv.f_atv_vel_tas ** 2) - (f_atv.f_atv_raz_sub ** 2)

        # retorna o módulo do vetor velocidade
        f_atv.f_atv_vel_gnd = math.sqrt(lf_vel_anv) if lf_vel_anv > 0. else 0.
        # cdbg.M_DBG.debug("f_atv_vel_gnd.:[{}]".format(f_atv.f_atv_vel_gnd))

    # converte a direção atual para radianos
    # lf_dir_atu = math.radians(f_atv.f_atv_dir_atu)
    lf_dir_atu = math.radians(f_atv.f_trf_pro_atu)

    # decompõem a velocidade em x e y em m/s (passo da aeronave) e salva na pilha (v.t)
    f_cine_data.f_delta_x = f_atv.f_atv_vel_gnd * fl_delta_t * math.sin(lf_dir_atu)
    f_cine_data.f_delta_y = f_atv.f_atv_vel_gnd * fl_delta_t * math.cos(lf_dir_atu)

    # decompõem a velocidade em seus componentes x e y
    # lf_vel_x = ff_vel_med * math.cos(ff_alfa) * math.cos(lf_dir_atu)
    # lf_vel_y = ff_vel_med * math.cos(ff_alfa) * math.sin(lf_dir_atu)
    # cdbg.M_DBG.debug("velocidade: x:[{}] y:[{}]".format(lf_vel_x, lf_vel_y))

    # verifica se há variação de velocidade (aceleração)...
    if f_atv.f_trf_vel_atu != f_atv.f_atv_vel_dem:
        # verifica se acelera ou freia
        li_sign = 1 if f_atv.f_trf_vel_atu < f_atv.f_atv_vel_dem else -1

        # soma a componente de aceleração (1/2 at^2) e guarda na pilha
        f_cine_data.f_delta_x += (li_sign * f_atv.f_atv_acel * (fl_delta_t ** 2) / 2.) * math.sin(lf_dir_atu)
        f_cine_data.f_delta_y += (li_sign * f_atv.f_atv_acel * (fl_delta_t ** 2) / 2.) * math.cos(lf_dir_atu)

    '''# aeronave em 'manual' ?
    if (ldefs.E_MANUAL == f_atv.en_trf_fnc_ope) or (ldefs.E_NOPROC == f_atv.en_trf_fnc_ope):
        # vento só para aeronave manual
        for li_ndx in xrange(len(self._exe_met.afMetNVento)):
            # faixa de vento correta ?
            if f_atv.f_trf_alt_atu <= self._exe_met.afMetNVento[li_ndx]:
                # faixa do vento
                f_cine_data.f_delta_x += self._exe_met.afMetVentoX[li_ndx] * fl_delta_t
                f_cine_data.f_delta_y += self._exe_met.afMetVentoY[li_ndx] * fl_delta_t

                break

        # calcula o vetor velocidade de solo
        f_atv.f_atv_vel_gnd = math.sqrt((f_cine_data.f_delta_x ** 2) + (f_cine_data.f_delta_y ** 2))
    '''
    # calcula os componentes x e y da posição atual (x = xo + vt)
    # lf_atu_x = f_atv.f_trf_x + (lf_vel_x * fl_delta_t)
    # lf_atu_y = f_atv.f_trf_y + (lf_vel_y * fl_delta_t)
    # cdbg.M_DBG.debug(u"posição atu: x:[{}] y:[{}]".format(lf_atu_x, lf_atu_y))

    # atualiza as coordenadas (x, y) da aeronave (x = xo + vot + 1/2 at^2)
    f_atv.f_trf_x += f_cine_data.f_delta_x
    f_atv.f_trf_y += f_cine_data.f_delta_y
    # cdbg.M_DBG.debug("coords atu: x:[{}] y:[{}]".format(f_atv.f_trf_x, f_atv.f_trf_y))

# -------------------------------------------------------------------------------------------------
def __atualiza_proa(f_atv, ff_delta_t):
    """
    atualiza a proa da aeronave
    
    @param f_atv: pointer para struct aeronaves
    @param ff_delta_t: delta de tempo desde a ultima atualização
    """
    # check input
    assert f_atv

    # checks (II)
    if (ldefs.E_ATIVA != f_atv.en_trf_est_atv) or (not f_atv.v_atv_ok):
        # logger
        l_log = logging.getLogger("dados_dinamicos::__atualiza_proa")
        l_log.setLevel(logging.ERROR) 
        l_log.error(u"<E01: aeronave não ativa.")
                        
        # cai fora...
        return False

    # cdbg.M_DBG.debug("__atualiza_proa:proa atual..:[{}]".format(f_atv.f_trf_pro_atu))
    # cdbg.M_DBG.debug("__atualiza_proa:proa demanda:[{}]".format(f_atv.f_atv_pro_dem))

    # está em vôo normal ?
    if 'N' == f_atv.c_atv_status_voo:
        # razão de curva em rota
        pass  # f_atv.f_atv_raz_crv = f_atv.ptr_trf_prf.f_prf_raz_crv_rot

    # otherwise, está em vôo...anormal ?
    else:
        # razão de curva no tráfego
        pass  # f_atv.f_atv_raz_crv = f_atv.ptr_trf_prf.f_prf_raz_crv_trf

    # cdbg.M_DBG.debug("__atualiza_proa:razão de curva:[{}]".format(f_atv.f_atv_raz_crv))

    # se proa demanda < 0 ?
    if f_atv.f_atv_pro_dem < 0.:
        # curva a aeronave indefinidamente
        lf_trf_pro_atu = f_atv.f_trf_pro_atu + (f_atv.f_atv_raz_crv * ff_delta_t)

        # normaliza a nova proa
        if lf_trf_pro_atu >= 360.:
            lf_trf_pro_atu -= 360.

        elif lf_trf_pro_atu < 0.:
            lf_trf_pro_atu += 360.

        # salva a proa atual
        f_atv.f_trf_pro_atu = round(lf_trf_pro_atu, 2)

    # aeronave curvando ?
    elif f_atv.f_trf_pro_atu != f_atv.f_atv_pro_dem:
        # obtém o sentido de curva
        # cdbg.M_DBG.debug("__atualiza_proa:en_atv_sentido_curva:[{}]".format(ldefs.DCT_SENTIDOS_CURVA[f_atv.en_atv_sentido_curva]))
        assert f_atv.en_atv_sentido_curva in ldefs.SET_SENTIDOS_CURVA

        # curva pelo menor ângulo ?
        if ldefs.E_MENOR == f_atv.en_atv_sentido_curva:
            # calcula diferença entre proas
            lf_dif_anter = abs(f_atv.f_trf_pro_atu - f_atv.f_atv_pro_dem)

            # maior que 180 ?
            if lf_dif_anter > 180.:
                # calcula o menor ângulo
                lf_dif_anter = 360. - lf_dif_anter

            # calcula nova proa
            lf_trf_pro_atu = f_atv.f_trf_pro_atu + (f_atv.f_atv_raz_crv * ff_delta_t)

            # normaliza a nova proa
            if lf_trf_pro_atu >= 360.:
                lf_trf_pro_atu -= 360.

            elif lf_trf_pro_atu < 0.:
                lf_trf_pro_atu += 360.

            # salva a proa atual
            f_atv.f_trf_pro_atu = round(lf_trf_pro_atu, 2)

            # calcula diferença entre proas
            lf_dif_atual = abs(f_atv.f_trf_pro_atu - f_atv.f_atv_pro_dem)

            # maior que 180 ?
            if lf_dif_atual > 180.:
                # calcula o menor ângulo
                lf_dif_atual = 360. - lf_dif_atual

            # está oscilando ?
            if (lf_dif_anter < abs(f_atv.f_atv_raz_crv)) and (lf_dif_anter < lf_dif_atual):
                # evita o efeito oscilante...
                f_atv.f_trf_pro_atu = f_atv.f_atv_pro_dem

        # curva à direita ?
        elif ldefs.E_DIREITA == f_atv.en_atv_sentido_curva:
            # está do "lado" certo ?
            if f_atv.f_atv_pro_dem < f_atv.f_trf_pro_atu:
                # ajusta o ângulo
                f_atv.f_atv_pro_dem += 360.

            # incrementa a proa atual do ângulo de rotação calculado
            f_atv.f_trf_pro_atu += f_atv.f_atv_raz_crv * ff_delta_t

            # se ultrapassou a demanda, assume a demanda
            f_atv.f_trf_pro_atu = round(min(f_atv.f_trf_pro_atu, f_atv.f_atv_pro_dem), 2)

        # otherwise, curva a esquerda
        else:
            # está do "lado" certo ?
            if f_atv.f_trf_pro_atu < f_atv.f_atv_pro_dem:
                # ajusta o ângulo
                f_atv.f_trf_pro_atu += 360.

            # decrementa a proa atual do ângulo de rotação calculado
            f_atv.f_trf_pro_atu -= f_atv.f_atv_raz_crv * ff_delta_t

            # se ultrapassou a demanda, assume a demanda
            f_atv.f_trf_pro_atu = round(max(f_atv.f_trf_pro_atu, f_atv.f_atv_pro_dem), 2)

    # otherwise, está linha reta
    else:
        # retorna flag 'on demand'
        return False

    # normaliza a nova proa
    if f_atv.f_trf_pro_atu >= 360.:
        f_atv.f_trf_pro_atu -= 360.

    elif f_atv.f_trf_pro_atu < 0.:
        f_atv.f_trf_pro_atu += 360.

    # converte a proa atual em direção
    # f_atv.f_atv_dir_atu = cincalc.conv_proa2direcao(f_atv.f_trf_pro_atu)

    # cdbg.M_DBG.debug("nova proa atual:[{}]".format(f_atv.f_trf_pro_atu))
    # cdbg.M_DBG.debug("nova direção atual:[{}]".format(f_atv.f_atv_dir_atu))

    # retorna flag 'on demand'
    return True

# -------------------------------------------------------------------------------------------------
def __atualiza_velocidade(f_atv, ff_delta_t):
    """
    atualiza a velocidade atual da aeronave
    
    @param f_atv: pointer para struct aeronaves
    @param ff_delta_t: delta de tempo desde a última atualização
    """
    # check input
    assert f_atv

    # checks (II)
    if (ldefs.E_ATIVA != f_atv.en_trf_est_atv) or (not f_atv.v_atv_ok):
        # logger
        l_log = logging.getLogger("dados_dinamicos::__atualiza_velocidade")
        l_log.setLevel(logging.ERROR) 
        l_log.error(u"<E01: aeronave não ativa.")
                                
        # cai fora...
        return 0.0001, False

    # cdbg.M_DBG.debug("__atualiza_velocidade:vel. atual..:[{}]".format(f_atv.f_trf_vel_atu))
    # cdbg.M_DBG.debug("__atualiza_velocidade:vel. demanda:[{}]".format(f_atv.f_atv_vel_dem))

    # salva velocidade atual para o cálculo da velocidade média
    lf_vel_ant = f_atv.f_trf_vel_atu

    # está variando a velocidade ?
    if f_atv.f_trf_vel_atu != f_atv.f_atv_vel_dem:
        # parando após pouso (S) ou toque e arremetida (T) ?
        # if f_atv.c_atv_status_solo in ['S', 'T']:
            # obtém a desaceleração máxima de pouso (performance)
            # f_atv.f_atv_acel = f_atv.ptr_trf_prf.f_prf_desacel_max_arr
            # cdbg.M_DBG.debug("desaceleração pouso: " + str(f_atv.f_atv_acel))

        # está acelerando ?
        if f_atv.f_trf_vel_atu < f_atv.f_atv_vel_dem:
            # aumenta a velocidade (v = vo + at)
            f_atv.f_trf_vel_atu += f_atv.f_atv_acel * ff_delta_t
            # cdbg.M_DBG.debug("__atualiza_velocidade:nova velocidade (ACC): " + str(f_atv.f_trf_vel_atu))

            # se ultrapassou a demanda, assume a demanda
            f_atv.f_trf_vel_atu = min(f_atv.f_trf_vel_atu, f_atv.f_atv_vel_dem)

        # está freando ?
        elif f_atv.f_trf_vel_atu > f_atv.f_atv_vel_dem:
            # diminui a velocidade da aeronave (v = vo - at)
            f_atv.f_trf_vel_atu -= f_atv.f_atv_acel * ff_delta_t
            # cdbg.M_DBG.debug("__atualiza_velocidade:nova velocidade (FRE): " + str(f_atv.f_trf_vel_atu))

            # se ultrapassou a demanda, assume a demanda
            f_atv.f_trf_vel_atu = max(f_atv.f_trf_vel_atu, f_atv.f_atv_vel_dem)

        # calcula a velocidade média do percurso
        lf_vel_med = (lf_vel_ant + f_atv.f_trf_vel_atu) / 2.
        # cdbg.M_DBG.debug("__atualiza_velocidade:velocidade média: " + str(lf_vel_med))

        # atualiza as velocidades TAS e MACH atual e demanda da aeronave
        f_atv.f_atv_vel_tas = f_atv.f_trf_vel_atu  # calcTAS (f_atv.f_trf_vel_atu, f_atv.f_trf_alt_atu, gdata.G_EXE_VAR_TEMP_ISA)
        # f_atv.f_atv_vel_mac_atu = calcMACH(f_atv.f_atv_vel_tas, f_atv.f_trf_alt_atu, gdata.G_EXE_VAR_TEMP_ISA)
        # f_atv.f_atv_vel_mac_dem = f_atv.f_atv_vel_mac_atu

        # seta flag 'on demand'
        lv_flag = True

    # otherwise, velocidade constante
    else:
        # calcula a velocidade média do percurso
        lf_vel_med = f_atv.f_trf_vel_atu

        # seta flag 'on demand'
        lv_flag = False

    # velocidade média = 0. ?
    if 0. == lf_vel_med:
        # evita divisão por zero
        lf_vel_med = 0.0001

    # retorna a velocidade media calculada e o flag 'on demand'
    return lf_vel_med, lv_flag

# -------------------------------------------------------------------------------------------------
def __calcula_tod(f_atv):
    """
    calcular o Ponto Ideal de Descida (Top of Decent - TOD)
    
    @param f_atv: pointer para struct aeronaves
    """
    # check input
    assert f_atv

    # checks (II)
    if (ldefs.E_ATIVA != f_atv.en_trf_est_atv) or (not f_atv.v_atv_ok):
        # logger
        l_log = logging.getLogger("dados_dinamicos::__calcula_tod")
        l_log.setLevel(logging.ERROR) 
        l_log.error(u"<E01: aeronave não ativa.")
                        
        # cai fora...
        return

    # variáveis locais
    li_tod = 0
    li_dst_anv_aer_arr = 0

    lf_dst_anv_pis_x = 0.     # X da distância da aeronave a pista
    lf_dst_anv_pis_y = 0.     # Y da distância da aeronave a pista

    lf_dst_anv_aer_arr = 0.   # distância aeronave a pista pouso
    lf_24_nm_antes_tod = 0.   # limite de 24NM antes do TOD

    # obtém o indicativo da aeronave para apresentação
    # memset(l_szAnvInd, '\0', sizeof l_szAnvInd)
    # strncpy(l_szAnvInd, f_atv.sAnvInd, xxANVIND_LEN)

    # obtém o indicativo do aeródromo de destino para apresentação
    # memset(l_szAerDst, '\0', sizeof l_szAerDst)
    # strncpy(l_szAerDst, f_atv.sAnvDestino, xxAERIND_LEN)

    # calcula distância da aeronave a pista pouso
    lf_dst_anv_pis_x = f_atv.f_anv_aer_dst_x - f_atv.f_trf_x
    lf_dst_anv_pis_y = f_atv.f_anv_aer_dst_y - f_atv.f_trf_y

    # calcula distância da aeronave a pista pouso (em linha reta)
    lf_dst_anv_aer_arr = math.sqrt((lf_dst_anv_pis_x ** 2) + (lf_dst_anv_pis_y ** 2))

    # ---------------------------------------------------------------------------------------------
    # +-- SE houver mudança de nível para maior ou menor
    # |   +-- SE aeronave encontra-se no intervalo 24NM antes do TOD
    # |   |   +-- SE a distância da aeronave ao TOD for menor ou igual a 5.5NM
    # |   |   |       considera que a aeronave chegou no TOD
    # |   |   |       sinaliza ao Piloto para limpar o campo TOD da tela
    # ---------------------------------------------------------------------------------------------
    if ((f_atv.f_atv_alt_dem > f_atv.f_anv_alt_bak) and (lf_dst_anv_aer_arr <= f_atv.f_anv_dst_tod + (24. * cdefs.D_CNV_NM2M))) or \
       ((f_atv.f_atv_alt_dem < f_atv.f_anv_alt_bak) and (lf_dst_anv_aer_arr <= f_atv.f_anv_dst_tod + (24. * cdefs.D_CNV_NM2M))):
        # evita que a aeronave esteja próximo do TOD e por uma mudança de altitude do próximo
        # ponto TRJ, seja calculado um novo TOD completamente distante do TOD original
        if lf_dst_anv_aer_arr <= (f_atv.f_anv_dst_tod + (5.5 * cdefs.D_CNV_NM2M)):

            # condição para o piloto não apresentar o valor até o TOD
            f_atv.v_atv_apr_tod = False

            # reinicia a flag de NM até o TOD
            f_atv.i_atv_24_nm_antes_tod = 0

            # reinicia campo de quantas NM faltam para chegar ao TOD
            f_atv.f_atv_dst_anv_tod = 0.

            # logger
            # M_LOG.info("__calcula_tod:<E01: ")

            # return
            return

    # calcula o Ponto Ideal de Descida (Top of Descent)
    f_atv.f_anv_dst_tod = ((f_atv.f_atv_alt_dem * cdefs.D_CNV_M2FT) - (f_atv.fAnvAerDstElev * cdefs.D_CNV_M2FT) + 50.) / math.tan(math.radians(3.)) / 6076. * cdefs.D_CNV_NM2M

    # calcula o limite de 24NM antes do TOD para alertar o piloto
    lf_24_nm_antes_tod = f_atv.f_anv_dst_tod + (24. * cdefs.D_CNV_NM2M)

    # calcula a distância da aeronave ao TOD
    if lf_dst_anv_aer_arr > lf_24_nm_antes_tod:
        # converte o TOD para NM
        li_tod = int(f_atv.f_anv_dst_tod * cdefs.D_CNV_M2NM)

        # converte a distância da aeronave ao aeródromo de destino para NM
        li_dst_anv_aer_arr = int(lf_dst_anv_aer_arr * cdefs.D_CNV_M2NM)

        # calcula quantas NM faltam para chegar ao TOD
        f_atv.f_atv_dst_anv_tod = li_dst_anv_aer_arr - li_tod

    # verifica se a aeronave esta dentro do intervalo 24NM até o TOD
    if (lf_dst_anv_aer_arr <= lf_24_nm_antes_tod) and (lf_dst_anv_aer_arr > f_atv.f_anv_dst_tod):
        # condição para o Piloto apresentar a ditância em NM até o TOD
        f_atv.v_atv_apr_tod = True

        # converte o TOD para NM
        li_tod = int(f_atv.f_anv_dst_tod * cdefs.D_CNV_M2NM)

        # converte a distância da aeronave ao aeródromo de destino para NM
        li_dst_anv_aer_arr = int(lf_dst_anv_aer_arr * cdefs.D_CNV_M2NM)

        # calcula quantas NM faltam para chegar ao TOD
        f_atv.i_atv_24_nm_antes_tod = li_dst_anv_aer_arr - li_tod
        f_atv.f_atv_dst_anv_tod = f_atv.i_atv_24_nm_antes_tod

        # normaliza cálculo
        f_atv.i_atv_24_nm_antes_tod = max(f_atv.i_atv_24_nm_antes_tod, 0)

    # aeronave chegou no TOD ?
    elif lf_dst_anv_aer_arr <= f_atv.f_anv_dst_tod:
        # condição para o Piloto não apresentar o valor até o TOD
        f_atv.v_atv_apr_tod = False

        # reinicia a flag de NM até o TOD
        f_atv.i_atv_24_nm_antes_tod = 0

        # reinicia campo de quantas NM faltam para chegar ao TOD
        f_atv.f_atv_dst_anv_tod = 0.

# -------------------------------------------------------------------------------------------------
def dados_dinamicos(f_atv, f_cine_data, ff_delta_t, f_stime):
    """
    atualiza os dados dinâmicos da aeronave

    @param f_atv: pointer para aeronave
    @param f_cine_data: pointer para CINDATA
    @param f_stime: pointer para sim_time
    """
    # check input
    assert f_atv
    assert f_cine_data
    assert f_stime

    # checks (II)
    if (ldefs.E_ATIVA != f_atv.en_trf_est_atv) or (not f_atv.v_atv_ok):
        # logger
        l_log = logging.getLogger("dados_dinamicos::dados_dinamicos")
        l_log.setLevel(logging.ERROR) 
        l_log.error(u"<E01: aeronave não ativa.")
                        
        # cai fora...
        return

    # calcula a nova velocidade e a velocidade média do percurso
    lf_vel_med, lb_vel = __atualiza_velocidade(f_atv, ff_delta_t)

    # if f_atv.f_atv_vel_mac_atu != f_atv.f_atv_vel_mac_dem:
        # calcula e atualiza a velocidade MACH atual da aeronave
        # __atualiza_mach(f_atv, ff_delta_t)

    # atualiza a proa da aeronave
    lb_proa = __atualiza_proa(f_atv, ff_delta_t)

    # calcula a nova altitude e a variação de altitude
    lf_alfa, lb_alt = __atualiza_altitude(f_atv, ff_delta_t, lf_vel_med)

    # atualiza a posição da aeronave
    __atualiza_posicao(f_atv, f_cine_data, ff_delta_t, lf_vel_med, lf_alfa)

    # cálculo da distância e radial ao radar
    f_atv.f_atv_dst_crd = math.sqrt((f_atv.f_trf_x ** 2) + (f_atv.f_trf_y ** 2))
    f_atv.f_atv_rad_crd = cpd.calc_proa_demanda(f_atv.f_trf_x, f_atv.f_trf_y)

    # cálculo do tempo estimado para a aeronave alcancar o fixo (ETO)
    if (f_atv.ptr_atv_fix_eto is not None) and f_atv.ptr_atv_fix_eto.v_fix_ok:
        # calcula distância da aeronave ao fixo ETO (x, y)
        lf_dst_anv_fix_x = f_atv.ptr_atv_fix_eto.f_fix_x - f_atv.f_trf_x
        lf_dst_anv_fix_y = f_atv.ptr_atv_fix_eto.f_fix_y - f_atv.f_trf_y

        # calcula distância da aeronave ao fixo (em linha reta)
        f_atv.f_atv_dst_fix = math.sqrt((lf_dst_anv_fix_x ** 2) + (lf_dst_anv_fix_y ** 2))

        # cálculo do ETO (sem aceleração)
        f_atv.i_atv_hora_eto = (f_atv.f_atv_dst_fix / f_atv.f_atv_vel_tas) + f_stime.get_hora_sim()  # f_pExe.iExeHoraAtu

    # otherwise, registra a falha no arquivo de log
    else:
        # logger
        # l_log = logging.getLogger("dados_dinamicos")
        # l_log.setLevel(logging.ERROR)
        # l_log.error("<E01: ETO fixo inexistente. aeronave:[%d/%s].", f_atv.i_trf_id, f_atv.s_trf_ind)
        pass

    # cálculo da distância e radial relativamente ao fixo de referência base para o procedimento de direcionamento a fixo
    if (f_atv.ptr_atv_fix_prc is not None) and f_atv.ptr_atv_fix_prc.v_fix_ok:
        # calcula distância da aeronave ao fixo (x, y)
        f_cine_data.f_dst_anv_fix_x = f_atv.ptr_atv_fix_prc.f_fix_x - f_atv.f_trf_x
        f_cine_data.f_dst_anv_fix_y = f_atv.ptr_atv_fix_prc.f_fix_y - f_atv.f_trf_y

        # calcula distância e radial da aeronave ao fixo (em linha reta)
        f_atv.f_atv_dst_fix = math.sqrt((f_cine_data.f_dst_anv_fix_x ** 2) + (f_cine_data.f_dst_anv_fix_y ** 2))
        f_atv.f_atv_rad_fix = cpd.calc_proa_demanda(-f_cine_data.f_dst_anv_fix_x, -f_cine_data.f_dst_anv_fix_y)

    # otherwise,...
    else:
        # força aeronave para vôo manual
        # f_atv.f_atv_pro_dem = f_atv.f_trf_pro_atu
        # f_atv.f_atv_vel_dem = f_atv.f_trf_vel_atu
        # f_atv.f_atv_alt_dem = f_atv.f_trf_alt_atu
        # f_atv.ptr_atv_fix_prc = None
        # f_atv.ptr_atv_fix_drd = None
        # f_atv.en_trf_fnc_ope = ldefs.E_MANUAL

        # logger
        # l_log = logging.getLogger("dados_dinamicos")
        # l_log.setLevel(logging.NOTSET)
        # l_log.error("E02: PRO fixo inexistente. aeronave:[%d/%s].", f_atv.i_trf_id, f_atv.s_trf_ind)
        pass

    # cálculo da distância e radial relativamento ao fixo de referência base para um comando de Azim/Dist
    if (f_atv.ptr_atv_fix_drd is not None) and f_atv.ptr_atv_fix_drd.v_fix_ok:
        # calcula distância da aeronave ao fixo (x, y)
        lf_delta_x = f_atv.ptr_atv_fix_drd.f_fix_x - f_atv.f_trf_x
        lf_delta_y = f_atv.ptr_atv_fix_drd.f_fix_y - f_atv.f_trf_y

        # calcula da distância e radial da aeronave ao fixo (em linha reta)
        f_atv.f_atv_dst_fix = math.sqrt((lf_delta_x ** 2) + (lf_delta_y ** 2))
        f_atv.f_atv_rad_fix = cpd.calc_proa_demanda(-lf_delta_x, -lf_delta_y)

    # otherwise,...
    else:
        # força a aeronave para vôo manual
        # f_atv.f_atv_pro_dem = f_atv.f_trf_pro_atu
        # f_atv.f_atv_vel_dem = f_atv.f_trf_vel_atu
        # f_atv.f_atv_alt_dem = f_atv.f_trf_alt_atu
        # f_atv.ptr_atv_fix_prc = None
        # f_atv.ptr_atv_fix_drd = None
        # f_atv.en_trf_fnc_ope = ldefs.E_MANUAL

        # logger
        # l_log = logging.getLogger("dados_dinamicos")
        # l_log.setLevel(logging.ERROR)
        # l_log.error("<E01: DRD fixo inexistente. aeronave:[%d/%s].", f_atv.i_trf_id, f_atv.s_trf_ind)
        pass

    # temporização para o SPI ?
    if 0 < f_atv.i_atv_spi < 18:
        # incrementa SPI
        f_atv.i_atv_spi += 1

    # otherwise,... 
    else:
        # reset SPI
        f_atv.i_atv_spi = -1

    # aeronaves em trajetória ou manual ?
    # if (ldefs.E_TRAJETORIA == f_atv.en_trf_fnc_ope) or (ldefs.E_NOPROC == f_atv.en_trf_fnc_ope):
        # cálculo do TOD maior que zero ?
        # if f_atv.f_anv_dst_tod > 0:
            # calcula o Ponto Ideal de Descida
            # __calcula_tod(f_atv)

# < the end >--------------------------------------------------------------------------------------
