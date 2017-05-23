#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
flight_engine

the flight engine class holds information about a flight and the commands the flight has been given

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
import threading
import time

# libs
import libs.coords.coord_defs as cdefs

# model
import model.common.glb_data as gdata

import model.newton.cine.abort_prc as abnd
import model.newton.cine.cine_data as cindata
# import model.newton.cine.cine_solo as cinsolo
import model.newton.cine.cine_voo as cinvoo
import model.newton.cine.sentido_curva as scrv

import model.newton.defs_newton as ldefs
import model.piloto.comando_piloto as cmdpil

# control
import control.control_debug as cdbg
import control.common.glb_defs as gdefs

# < class CFlightEngine >--------------------------------------------------------------------------

class CFlightEngine(threading.Thread):
    """
    the object holding all information concerning a flight
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control, f_atv):
        """
        constructor
        
        @param f_control: control manager
        @param f_atv: aeronave ativa
        """
        # check input
        assert f_control
        assert f_atv

        # inicia a super classe
        super(CFlightEngine, self).__init__()

        # control manager
        self.__control = f_control
        assert self.__control

        # event manager
        # self.__event = f_control.event
        # assert self.__event

        # relógio da simulação
        self.__sim_time = f_control.sim_time
        assert self.__sim_time

        # model manager
        self.__model = f_control.model
        assert self.__model

        # exercício
        self.__exe = self.__model.exe
        assert self.__exe

        # dados da aeronave
        self.__atv = f_atv

        # context stack
        self.__stk_context = []

        # área de dados de cinemática
        self.__cine_data = cindata.CCineData()
        assert self.__cine_data

        # cinemática de solo
        # self.__cine_solo = cinsolo.CineSolo(self, self._aer)
        # assert self.__cine_solo

        # cinemática de vôo
        self.__cine_voo = cinvoo.CCineVoo(self, f_control)
        assert self.__cine_voo

    # ---------------------------------------------------------------------------------------------
    def __cmd_pil_altitude(self, f_atv, fo_cmd_pil, fen_cmd_ope):
        """
        comando de pilotagem de altitude
        """
        # check input
        assert f_atv

        # altitude desejada (demanda)
        if ldefs.E_ALT == fen_cmd_ope:
            # ajusta demanda pelo primeiro parâmetro (altitude)
            f_atv.f_atv_alt_dem = fo_cmd_pil.t_param_1[0] * cdefs.D_CNV_FT2M

        # obtém a altitude desejada (demanda)
        elif ldefs.E_NIV == fen_cmd_ope:
            # ajusta demanda pelo segundo parâmetro (nível)
            f_atv.f_atv_alt_dem = fo_cmd_pil.t_param_2[0] * 100 * cdefs.D_CNV_FT2M

        # senão,...
        else:
            # logger
            l_log = logging.getLogger("CFlightEngine::__cmd_pil_altitude")
            l_log.setLevel(logging.ERROR)
            l_log.error(u"<E01: comando operacional ({}) não existe.".format(fen_cmd_ope))

        # obtém o terceiro parâmetro (razão)
        lf_param_3 = fo_cmd_pil.t_param_3[0]

        # razão ?
        if (lf_param_3 is not None) and (lf_param_3 != 0.):
            # ajusta razão de subida/descida
            f_atv.f_atv_raz_sub = lf_param_3

    # ---------------------------------------------------------------------------------------------
    def __cmd_pil_curva(self, f_atv, fo_cmd_pil, fen_cmd_ope):
        """
        comando de pilotagem de curva
        """
        # check input
        assert f_atv

        # força aeronave a abandonar qualquer procedimento
        abnd.abort_prc(f_atv)

        # coloca a aeronave em manual
        f_atv.en_trf_fnc_ope = ldefs.E_MANUAL

        cdbg.M_DBG.debug("__cmd_pil_curva: fo_cmd_pil.t_param_1[0]: {}".format(fo_cmd_pil.t_param_1[0]))
        cdbg.M_DBG.debug("__cmd_pil_curva: fo_cmd_pil.t_param_2[0]: {}".format(fo_cmd_pil.t_param_2[0]))
        cdbg.M_DBG.debug("__cmd_pil_curva: fo_cmd_pil.t_param_3[0]: {}".format(fo_cmd_pil.t_param_3[0]))

        # curva a direita ?
        if ldefs.E_CDIR == fen_cmd_ope:
            # graus ?
            if (fo_cmd_pil.t_param_1 is not None) and fo_cmd_pil.t_param_1[1]:
                # obtém a proa desejada (demanda)
                cdbg.M_DBG.debug("__cmd_pil_curva: f_atv.f_atv_pro_dem (A): {}".format(f_atv.f_atv_pro_dem))
                f_atv.f_atv_pro_dem = (360. + f_atv.f_trf_pro_atu + fo_cmd_pil.t_param_1[0]) % 360.
                cdbg.M_DBG.debug("__cmd_pil_curva: f_atv.f_atv_pro_dem (D): {}".format(f_atv.f_atv_pro_dem))

            # proa ?
            elif (fo_cmd_pil.t_param_2 is not None) and fo_cmd_pil.t_param_2[1]:
                # obtém a proa desejada (demanda)
                cdbg.M_DBG.debug("__cmd_pil_curva: f_atv.f_atv_pro_dem (A): {}".format(f_atv.f_atv_pro_dem))
                f_atv.f_atv_pro_dem = fo_cmd_pil.t_param_2[0] % 360.
                cdbg.M_DBG.debug("__cmd_pil_curva: f_atv.f_atv_pro_dem (D): {}".format(f_atv.f_atv_pro_dem))

            # senão, curva indefinida...
            else:
                # proa negativa
                f_atv.f_atv_pro_dem = -1.

            # razão ?
            if (fo_cmd_pil.t_param_3 is not None) and (fo_cmd_pil.t_param_3[1]) and (fo_cmd_pil.t_param_3[0] != 0.):
                # curva direita (razão positiva)
                f_atv.f_atv_raz_crv = abs(fo_cmd_pil.t_param_3[0])

            else:
                # curva direita (razão positiva)
                f_atv.f_atv_raz_crv = abs(f_atv.f_atv_raz_crv)

        # curva a esquerda ?
        elif ldefs.E_CESQ == fen_cmd_ope:
            # graus ?
            if (fo_cmd_pil.t_param_1 is not None) and fo_cmd_pil.t_param_1[1]:
                # obtém a proa desejada (demanda)
                f_atv.f_atv_pro_dem = (360. + f_atv.f_trf_pro_atu - fo_cmd_pil.t_param_1[0]) % 360.

            # proa ?
            elif (fo_cmd_pil.t_param_2 is not None) and fo_cmd_pil.t_param_2[1]:
                # obtém a proa desejada (demanda)
                f_atv.f_atv_pro_dem = fo_cmd_pil.t_param_2[0] % 360.

            # senão, curva indefinida...
            else:
                # proa negativa
                f_atv.f_atv_pro_dem = -1.

            # razão ?
            if (fo_cmd_pil.t_param_3 is not None) and (fo_cmd_pil.t_param_3[1]) and (fo_cmd_pil.t_param_3[0] != 0.):
                # curva esquerda (razão negativa)
                f_atv.f_atv_raz_crv = -abs(fo_cmd_pil.t_param_3[0])

            else:
                # curva esquerda (razão negativa)
                f_atv.f_atv_raz_crv = -abs(f_atv.f_atv_raz_crv)

        # curva pelo menor ângulo ?
        elif ldefs.E_CMNR == fen_cmd_ope:
            # graus ?
            if (fo_cmd_pil.t_param_1 is not None) and fo_cmd_pil.t_param_1[1]:
                # obtém a proa desejada (demanda)
                f_atv.f_atv_pro_dem = (360. + f_atv.f_trf_pro_atu + fo_cmd_pil.t_param_1[0]) % 360.

            # proa ?
            elif (fo_cmd_pil.t_param_2 is not None) and fo_cmd_pil.t_param_2[1]:
                # obtém a proa desejada (demanda)
                f_atv.f_atv_pro_dem = fo_cmd_pil.t_param_2[0] % 360.

            # senão, curva indefinida...
            else:
                # proa negativa
                f_atv.f_atv_pro_dem = -1.

            # razão ?
            if (fo_cmd_pil.t_param_3 is not None) and (fo_cmd_pil.t_param_3[1]) and (fo_cmd_pil.t_param_3[0] != 0.):
                # razão de curva
                f_atv.f_atv_raz_crv = abs(fo_cmd_pil.t_param_3[0])

            else:
                # razão de curva
                f_atv.f_atv_raz_crv = abs(f_atv.f_atv_raz_crv)

            # força a curva pelo menor ângulo
            scrv.sentido_curva(f_atv)

        # proa ?
        elif ldefs.E_PROA == fen_cmd_ope:
            # obtém a proa desejada (demanda)
            f_atv.f_atv_pro_dem = fo_cmd_pil.t_param_2[0] % 360.

            # força a curva pelo menor ângulo
            scrv.sentido_curva(f_atv)

        # senão,...
        else:
            # logger
            l_log = logging.getLogger("CFlightEngine::__cmd_pil_curva")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: comando operacional ({}) não existe.".format(fen_cmd_ope))

    # ---------------------------------------------------------------------------------------------
    def __cmd_pil_decolagem(self, f_atv, fo_cmd_pil):
        """
        comando de pilotagem de decolagem
        """
        # check input
        assert f_atv

        # aeródromo e pista da decolagem
        f_atv.ptr_atv_aer, f_atv.ptr_atv_pst = self.__model.airspace.get_aer_pst(fo_cmd_pil.t_param_1[0], fo_cmd_pil.t_param_2[0])

        # função operacional
        f_atv.en_trf_fnc_ope = ldefs.E_DECOLAGEM

        # fase de verificar condições
        f_atv.en_atv_fase = ldefs.E_FASE_ZERO

    # ---------------------------------------------------------------------------------------------
    def __cmd_pil_dir_fixo(self, f_atv, fo_cmd_pil):
        """
        comando de pilotagem de dir_fixo
        """
        # check input
        assert f_atv

        # clear to go
        assert self.__cine_data

        # obtém o dicionário de fixos
        ldct_fix = self.__cine_voo.dct_fix
        assert ldct_fix is not None

        # obtém fixo a bloquear
        f_atv.ptr_atv_fix_prc = ldct_fix.get(fo_cmd_pil.t_param_1[0], None)

        # status da interceptação ao fixo
        self.__cine_data.v_interceptou_fixo = False

        # função operacional
        f_atv.en_trf_fnc_ope = ldefs.E_DIRFIXO

        # fase de verificar condições
        f_atv.en_atv_fase = ldefs.E_FASE_ZERO

    # ---------------------------------------------------------------------------------------------
    def __cmd_pil_espera(self, f_atv, fo_cmd_pil):
        """
        comando de pilotagem de espera
        """
        # check input
        assert f_atv

        # clear to go
        assert self.__model

        # obtém o primeiro parâmetro (número da espera)
        ls_prc = "ESP{:03d}".format(int(fo_cmd_pil.t_param_1[0]))

        # procedimento e função operacional
        f_atv.ptr_trf_prc, f_atv.en_trf_fnc_ope = self.__model.airspace.get_ptr_prc(ls_prc)

        # fase de verificar condições
        f_atv.en_atv_fase = ldefs.E_FASE_ZERO

    # ---------------------------------------------------------------------------------------------
    def __cmd_pil_pouso(self, f_atv, fo_cmd_pil):
        """
        comando de pilotagem de pouso
        """
        # check input
        assert f_atv

        # clear to go
        assert self.__model

        # aeródromo e pista do pouso
        f_atv.ptr_atv_aer, f_atv.ptr_atv_pst = self.__model.airspace.get_aer_pst(fo_cmd_pil.t_param_1[0], fo_cmd_pil.t_param_2[0])

        # função operacional
        f_atv.en_trf_fnc_ope = ldefs.E_POUSO

        # fase de verificar condições
        f_atv.en_atv_fase = ldefs.E_FASE_ZERO

    # ---------------------------------------------------------------------------------------------
    def __cmd_pil_trajetoria(self, f_atv, fo_cmd_pil):
        """
        comando de pilotagem de trajetória
        """
        # check input
        assert f_atv

        # clear to go
        assert self.__model

        # monta procedimento. Primeiro parâmetro do comando é o número da trajetória
        ls_prc = "TRJ{:03d}".format(int(fo_cmd_pil.t_param_1[0]))

        # procedimento e função operacional
        f_atv.ptr_trf_prc, f_atv.en_trf_fnc_ope = self.__model.airspace.get_ptr_prc(ls_prc)

        # fase de verificar condições
        f_atv.en_atv_fase = ldefs.E_FASE_ZERO

    # ---------------------------------------------------------------------------------------------
    def __cmd_pil_velocidade(self, f_atv, fo_cmd_pil, fen_cmd_ope):
        """
        comando de pilotagem de velocidade
        """
        # check input
        assert f_atv

        # velocidade IAS ?
        if ldefs.E_IAS == fen_cmd_ope:
            # obtém a velocidade desejada (demanda)
            f_atv.f_atv_vel_dem = fo_cmd_pil.t_param_1[0] * cdefs.D_CNV_KT2MS

        # velocidade MACH ?
        elif ldefs.E_MACH == fen_cmd_ope:
            # if f_atv.f_trf_alt_atu >= self.__exe.f_exe_niv_apr_mac:
                # obtém a velocidade desejada (demanda)
                # f_atv.f_trf_vel_mac_dem = fo_cmd_pil.t_param_1[0]

                # f_atv.f_atv_vel_dem = calcIASDemanda(f_atv.f_trf_vel_mac_dem,
                #                                      f_atv.f_atv_alt_dem,
                #                                      self.__exe.f_exe_var_temp_isa)
            pass

    # ---------------------------------------------------------------------------------------------
    def __comando_pilotagem(self, f_atv):
        """
        executa comandos de pilotagem
        """
        # check input
        assert f_atv

        # clear to go
        assert self.__cine_data

        # aeronave ativa ?
        if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):
            # aeronave não ativa. cai fora...
            return

        # (f_atv.en_trf_fnc_ope in [ldefs.E_NOPROC, ldefs.E_MANUAL, ldefs.E_DIRFIXO]):

        # inicializa campos referentes a procedimentos
        # f_atv.ptr_trf_bkp = None
        # f_atv.ptr_trf_prc = None

        # esvazia pilha de contexto
        self.__cine_data.i_cin_ptr = 0

        # obtém o comando de pilotagem atual
        lo_cmd_pil = f_atv.lst_atv_cmd_pil.pop(0)
        assert lo_cmd_pil

        cdbg.M_DBG.debug("__comando_pilotagem: lo_cmd_pil: {}".format(lo_cmd_pil))

        # obtém o comando operacional
        len_cmd_ope = lo_cmd_pil.en_cmd_ope

        # curva ou proa ?
        if len_cmd_ope in [ldefs.E_CDIR, ldefs.E_CESQ, ldefs.E_CMNR, ldefs.E_PROA]:
            # trata comando de curva ou proa
            self.__cmd_pil_curva(f_atv, lo_cmd_pil, len_cmd_ope)

        # velocidade ou mach ?
        elif len_cmd_ope in [ldefs.E_IAS, ldefs.E_MACH]:
            # trata comando de velocidade
            self.__cmd_pil_velocidade(f_atv, lo_cmd_pil, len_cmd_ope)

        # altitude ou nível ?
        elif len_cmd_ope in [ldefs.E_ALT, ldefs.E_DES, ldefs.E_NIV, ldefs.E_SUB]:
            # trata comando de altitude
            self.__cmd_pil_altitude(f_atv, lo_cmd_pil, len_cmd_ope)

        # decolagem ?
        elif ldefs.E_DECOLAGEM == len_cmd_ope:
            # trata comando de decolagem
            self.__cmd_pil_decolagem(f_atv, lo_cmd_pil)

        # direcionamento a fixo ?
        elif ldefs.E_DIRFIXO == len_cmd_ope:
            # trata comando de direcionamento a fixo
            self.__cmd_pil_dir_fixo(f_atv, lo_cmd_pil)

        # espera ?
        elif ldefs.E_ESPERA == len_cmd_ope:
            # trata comando de espera
            self.__cmd_pil_espera(f_atv, lo_cmd_pil)

        # põem em movimento ?
        #elif ldefs.E_MOV == len_cmd_ope:
            # inicia movimentação
            #f_atv.v_atv_movi = lf_param

        # pouso ?
        elif ldefs.E_POUSO == len_cmd_ope:
            # trata comando de pouso
            self.__cmd_pil_pouso(f_atv, lo_cmd_pil)

        # transponder ?
        elif ldefs.E_SSR == len_cmd_ope:
            # inicializa campo código transponder
            f_atv.i_trf_issr = lo_cmd_pil.t_param_1[0]

        # trajetória ?
        elif ldefs.E_TRAJETORIA == len_cmd_ope:
            # trata comando de trajetória
            self.__cmd_pil_trajetoria(f_atv, lo_cmd_pil)

        # visualiza ?
        #elif ldefs.E_VISU == len_cmd_ope:
            # inicia visualização
            #f_atv.v_trf_visu = lf_param

        # manual ?
        # elif ldefs.E_MANUAL == len_cmd_ope:
            # força aeronave a abandonar qualquer procedimento
            # abnd.abort_prc(f_atv)

            # estabelece fim de comandos de pilotagem
            # f_atv.lst_atv_cmd_pil = []

        # otherwise,...
        else:
            # inicia função operacional
            f_atv.en_trf_fnc_ope = len_cmd_ope

    # ---------------------------------------------------------------------------------------------
    def instruction(self, fs_cmd):
        """
        faz o parse da mensagem de pilotagem recebida

        @param fs_cmd: mensagem
        """
        # check input
        assert fs_cmd

        # clear to go
        assert self.__atv

        # coloca o comando na lista do tráfego
        self.__atv.lst_atv_cmd_pil.append(cmdpil.CComandoPil(fs_cmd))
        cdbg.M_DBG.debug("instruction: self.__atv.lst_atv_cmd_pil: {}".format(self.__atv.lst_atv_cmd_pil))

    # ---------------------------------------------------------------------------------------------
    def __move_no_solo(self, f_atv):
        """
        move uma aeronave no solo
        """
        # check input
        assert f_atv

        # aeronave ativa ?
        if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):
            # aeronave não ativa. cai fora...
            return

        # muda a função operacional para decolagem
        f_atv.en_trf_fnc_ope = ldefs.E_DECOLAGEM

        # fase de preparação
        f_atv.en_atv_fase = ldefs.E_FASE_ZERO

    # ---------------------------------------------------------------------------------------------
    def __procedimentos(self, f_atv):
        """
        verificar e direcionar a aeronave a um procedimento
        """
        # check input
        assert f_atv

        # clear to go
        assert self.__cine_data
        assert self.__cine_voo

        # aeronave ativa ?
        if (ldefs.E_ATIVA != f_atv.en_trf_est_atv) or (not f_atv.v_atv_ok):
            # aeronave não ativa. cai fora...
            return

        # função operacional é aproximação ?
        if ldefs.E_APROXIMACAO == f_atv.en_trf_fnc_ope:
            # aproximação
            self.__cine_voo.prc_aproximacao()

        # função operacional é aproximação perdida ?
        elif ldefs.E_APXPERDIDA == f_atv.en_trf_fnc_ope:
            # aproximação perdida
            self.__cine_voo.prc_apx_perdida()

        # X - arremeter em emergência ?
        # Y - "toque e arremetida" ?
        # Z - arremeter para a perna do vento ?
        # elif f_atv.c_atv_status_voo in ['X', 'Y', 'Z']:
            # procedimento de arremetida
            # self.__cine_voo.prc_arremeter ()

        # K - circuito, entrada pela perna do contra vento ?
        # V - circuito, entrada pela perna do vento ?
        # elif f_atv.c_atv_status_voo in ['K', 'V']:
            # procedimento de circuito
            # self.__cine_voo.prc_circuito ()

        # função operacional é decolagem ?
        elif ldefs.E_DECOLAGEM == f_atv.en_trf_fnc_ope:
            # decolagem
            self.__cine_voo.prc_decolagem()

        # função operacional é direcionamento a fixo ?
        elif ldefs.E_DIRFIXO == f_atv.en_trf_fnc_ope:
            # direcionamento a fixo
            self.__cine_voo.prc_dir_fixo()

        # função operacional é espera ?
        elif ldefs.E_ESPERA == f_atv.en_trf_fnc_ope:
            # espera
            self.__cine_voo.prc_espera()

        # função operacional é ILS ?
        elif ldefs.E_ILS == f_atv.en_trf_fnc_ope:
            # ILS
            pass  # self.__cine_voo.prc_ils()

        # função operacional é interceptação de radial ?
        elif ldefs.E_INTRADIAL == f_atv.en_trf_fnc_ope:
            # interceptação de radial
            pass  # self.__cine_voo.int_radial()

        # função operacional é manual ?
        elif ldefs.E_MANUAL == f_atv.en_trf_fnc_ope:
            # obtém o sentido de curva atual
            li_sinal = 1 if f_atv.f_atv_raz_crv >= 0 else -1

            # verifica qual deve ser a razão de curva (limite de 14000 pés)
            f_atv.f_atv_raz_crv = 1.5 if f_atv.f_trf_z > 4267.2 else 3.

            # ajusta o sentido de curva
            f_atv.f_atv_raz_crv *= li_sinal

        # O - peel-off ?
        # elif 'O' == f_atv.c_atv_status_voo:
            # procedimento de peel-off
            # self.__cine_voo.prc_peel_off ()

        # função operacional é pouso ?
        elif ldefs.E_POUSO == f_atv.en_trf_fnc_ope:
            # pouso
            self.__cine_voo.prc_pouso()

        # D - pouso direto ?
        # P - pousa movendo-se no circuito ?
        # elif f_atv.c_atv_status_voo in ['A', 'D', 'P']:
            # procedimento de pouso
            # self.__cine_voo.prc_pouso()

        # função operacional é subida ?
        elif ldefs.E_SUBIDA == f_atv.en_trf_fnc_ope:
            # subida
            self.__cine_voo.prc_subida()

        # função operacional é trajetória ?
        elif ldefs.E_TRAJETORIA == f_atv.en_trf_fnc_ope:
            # trajetória
            self.__cine_voo.prc_trajetoria()

        # senão, função operacional desconhecida
        else:
            # logger
            l_log = logging.getLogger("CFlightEngine::__procedimentos")
            l_log.setLevel(logging.WARNING)
            l_log.warning(u"<E02: função operacional {} desconhecida".format(ldefs.DCT_FNC_OPE[f_atv.en_trf_fnc_ope]))

    # ---------------------------------------------------------------------------------------------
    def run(self):
        """
        updates the position of all flights in the flight list
        """
        # clear to go
        assert self.__atv
        # assert self.__cine_solo
        assert self.__cine_voo

        # tempo de espera
        lf_tim_wait = float(self.__control.config.dct_config["tim.wait"])

        # enquanto não inicia...
        while not gdata.G_KEEP_RUN:
            # aguarda 1 seg
            time.sleep(1.)

        # timestamp of the last turn
        self.__atv.l_atv_time_ant = self.__sim_time.obtem_hora_sim()

        # inicia o timer
        lf_call_time = time.time()

        # loop de vida da aeronave
        while gdata.G_KEEP_RUN and self.__atv.v_atv_ok and (ldefs.E_ATIVA == self.__atv.en_trf_est_atv):
            # aeronave em movimento ?
            if 1:  # self.__atv.v_atv_movi:
                # existem comandos de pilotagem ?
                if len(self.__atv.lst_atv_cmd_pil) > 0:
                    # executa os comandos de pilotagem
                    self.__comando_pilotagem(self.__atv)

                # a aeronave está no solo ?
                # if self.__atv.v_atv_solo:
                    # movimenta no solo
                    # self.__move_no_solo()

                # atualiza dados dinâmicos da aeronave
                self.__cine_voo.update_cinematica()

                # tem procedimento ?
                if ldefs.E_NOPROC != self.__atv.en_trf_fnc_ope:
                    # executa procedimento da aeronave
                    self.__procedimentos(self.__atv)

            # recálculo da posição (.75s)
            lf_call_time += lf_tim_wait

            # obtém o tempo atual em segundos
            lf_now = time.time()

            # está adiantado ?
            if lf_call_time >= lf_now:
                # permite o scheduler
                time.sleep(lf_call_time - lf_now)

            # senão, está atrasado
            else:
                # logger
                l_log = logging.getLogger("CFlightEngine::run")
                l_log.setLevel(logging.WARNING)
                l_log.warning("<E01: atraso de {}(s).".format(lf_now - lf_call_time))

                # reinicia o timer
                lf_call_time = time.time()

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def atv(self):
        """
        get pointer para a aeronave ativa
        """
        return self.__atv

    # ---------------------------------------------------------------------------------------------
    @property
    def cine_data(self):
        """
        get pointer para área de dados da cinemática
        """
        return self.__cine_data

    # ---------------------------------------------------------------------------------------------
    @property
    def cine_solo(self):
        """
        get cinemática de solo
        """
        return self.__cine_solo

    # ---------------------------------------------------------------------------------------------
    @property
    def cine_voo(self):
        """
        get cinemática de vôo
        """
        return self.__cine_voo

    # ---------------------------------------------------------------------------------------------
    @property
    def stk_context(self):
        """
        get context stack
        """
        return self.__stk_context

# < the end >--------------------------------------------------------------------------------------
