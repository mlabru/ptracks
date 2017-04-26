#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
atv_new

mantém os detalhes comuns de uma aeronave ativa

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
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import binascii
import os

# model
import model.items.trf_new as model
import model.newton.defs_newton as ldefs

# < class CAtvNEW >--------------------------------------------------------------------------------

class CAtvNEW(model.CTrfNEW):
    """
    informações de aeronave ativa
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_model, f_trf):
        """
        constructor

        @param f_model: control manager
        @param f_trf: tráfego a ativar

        @notes  é importante definir todo os parametros da aeronave antes de incluí-la no conjunto
                de aeronaves ativas. As aeronaves são ativadas considerando o vôo normal, isto é,
                AtvStatusVoo 'N'. No modulo Cinematica é definido o AtvTempoAnt para efeito de
                cálculo de movimento inicial. Caso a aeronave fosse incluida antes de se definir o
                Status, o sistema tomaria como verdadeiro o 'LIXO' que estivesse naquela posição no
                momento. Se for diferente de N, o AtvTempoAnt não seria definido e o primeiro
                movimento poderia mandar a aeronave para a uma posição errada, uma vez que o DeltaT
                seria muito grande
        """
        # check input
        assert f_model
        assert f_trf

        # init super class
        super(CAtvNEW, self).__init__(f_model, f_trf)

        # heradados de CTrfModel
        # self.i_trf_id         # indicativo da aeronave
        # self.s_trf_ind        # descrição da aeronave
        # self.ptr_trf_prf      # performance (designador)
        # self.f_trf_x          # X (m)/longitude (gr)
        # self.f_trf_y          # Y (m)/latitude (gr)
        # self.f_trf_z          # Z (m)/altitude (m)
        # self.f_trf_alt_atu    # altitude atual (m)
        # self.i_trf_niv_aut    # nível autorizado (ft/100)
        # self.f_trf_pro_atu    # proa atual (gr)
        # self.f_trf_vel_atu    # velocidade atual (m/s)
        # self.t_trf_hor_atv    # hora de ativação (h:m:s)

        # heradados de CTrfNEW
        # self.i_trf_ssr             # código transponder
        # self.ptr_trf_aer_ori       # aeródromo de origem
        # self.ptr_trf_aer_dst       # aeródromo de destino
        # self.f_trf_lat             # latitude
        # self.f_trf_lng             # longitude
        # self.f_trf_alt_trj         # altitude do tráfego na trajetória
        # self.f_trf_vel_trj         # velocidade do tráfego na trajetória
        # self.ptr_trf_prc           # procedimento
        # self.s_trf_rota            # rota
        # self.en_trf_est_atv        # estado de ativação
        # self.en_trf_est_ope        # estado operacional
        # self.en_trf_fnc_ope        # função operacional
        # self.en_trf_fnc_ope_ant    # função operacional anterior

        # [ informação local ]---------------------------------------------------------------------

        # flight engine da aeronave
        self.__atv_fe = None

        # código ICAO
        self.__s_atv_icao24 = binascii.b2a_hex(os.urandom(3))

        # check performance
        assert self.ptr_trf_prf
        assert self.ptr_trf_prf.v_prf_ok

        # em qual das faixas a aeronave está (int)
        # self._oAtvFaixaPer = None

        # esteira da aeronave (charX1)
        # self._c_prf_esteira = self.ptr_trf_prf.c_prf_esteira

        # razão de subida/descida (m/s) / razão de descida
        self.__f_atv_raz_sub = self.ptr_trf_prf.f_prf_raz_sub_crz    # self._dRazaoDescida (newton)
        # razão de curva (gr/s)
        self.__f_atv_raz_crv = self.ptr_trf_prf.f_prf_raz_crv_rot

        # aceleração da aeronave (m/s²)
        self.__f_atv_acel = self.ptr_trf_prf.f_prf_raz_var_vel

        # proa de demanda (gr)
        self.__f_atv_pro_dem = self.f_trf_pro_atu
        # proa de demanda informativa (gr)
        # self.__f_atv_pro_demInf = -51

        # velocidade de demanda (m/s)
        self.__f_atv_vel_dem = self.f_trf_vel_atu
        # velocidade de demanda informativa (m/s)
        # self.__f_atv_vel_demInf = -51

        # velocidade de solo (ground) (m/s)
        self.__f_atv_vel_gnd = self.f_trf_vel_atu

        # velocidade verdadeira (m/s)
        self.__f_atv_vel_tas = self.f_trf_vel_atu

        # altitude de demanda (m)
        self.__f_atv_alt_dem = self.f_trf_alt_atu
        # altitute de demanda informativa (m)
        # self.__f_atv_alt_demInf = -51

        # código transponder anterior (charX4)
        # self._sAtvSSRAnt = 0

        # status da aeronave
        # self._cStatus = 'A'

        # is the flight landed ? (T = pousada / F = voando)
        self.__v_atv_solo = self.f_trf_alt_atu == 0.
        # status de solo
        # !V!self.__c_atv_status_solo = 'P'

        # (bool) (T = movendo / F = parada)
        self.__v_atv_movi = self.f_trf_vel_atu > 0.
        # status de vôo
        self.__c_atv_status_voo = 'N'
        # flag de mudança de status
        # self._bAltStatus = False

        # flag de cancelamento da espera (prc_espera)
        self.__v_atv_cnl_esp = False

        # is the flight selected ?
        # !V!self._bSel = False
        # is the flight selected for navigation ?
        # !V!self._bNav = False

        # flags de navegação
        # !V!self._bSel = False
        # flag show percurso
        # !V!self._bShowPercurso = False

        # (bool) (T = visível / F = invisível)
        # self._vAtvVisu = False

        # if there exists alerts on flight
        self.__v_atv_alert = False

        # the current no. of alerts on flight
        # !V!self.__i_atv_alerts = 0

        # SPI on/off (int)
        self.__i_atv_spi = -1

        # (bool) ( T = A(alfa) / F = C(charlie))
        # self._vAtvModo = False
        # self._vAtvModo = True
        # flag de cancelamento de pista (bool)
        # self._vAtvCPis = False

        # fase do procedimento
        self.__en_atv_fase = ldefs.E_FASE_ZERO

        # lista de comandos de pilotagem
        self.__lst_atv_cmd_pil = []

        # número do procedimento (int)
        # self._iAtvNumProc = 0
        # número último procedimento (int)
        # self._iAtvNumUltProc = 0

        # inicia índice do 1*breakpoint
        self._ptr_atv_bkp = None      # !!!REVER!!!

        # número do breakpoint atual (int)
        # self._iAtvNumBkp = 0
        # número último breakPoint (int)
        # self._iAtvNumUltBkp = 0

        # direção atual
        self.__f_atv_dir_atu = f_trf.f_trf_pro_atu  # cineCalc.convProa2Direcao((self._dProa, self._oAer.getDifDeclinacao()))

        # flag de cálculo da distância-radial (bool)
        # self._vAtvCalDRd = False

        # distância da cabeça radar (100NM)
        self._f_atv_dst_crd = 185200.

        # fixo para cálculo de distância-radial (int) [cineVoo/dadosDinamicos]
        self.__ptr_atv_fix_drd = None
        # fixo para cálculo de ETO (int) [cineVoo/dadosDinamicos]
        self.__ptr_atv_fix_eto = None
        # fixo do procedimento de direção a fixo (int) [cineVoo/dadosDinamicos]
        self.__ptr_atv_fix_prc = None

        # pointer para aeródromo e pista do procedimento de pouso/decolagem
        self.__ptr_atv_aer = None
        self.__ptr_atv_pst = None

        # indicativo do fixo de entrada na área terminal (int)
        # self._sAtvFixEntrada = ""

        # distância ao fixo (m) [cineVoo/dadosDinamicos]
        self._f_atv_dst_fix = 0.
        # radial do fixo (float) [cineVoo/dadosDinamicos]
        self._f_atv_rad_fix = 0.

        # horário estimado até o fixo (s) [cineVoo/dadosDinamicos]
        self._f_atv_hora_eto = 0.

        # flag indicativo de mudança de altitude durante procedimentos TRJ e SUB
        self.__v_atv_change_alt = False
        # flag indicativo de mudança de velocidade durante procedimentos TRJ e SUB
        self.__v_atv_change_vel = False
        # mudança de altitude/velocidade na TRJ e SUB
        self.__i_atv_change_alt_vel = 0

        # mensagem associada a aeronave (charX70)
        # self._sAtvMensa = ""

        # número do terminal de pilotagem (int)
        # self._iAtvTrmPil = 0

        # sentido de curva (D = direita, E = esquerda, M = menor ângulo)
        self.__en_atv_sentido_curva = ldefs.E_MENOR

        # hora de ativação da aeronave (HORA)
        # self._iAtvTpoAtv = 0
        # obtám tempo de ativação da aeronave
        # self._iAtvTpoAtv = exe.iExeHoraIni + ( l_pRow->_iTAtiv * 60 )
        # !LOG! log4c_category_info ( l_log, "tempo ativação:[%d]", l_iTAtv )

        # hora de ativação da Mensagem (HORA)
        # self._iAtvAtvMens = 0
        # timestamp of the last turn
        self.__l_atv_time_ant = 0

        # is the flight active ? sure it is...
        self.en_trf_est_atv = ldefs.E_ATIVA

        # Ok (bool)
        self.__v_atv_ok = True

    # =============================================================================================
    #
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    def get_status_envio(self):
        """
        DOCUMENT ME!
        """
        # aeronave no solo ?
        if self.__v_atv_solo:
            # movimento no solo ?
            # !V!if self.__c_atv_status_solo in ['T', 'B', 'D', 'Y', 'S']:
                # !V!lc_status = 'M'

            # parada ?
            # !V!elif self.__c_atv_status_solo in ['X', 'P', 'G', 'R']:
                # !V!lc_status = 'P'

            # senão, acidente
            # !V!else:
                # !V!lc_status = 'A'

            # solo
            ls_status = "SP*"  # + self.__c_atv_status_solo + lc_status

        # senão, em vôo
        else:
            ls_status = 'V' + self.__c_atv_status_voo + '*'

        # status da aeronave
        return ls_status

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def f_atv_acel(self):
        """
        get aceleração da aeronave (m/s²)
        """
        return self.__f_atv_acel

    @f_atv_acel.setter
    def f_atv_acel(self, f_val):
        """
        set aceleração da aeronave (m/s²)
        """
        self.__f_atv_acel = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def v_atv_alert(self):
        """
        get flag alerta
        """
        return self.__v_atv_alert

    @v_atv_alert.setter
    def v_atv_alert(self, f_val):
        """
        set flag alerta
        """
        self.__v_atv_alert = f_val

    # ---------------------------------------------------------------------------------------------
    '''
    @property
    def i_atv_alerts(self):
        """
        get quantidade de alertas
        """
        return self.__i_atv_alerts

    @i_atv_alerts.setter
    def i_atv_alerts(self, f_val):
        """
        set quantidade de alertas
        """
        self.__i_atv_alerts = f_val
    '''
    # ---------------------------------------------------------------------------------------------
    @property
    def f_atv_alt_dem(self):
        """
        get altitude de demanda
        """
        return self.__f_atv_alt_dem

    @f_atv_alt_dem.setter
    def f_atv_alt_dem(self, f_val):
        """
        set altitude de demanda
        """
        self.__f_atv_alt_dem = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def ptr_atv_aer(self):
        """
        get pointer para aeródromo
        """
        return self.__ptr_atv_aer

    @ptr_atv_aer.setter
    def ptr_atv_aer(self, f_val):
        """
        set pointer para aeródromo
        """
        self.__ptr_atv_aer = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def v_atv_change_alt(self):
        """
        get flag indicativo de mudança de altitude durante procedimentos TRJ e SUB
        """
        return self.__v_atv_change_alt

    @v_atv_change_alt.setter
    def v_atv_change_alt(self, f_val):
        """
        set flag indicativo de mudança de altitude durante procedimentos TRJ e SUB
        """
        self.__v_atv_change_alt = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def i_atv_change_alt_vel(self):
        """
        get mudança de altitude/velocidade na TRJ e SUB
        """
        return self.__i_atv_change_alt_vel

    @i_atv_change_alt_vel.setter
    def i_atv_change_alt_vel(self, f_val):
        """
        set mudança de altitude/velocidade na TRJ e SUB
        """
        self.__i_atv_change_alt_vel = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def v_atv_change_vel(self):
        """
        get flag indicativo de mudança de velocidade durante procedimentos TRJ e SUB
        """
        return self.__v_atv_change_vel

    @v_atv_change_vel.setter
    def v_atv_change_vel(self, f_val):
        """
        set flag indicativo de mudança de velocidade durante procedimentos TRJ e SUB
        """
        self.__v_atv_change_vel = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def lst_atv_cmd_pil(self):
        """
        get lista de comandos de pilotagem
        """
        return self.__lst_atv_cmd_pil

    @lst_atv_cmd_pil.setter
    def lst_atv_cmd_pil(self, f_val):
        """
        set lista de comandos de pilotagem
        """
        self.__lst_atv_cmd_pil = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def v_atv_cnl_esp(self):
        """
        get flag cancelamento de espera (prc_espera)
        """
        return self.__v_atv_cnl_esp

    @v_atv_cnl_esp.setter
    def v_atv_cnl_esp(self, f_val):
        """
        set flag cancelamento de espera (prc_espera)
        """
        self.__v_atv_cnl_esp = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_atv_dir_atu(self):
        """
        get direção atual
        """
        return self.__f_atv_dir_atu

    @f_atv_dir_atu.setter
    def f_atv_dir_atu(self, f_val):
        """
        set direção atual
        """
        self.__f_atv_dir_atu = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def en_atv_fase(self):
        """
        get fase de processamento
        """
        return self.__en_atv_fase

    @en_atv_fase.setter
    def en_atv_fase(self, f_val):
        """
        set fase de processamento
        """
        self.__en_atv_fase = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def atv_fe(self):
        """
        get flight engine
        """
        return self.__atv_fe

    @atv_fe.setter
    def atv_fe(self, f_val):
        """
        set flight engine
        """
        # check input
        assert f_val

        # flight engine
        self.__atv_fe = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def ptr_atv_fix_drd(self):
        """
        get indicativo do fixo para cálculo de distância-radial
        """
        return self.__ptr_atv_fix_drd

    @ptr_atv_fix_drd.setter
    def ptr_atv_fix_drd(self, f_val):
        """
        set indicativo do fixo para cálculo de distância-radial
        """
        self.__ptr_atv_fix_drd = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def ptr_atv_fix_eto(self):
        """
        get indicativo do fixo para cálculo de ETO
        """
        return self.__ptr_atv_fix_eto

    @ptr_atv_fix_eto.setter
    def ptr_atv_fix_eto(self, f_val):
        """
        set indicativo do fixo para cálculo de ETO
        """
        self.__ptr_atv_fix_eto = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def ptr_atv_fix_prc(self):
        """
        get indicativo do fixo do procedimento de direção a fixo
        """
        return self.__ptr_atv_fix_prc

    @ptr_atv_fix_prc.setter
    def ptr_atv_fix_prc(self, f_val):
        """
        set indicativo do fixo do procedimento de direção a fixo
        """
        self.__ptr_atv_fix_prc = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def v_atv_movi(self):
        """
        get flag aeronave em movimento
        """
        return self.__v_atv_movi

    @v_atv_movi.setter
    def v_atv_movi(self, f_val):
        """
        set flag aeronave em movimento
        """
        self.__v_atv_movi = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def s_atv_icao24(self):
        """
        get ICAO id
        """
        return self.__s_atv_icao24

    @s_atv_icao24.setter
    def s_atv_icao24(self, f_val):
        """
        set ICAO id
        """
        self.__s_atv_icao24 = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def v_atv_ok(self):
        """
        get flag ok
        """
        return self.__v_atv_ok

    @v_atv_ok.setter
    def v_atv_ok(self, f_val):
        """
        set flag ok
        """
        self.__v_atv_ok = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_atv_pro_dem(self):
        """
        get proa de demanda
        """
        return self.__f_atv_pro_dem

    @f_atv_pro_dem.setter
    def f_atv_pro_dem(self, f_val):
        """
        set proa de demanda
        """
        # check input
        # assert 0. <= f_val <= 360.

        # proa demanda
        self.__f_atv_pro_dem = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def ptr_atv_pst(self):
        """
        get pointer para pista
        """
        return self.__ptr_atv_pst

    @ptr_atv_pst.setter
    def ptr_atv_pst(self, f_val):
        """
        set pointer para pista
        """
        self.__ptr_atv_pst = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_atv_raz_crv(self):
        """
        get razão de curva (gr/s)
        """
        return self.__f_atv_raz_crv

    @f_atv_raz_crv.setter
    def f_atv_raz_crv(self, f_val):
        """
        set razão de curva (gr/s)
        """
        self.__f_atv_raz_crv = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_atv_raz_sub(self):
        """
        get razão de subida/descida (m/s) / razão de descida
        """
        return self.__f_atv_raz_sub

    @f_atv_raz_sub.setter
    def f_atv_raz_sub(self, f_val):
        """
        set razão de subida/descida (m/s) / razão de descida
        """
        self.__f_atv_raz_sub = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def en_atv_sentido_curva(self):
        """
        get sentido de curva
        """
        return self.__en_atv_sentido_curva

    @en_atv_sentido_curva.setter
    def en_atv_sentido_curva(self, f_val):
        """
        set sentido de curva
        """
        # check input
        assert f_val in ldefs.S_SENTIDOS_CURVA

        # salva novo sentido de curva
        self.__en_atv_sentido_curva = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def v_atv_solo(self):
        """
        get flag solo
        """
        return self.__v_atv_solo

    @v_atv_solo.setter
    def v_atv_solo(self, f_val):
        """
        set flag solo
        """
        self.__v_atv_solo = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def i_atv_spi(self):
        """
        get flag spi
        """
        return self.__i_atv_spi

    @i_atv_spi.setter
    def i_atv_spi(self, f_val):
        """
        set flag spi
        """
        self.__i_atv_spi = f_val

    # ---------------------------------------------------------------------------------------------
    '''
    @property
    def c_atv_status_solo(self):
        """
        get status de solo
        """
        return self.__c_atv_status_solo

    @c_atv_status_solo.setter
    def c_atv_status_solo(self, f_val):
        """
        set status de solo
        """
        # check input
        assert f_val.upper() in ldefs.S_STATUS_SOLO

        # status de solo
        self.__c_atv_status_solo = f_val.upper()
    '''
    # ---------------------------------------------------------------------------------------------
    @property
    def c_atv_status_voo(self):
        """
        get status de vôo
        """
        return self.__c_atv_status_voo

    @c_atv_status_voo.setter
    def c_atv_status_voo(self, f_val):
        """
        set status de vôo
        """
        # check input
        assert f_val.upper() in ldefs.S_STATUS_VOO

        # status de vôo
        self.__c_atv_status_voo = f_val.upper()

    # ---------------------------------------------------------------------------------------------
    @property
    def l_atv_time_ant(self):
        """
        get timestamp of the last turn
        """
        return self.__l_atv_time_ant

    @l_atv_time_ant.setter
    def l_atv_time_ant(self, f_val):
        """
        set timestamp of the last turn
        """
        self.__l_atv_time_ant = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_atv_vel_dem(self):
        """
        get velocidade de demanda
        """
        return self.__f_atv_vel_dem

    @f_atv_vel_dem.setter
    def f_atv_vel_dem(self, f_val):
        """
        set velocidade de demanda
        """
        self.__f_atv_vel_dem = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_atv_vel_gnd(self):
        """
        get velocidade de solo (ground) (m/s)
        """
        return self.__f_atv_vel_gnd

    @f_atv_vel_gnd.setter
    def f_atv_vel_gnd(self, f_val):
        """
        set velocidade de solo (ground) (m/s)
        """
        self.__f_atv_vel_gnd = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_atv_vel_tas(self):
        """
        get velocidade verdadeira
        """
        return self.__f_atv_vel_tas

    @f_atv_vel_tas.setter
    def f_atv_vel_tas(self, f_val):
        """
        set velocidade verdadeira
        """
        self.__f_atv_vel_tas = f_val

# < the end >--------------------------------------------------------------------------------------
