#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
trf_new

mantém os detalhes comuns de uma tráfego

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
import logging
import sys

# libs
import libs.coords.coord_defs as cdefs

# model
import model.items.aer_new as aer
import model.items.trf_model as model
import model.newton.defs_newton as ldefs

# control
import control.events.events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CTrfNEW >--------------------------------------------------------------------------------

class CTrfNEW(model.CTrfModel):
    """
    mantém os detalhes comuns de um tráfego.
    <trafego nTrf="1">
        <designador>A319</designador>
        <ssr>7001</ssr>
        <indicativo>TAM3912</indicativo>
        <origem>SBSP</origem>
        <destino>SBRJ</destino>
        <procedimento>TRJ307</procedimento>
        <coord> ... </coord>
        <temptrafego>0</temptrafego>
        <proa>153</proa>
        <velocidade>300</velocidade>
        <altitude>10000</altitude>
        <nivel>100</nivel>
        <rota>LOPES OPREV CANO</rota>
        <niveltrj>270</niveltrj>
        <veltrj>380</veltrj>
    </trafego>
    """
    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __init__(self, f_model, f_data=None, fs_ver="0001"):
        """
        @param f_model: event manager
        @param f_data: dados do tráfego
        @param fs_ver: versão do formato dos dados
        """
        # logger
        # M_LOG.info("__init__:>>")

        # check input
        assert f_model

        # init super class
        super(CTrfNEW, self).__init__(f_data)

        # salva o model manager localmente
        self.__model = f_model

        # salva o event manager localmente
        self.__event = f_model.event
        assert self.__event

        # heradados de CTrfModel
        # self.v_trf_ok         # flag ok
        # self.i_trf_id         # indicativo do tráfego
        # self.s_trf_ind        # descrição do tráfego
        # self.ptr_trf_prf      # performance (designador)
        # self.f_trf_x          # X (m) / longitude (gr)
        # self.f_trf_y          # Y (m) / latitude (gr)
        # self.f_trf_alt_atu    # altitude atual (m)
        # self.f_trf_pro_atu    # proa atual (gr)
        # self.f_trf_vel_atu    # velocidade atual (m/s)
        # self.i_trf_niv_aut    # nível autorizado (ft/100)
        # self.t_trf_hor_atv    # hora de ativação (h:m:s)

        # código transponder
        self.__i_trf_ssr = 0

        # aeródromo de origem
        self.__ptr_trf_aer_ori = None
        # aeródromo de destino
        self.__ptr_trf_aer_dst = None

        # latitude
        self.__f_trf_lat = 0.
        # longitude
        self.__f_trf_lng = 0.

        # altitude, nível & velocidade de trajetória
        self.__f_trf_alt_trj = 0.
        self.__i_trf_niv_trj = 0
        self.__f_trf_vel_trj = 0.

        # procedimento
        self.__ptr_trf_prc = None
        # nome do procedimento
        self.__s_trf_prc = ""

        # nome do arquivo de programação a seguir
        self.__s_trf_prg = ""

        # rota
        self.__s_trf_rota = ""
        # rvsm
        # self.__v_trf_rvsm = False

        # inicia estados da aeronave

        # estado de ativação (ESTATV) (ativa, cancelada, finalizada, pendente)
        self.__en_trf_est_atv = ldefs.E_PENDENTE

        # estado operacional (ESTOPE) (controlada, aleatória)
        self.__en_trf_est_ope = ldefs.E_AUTOMATICA

        # função operacional (FNCOPE) (manual, pln, dec, dirfix)
        self.__en_trf_fnc_ope = ldefs.E_NOPROC

        # função operacional anterior (FNCOPE)
        self.__en_trf_fnc_ope_ant = ldefs.E_NOPROC

        # recebeu dados ?
        if f_data is not None:
            # recebeu uma lista ?
            if isinstance(f_data, dict):
                # cria um tráfego com os dados da lista
                self.load_trf(f_data, fs_ver)

            # recebeu um tráfego ?
            elif isinstance(f_data, CTrfNEW):
                # copia o tráfego
                self.copy_trf(f_data)

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def copy_trf(self, f_trf):
        """
        copy constructor
        cria um novo tráfego a partir de um outro tráfego

        @param f_trf: tráfego a ser copiado
        """
        # logger
        # M_LOG.info("copy_trf:>>")

        # check input
        assert f_trf

        # copy super class attributes
        super(CTrfNEW, self).copy_trf(f_trf)

        # código transponder (charX4) (_sAtvCodT -> _i_trf_ssr) (H)
        # SSR (int) (OFF=0, HIJ=1 ,COM=2 ,EMG=3 )
        self.__i_trf_ssr = f_trf.i_trf_ssr

        # aeródromo de origem
        self.__ptr_trf_aer_ori = f_trf.ptr_trf_aer_ori
        # aeródromo de destino
        self.__ptr_trf_aer_dst = f_trf.ptr_trf_aer_dst

        # latitude da aeronave (H)
        self.f_trf_lat = f_trf.f_trf_lat
        # longitude da aeronave (H)
        self.f_trf_lng = f_trf.f_trf_lng

        # procedimento
        self.__ptr_trf_prc = f_trf.ptr_trf_prc
        # M_LOG.debug("procedimento: " + str(self.ptr_trf_prc))

        # nome do procedimento
        self.__s_trf_prc = f_trf.s_trf_prc

        # programação
        self.__s_trf_prg = f_trf.s_trf_prg
        # M_LOG.debug(u"programação: " + str(self.s_trf_prg))

        # rota
        self.__s_trf_rota = f_trf.s_trf_rota
        # rvsm
        # self.__v_trf_rvsm = f_trf.v_trf_rvsm

        # estado de ativação
        self.__en_trf_est_atv = f_trf.en_trf_est_atv
        # estado operacional
        self.__en_trf_est_ope = f_trf.en_trf_est_ope

        # função operacional
        self.__en_trf_fnc_ope = f_trf.en_trf_fnc_ope
        # função operacional anterior
        self.__en_trf_fnc_ope_ant = f_trf.en_trf_fnc_ope_ant

        # logger
        # M_LOG.info("copy_trf:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def load_trf(self, fdct_data, fs_ver="0001"):
        """
        carrega os dados de tráfego a partir de um dicionário (formato 0001)

        @param fdct_data: dicionário com os dados do tráfego
        @param fs_ver: versão do formato dos dados
        """
        # logger
        # M_LOG.info("load_trf:>>")

        # formato versão 0.01 ?
        if "0001" == fs_ver:
            # cria o tráfego
            self.make_trf(fdct_data)

        # senão, formato desconhecido
        else:
            # logger
            l_log = logging.getLogger("CTrfNEW::load_trf")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: formato desconhecido.")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # cai fora...
            sys.exit(1)

        # logger
        # M_LOG.info("load_trf:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def make_trf(self, fdct_data):
        """
        carrega os dados de tráfego a partir de um dicionário (formato 0001)

        @param fdct_data: dicionário com os dados do tráfego
        """
        # logger
        M_LOG.info("make_trf:>>")

        # identificação do tráfego
        if "nTrf" in fdct_data:
            self.i_trf_id = int(fdct_data["nTrf"])
            # M_LOG.debug("self.i_trf_id: " + str(self.i_trf_id))

        # indicativo do tráfego
        if "indicativo" in fdct_data:
            self.s_trf_ind = fdct_data["indicativo"]
            # M_LOG.debug("self.s_trf_ind: " + str(self.s_trf_ind))

        # código transponder
        if "ssr" in fdct_data:
            self.__i_trf_ssr = fdct_data["ssr"]
            # M_LOG.debug("self.i_trf_ssr: " + str(self.__i_trf_ssr))

        # performance (designador)
        if "designador" in fdct_data:
            # obtém o dicionário de performances
            ldct_prf = self.__model.dct_prf

            # obtém o designador da performance
            ls_prf_id = fdct_data["designador"].strip().upper()
            # M_LOG.debug("ls_prf_id: " + str(ls_prf_id))

            # existe a performance no dicionário ?
            if ls_prf_id in ldct_prf:
                # obtém a performance
                self.ptr_trf_prf = ldct_prf[ls_prf_id]
                assert self.ptr_trf_prf
                assert self.ptr_trf_prf.v_prf_ok

            # senão, não achou a performance
            else:
                # performance
                self.ptr_trf_prf = None

                # logger
                l_log = logging.getLogger("CTrfNEW::make_trf")
                l_log.setLevel(logging.NOTSET)
                l_log.error("<E01: performance [{}] não existe no dicionário.".format(ls_prf_id))

        # proa (gr)
        if "proa" in fdct_data:
            self.f_trf_pro_atu = float(fdct_data["proa"]) % 360.
            # M_LOG.debug("self.f_trf_pro_atu: " + str(self.f_trf_pro_atu))

        # velocidade (kt)
        if "velocidade" in fdct_data:
            self.f_trf_vel_atu = float(fdct_data["velocidade"]) * cdefs.D_CNV_KT2MS
            # M_LOG.debug("self.f_trf_vel_atu: " + str(self.f_trf_vel_atu))

        # altitude (ft)
        if "altitude" in fdct_data:
            self.f_trf_alt_atu = float(fdct_data["altitude"]) * cdefs.D_CNV_FT2M
            # M_LOG.debug("self.f_trf_alt_atu: " + str(self.f_trf_alt_atu))

        # posição (lat, lng)
        if "coord" in fdct_data:
            if len(fdct_data["coord"]) > 0:
                self.__f_trf_lat, self.__f_trf_lng = self.__model.coords.from_dict(fdct_data["coord"])
                # M_LOG.debug("self.__f_trf_lat: " + str(self.__f_trf_lat))
                # M_LOG.debug("self.__f_trf_lng: " + str(self.__f_trf_lng))

                # converte para xyz
                self.f_trf_x, self.f_trf_y, self.f_trf_z = self.__model.coords.geo2xyz(self.__f_trf_lat, self.__f_trf_lng, 0.)
                # M_LOG.debug("self.f_trf_x: " + str(self.f_trf_x))
                # M_LOG.debug("self.f_trf_y: " + str(self.f_trf_y))
                # M_LOG.debug("self.f_trf_z: " + str(self.f_trf_z))

            # senão,...
            else:
                # logger
                l_log = logging.getLogger("CTrfNEW::make_trf")
                l_log.setLevel(logging.WARNING)
                l_log.warning(u"<E02: tráfego [{}/{}] sem coordenadas.".format(self.i_trf_id, self.s_trf_ind))

        # origem
        if "origem" in fdct_data:
            # obtém o dicionário de aeródromos
            ldct_aer = self.__model.airspace.dct_aer

            # obtém o indicativo do aeródromo
            ls_aer_id = fdct_data["origem"]
            # M_LOG.debug("ls_aer_id: " + str(ls_aer_id))

            # existe o aeródromo no dicionário ?
            if ls_aer_id in ldct_aer:
                # obtém o aeródromo de origem
                self.__ptr_trf_aer_ori = ldct_aer[ls_aer_id]
                assert self.__ptr_trf_aer_ori

            # senão,...
            else:
                # aeródromo de origem
                self.__ptr_trf_aer_ori = None
                l_dctAer= {}
                l_dctAer["nAer"] = ls_aer_id

                # logger
                l_log = logging.getLogger("CTrfNEW::make_trf")
                l_log.setLevel(logging.WARNING)
                l_log.warning("<E03: aeródromo de origem [{}] não existe no dicionário.".format(ls_aer_id))
                l_log.warning("Aérodromo fake[{}] sendo criado.".format(ls_aer_id))
                self.__ptr_trf_aer_ori = aer.CAerNEW(self.__model, l_dctAer)

        # destino
        if "destino" in fdct_data:
            # obtém o dicionário de aeródromos
            ldct_aer = self.__model.airspace.dct_aer

            # obtém o indicativo do aeródromo
            ls_aer_id = fdct_data["destino"]
            # M_LOG.debug("ls_aer_id: " + str(ls_aer_id))

            # existe o aeródromo no dicionário ?
            if ls_aer_id in ldct_aer:
                # obtém o aeródromo de destino
                self.__ptr_trf_aer_dst = ldct_aer[ls_aer_id]
                assert self.__ptr_trf_aer_dst

            # senão,...
            else:
                # aeródromo de destino
                self.__ptr_trf_aer_dst = None
                l_dctAer= {}
                l_dctAer["nAer"] = ls_aer_id

                # logger
                l_log = logging.getLogger("CTrfNEW::make_trf")
                l_log.setLevel(logging.WARNING)
                l_log.warning("<E04: aeródromo de destino [{}] não existe no dicionário.".format(ls_aer_id))
                l_log.warning("Aérodromo fake[{}] sendo criado.".format(ls_aer_id))
                self.__ptr_trf_aer_dst = aer.CAerNEW(self.__model, l_dctAer)

        # procedimento
        if "procedimento" in fdct_data:
            self.__ptr_trf_prc, self.__en_trf_fnc_ope = self.__model.airspace.get_ptr_prc(fdct_data["procedimento"].strip().upper())
            self.__s_trf_prc = fdct_data["procedimento"].strip().upper()
            # M_LOG.debug("self.__ptr_trf_prc...: " + str(fdct_data["procedimento"].strip().upper()))
            # M_LOG.debug("self.__en_trf_fnc_ope: " + str(self.__en_trf_fnc_ope))

        # programação
        if "programa" in fdct_data:
            self.__s_trf_prg = fdct_data["programa"].strip()
            # M_LOG.debug("self.__s_trf_prg: " + str(fdct_data["programa"].strip()))

        # veltrj (kt)
        if "veltrj" in fdct_data:
            self.__f_trf_vel_trj = float(fdct_data["veltrj"]) * cdefs.D_CNV_KT2MS
            # M_LOG.debug("self.__f_trf_vel_trj: " + str(self.__f_trf_vel_trj))

        # nível da trajetória (ft/100)
        if "niveltrj" in fdct_data:
            self.__i_trf_niv_trj = int(fdct_data["niveltrj"])
            # M_LOG.debug("self.__i_trf_niv_trj: " + str(self.__i_trf_niv_trj))
            self.__f_trf_alt_trj = self.__i_trf_niv_trj * 100 * cdefs.D_CNV_FT2M
            # M_LOG.debug("self.__f_trf_alt_trj: " + str(self.__f_trf_alt_trj))

        # rota
        if "rota" in fdct_data:
            self.__s_trf_rota = fdct_data["rota"].strip().upper()
            # M_LOG.debug("self.__s_trf_rota: " + str(self.__s_trf_rota))

        # nível autorizado (ft/100)
        if "nivel" in fdct_data:
            self.i_trf_niv_aut = int(fdct_data["nivel"])
            # M_LOG.debug("self.i_trf_niv_aut: " + str(self.i_trf_niv_aut))

        # hora de ativação (h,m,s)
        if "temptrafego" in fdct_data:

            # obtém a hora inicial do exercício
            lt_hora_ini = self.__model.exe.t_exe_hor_ini
            M_LOG.debug("lt_hora_ini: " + str(lt_hora_ini))

            # obtém o tempo do tráfego (transformar em segundos)
            li_hor = int(float(fdct_data["temptrafego"]) * 60.)

            # calcula os minutos
            li_min = (li_hor // 60) % 60

            # calcula os segundos
            li_seg = li_hor % 60

            # calcula as horas
            li_hor = li_hor // 3600

            # calcula a hora inicial do tráfego no exercício
            self.t_trf_hor_atv = (lt_hora_ini[0] + li_hor,
                                  lt_hora_ini[1] + li_min,
                                  lt_hora_ini[2] + li_seg)
            M_LOG.debug("self.t_trf_hor_atv: " + str(self.t_trf_hor_atv))

        # (bool)
        self.v_trf_ok = True

        # logger
        M_LOG.info("make_trf:<<")

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def ptr_trf_aer_dst(self):
        """
        get aeródromo de destino
        """
        return self.__ptr_trf_aer_dst

    @ptr_trf_aer_dst.setter
    def ptr_trf_aer_dst(self, f_val):
        """
        set aeródromo de destino
        """
        self.__ptr_trf_aer_dst = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_trf_alt_trj(self):
        """
        get velocidade na trajetóra
        """
        return self.__f_trf_alt_trj

    @f_trf_alt_trj.setter
    def f_trf_alt_trj(self, f_val):
        """
        set velocidade na trajetóra
        """
        self.__f_trf_alt_trj = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def ptr_trf_aer_ori(self):
        """
        get aeródromo de origem
        """
        return self.__ptr_trf_aer_ori

    @ptr_trf_aer_ori.setter
    def ptr_trf_aer_ori(self, f_val):
        """
        set aeródromo de origem
        """
        self.__ptr_trf_aer_ori = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def en_trf_est_atv(self):
        """
        get estado de ativação
        """
        return self.__en_trf_est_atv

    @en_trf_est_atv.setter
    def en_trf_est_atv(self, f_val):
        """
        set estado de ativação
        """
        # check input
        assert f_val in ldefs.SET_EST_ATV

        # estado de ativação
        self.__en_trf_est_atv = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def en_trf_est_ope(self):
        """
        get estado operacional
        """
        return self.__en_trf_est_ope

    @en_trf_est_ope.setter
    def en_trf_est_ope(self, f_val):
        """
        set estado operacional
        """
        # check input
        assert f_val in ldefs.SET_EST_OPE

        # estado operacional
        self.__en_trf_est_ope = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def en_trf_fnc_ope(self):
        """
        get função operacional
        """
        return self.__en_trf_fnc_ope

    @en_trf_fnc_ope.setter
    def en_trf_fnc_ope(self, f_val):
        """
        set função operacional
        """
        # check input
        assert f_val in ldefs.SET_FNC_OPE

        # função operacional
        self.__en_trf_fnc_ope = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def en_trf_fnc_ope_ant(self):
        """
        get função operacional anterior
        """
        return self.__en_trf_fnc_ope_ant

    @en_trf_fnc_ope_ant.setter
    def en_trf_fnc_ope_ant(self, f_val):
        """
        set função operacional anterior
        """
        # check input
        assert f_val in ldefs.SET_FNC_OPE

        # função operacional anterior
        self.__en_trf_fnc_ope_ant = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_trf_lat(self):
        """
        get latitude
        """
        return self.__f_trf_lat

    @f_trf_lat.setter
    def f_trf_lat(self, f_val):
        """
        set latitude
        """
        # check input
        assert -90. <= f_val <= 90.

        # latitude
        self.__f_trf_lat = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_trf_lng(self):
        """
        get longitude
        """
        return self.__f_trf_lng

    @f_trf_lng.setter
    def f_trf_lng(self, f_val):
        """
        set longitude
        """
        # check input
        assert -180. <= f_val <= 180.

        # longitude
        self.__f_trf_lng = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def i_trf_niv_trj(self):
        """
        get nível na trajetóra
        """
        return self.__i_trf_niv_trj

    @i_trf_niv_trj.setter
    def i_trf_niv_trj(self, f_val):
        """
        set nível na trajetóra
        """
        self.__i_trf_niv_trj = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def ptr_trf_prc(self):
        """
        get procedimento
        """
        return self.__ptr_trf_prc

    @ptr_trf_prc.setter
    def ptr_trf_prc(self, f_val):
        """
        set procedimento
        """
        self.__ptr_trf_prc = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def s_trf_prc(self):
        """
        get nome do procedimento
        """
        return self.__s_trf_prc

    @s_trf_prc.setter
    def s_trf_prc(self, f_val):
        """
        set nome do procedimento
        """
        self.__s_trf_prc = f_val


    # ---------------------------------------------------------------------------------------------
    @property
    def s_trf_prg(self):
        """
        get programa
        """
        return self.__s_trf_prg

    @s_trf_prg.setter
    def s_trf_prg(self, f_val):
        """
        set programa
        """
        self.__s_trf_prg = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def s_trf_rota(self):
        """
        get rota
        """
        return self.__s_trf_rota

    @s_trf_rota.setter
    def s_trf_rota(self, f_val):
        """
        set rota
        """
        self.__s_trf_rota = f_val.strip().upper() if f_val is not None else ""

    # ---------------------------------------------------------------------------------------------
    '''@property
    def v_trf_rvsm(self):
        """
        get flag RVSM
        """
        return self.__v_trf_rvsm

    @v_trf_rvsm.setter
    def v_trf_rvsm(self, f_val):
        """
        set flag RVSM
        """
        self.__v_trf_rvsm = f_val
    '''
    # ---------------------------------------------------------------------------------------------
    @property
    def i_trf_ssr(self):
        """
        get código transponder
        """
        return self.__i_trf_ssr

    @i_trf_ssr.setter
    def i_trf_ssr(self, f_val):
        """
        set código transponder
        """
        self.__i_trf_ssr = int(f_val)

    # ---------------------------------------------------------------------------------------------
    @property
    def f_trf_vel_trj(self):
        """
        get velocidade na trajetóra
        """
        return self.__f_trf_vel_trj

    @f_trf_vel_trj.setter
    def f_trf_vel_trj(self, f_val):
        """
        set velocidade na trajetóra
        """
        self.__f_trf_vel_trj = f_val

# < the end >--------------------------------------------------------------------------------------
