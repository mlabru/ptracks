#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
control_piloto

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
__date__ = "2016/03"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import multiprocessing
import os
import Queue
import sys
import time

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui 

# model 
import model.common.glb_data as gdata
import model.piloto.model_piloto as model

# view 
import view.piloto.view_piloto as view

# control 
# import control.control_debug as cdbg
import control.control_basic as control

import control.common.glb_defs as gdefs
import control.config.config_piloto as config
import control.events.events_config as events

import control.network.get_address as gaddr
import control.network.net_http_get as httpsrv
import control.network.net_listener as listener
import control.network.net_sender as sender

import control.simula.sim_time as stime

# < class CControlPiloto >-------------------------------------------------------------------------

class CControlPiloto(control.CControlBasic):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # init super class
        super(CControlPiloto, self).__init__()

        # herdados de CControlManager
        # self.app       # the application
        # self.event     # event manager
        # self.config    # opções de configuração
        # self.model     # model manager
        # self.view      # view manager
        # self.voip      # biblioteca de VoIP

        # herdados de CControlBasic
        # self.ctr_flight    # flight control
        # self.sck_send      # net sender
        # self.sim_stat      # simulation statistics
        # self.sim_time      # simulation timer

        # carrega o arquivo com as opções de configuração
        self.config = config.CConfigPiloto("tracks.cfg")
        assert self.config

        # obtém o dicionário de configuração
        self.__dct_config = self.config.dct_config
        assert self.__dct_config

        # create application
        self.create_app("piloto")
                
        # create simulation statistics control
        # self.sim_stat = stats.SimStats()
        # assert self.sim_stat

        # create simulation time engine
        self.sim_time = stime.CSimTime(self)
        assert self.sim_time


        # cria a queue de envio
        self.__q_snd_cpil = multiprocessing.Queue()
        assert self.__q_snd_cpil

        # obtém o endereço de envio
        lt_ifce, ls_addr, li_port = gaddr.get_address(self.config, "net.cpil")

        # cria o socket de envio
        self.__sck_snd_cpil = sender.CNetSender(lt_ifce, ls_addr, li_port, self.__q_snd_cpil)
        assert self.__sck_snd_cpil


        # cria a queue de recebimento de comando/controle/configuração
        self.__q_rcv_cnfg = multiprocessing.Queue()
        assert self.__q_rcv_cnfg

        # obtém o endereço de recebimento
        lt_ifce, ls_addr, li_port = gaddr.get_address(self.config, "net.cnfg")

        # cria o socket de recebimento de comando/controle/configuração
        self.__sck_rcv_cnfg = listener.CNetListener(lt_ifce, ls_addr, li_port, self.__q_rcv_cnfg)
        assert self.__sck_rcv_cnfg


        # cria a queue de recebimento de pistas
        self.__q_rcv_trks = multiprocessing.Queue()
        assert self.__q_rcv_trks

        # obtém o endereço de recebimento
        lt_ifce, ls_addr, li_port = gaddr.get_address(self.config, "net.trks")

        # cria o socket de recebimento de pistas
        self.__sck_rcv_trks = listener.CNetListener(lt_ifce, ls_addr, li_port, self.__q_rcv_trks)
        assert self.__sck_rcv_trks


        # cria o socket de acesso ao servidor
        self.__sck_http = httpsrv.CNetHttpGet(self.event, self.config)
        assert self.__sck_http


        # instancia o modelo
        self.model = model.CModelPiloto(self)
        assert self.model

        # get flight model
        self.__emula = self.model.emula
        assert self.__emula

        # create view manager
        self.view = view.CViewPiloto(self, self.model)
        assert self.view

    # ---------------------------------------------------------------------------------------------
    def run(self):
        """
        drive application
        """
        # model and view ok ?
        if (self.model is None) or (self.view is None):
            # termina a aplicação sem confirmação e sem envio de fim
            self.cbk_termina()

        # clear to go
        assert self.event
        assert self.__emula
        assert self.__q_rcv_cnfg
        assert self.__sck_rcv_cnfg

        # temporização de scheduler
        lf_tim_rrbn = self.config.dct_config["tim.rrbn"]

        # keep things running
        gdata.G_KEEP_RUN = True

        # ativa o relógio
        self.start_time()

        # inicia o recebimento de mensagens de configuração
        self.__sck_rcv_cnfg.start()

        # starts flight model
        self.__emula.start()

        # obtém o tempo inicial em segundos
        lf_now = time.time()

        # application loop
        while gdata.G_KEEP_RUN:
            try:
                # obtém um item da queue de configuração (nowait)
                llst_data = self.__q_rcv_cnfg.get(False)
                # cdbg.M_DBG.debug("llst_data: {}".format(llst_data))

                # queue tem dados ?
                if llst_data:
                    # mensagem toggle call sign ?
                    if gdefs.D_MSG_CSG == int(llst_data[0]):
                        # liga/desliga callsign
                        pass  # self.view.cbk_toggle_callsign()

                    # mensagem configuração de exercício ?
                    elif gdefs.D_MSG_EXE == int(llst_data[0]):
                        # cria um evento de configuração de exercício
                        l_evt = events.CConfigExe(llst_data[1])
                        assert l_evt

                        # dissemina o evento
                        self.event.post(l_evt)

                    # mensagem de fim de execução ?
                    elif gdefs.D_MSG_FIM == int(llst_data[0]):
                        # termina a aplicação
                        self.cbk_termina()

                    # mensagem de endereço do servidor ?
                    elif gdefs.D_MSG_SRV == int(llst_data[0]):
                        # salva o endereço do servidor
                        self.__dct_config["srv.addr"] = str(llst_data[1])

                    # mensagem de hora ?
                    elif gdefs.D_MSG_TIM == int(llst_data[0]):
                        # monta uma tupla com a mensagem de hora
                        lt_hora = tuple(int(s) for s in llst_data[1][1: -1].split(','))

                        # seta a hora de simulação
                        self.sim_time.set_hora(lt_hora)

                        # cria um evento de configuração de hora de simulação
                        l_evt = events.CConfigHora(self.sim_time.get_hora_format())
                        assert l_evt

                        # dissemina o evento
                        self.event.post(l_evt)

                    # senão, mensagem não reconhecida ou não tratavél
                    else:
                        # logger
                        l_log = logging.getLogger("CControlPiloto::run")
                        l_log.setLevel(logging.WARNING)
                        l_log.warning("Mensagem não reconhecida ou não tratável.")

            # em caso de não haver mensagens...
            except Queue.Empty, ls_err:
                # salva o tempo anterior
                lf_ant = lf_now

                # obtém o tempo atual em segundos
                lf_now = time.time()

                # obtém o tempo final em segundos e calcula o tempo decorrido
                lf_dif = lf_now - lf_ant

                # está adiantado ?
                if lf_tim_rrbn > lf_dif:
                    # permite o scheduler
                    time.sleep(lf_tim_rrbn - lf_dif)

    # ---------------------------------------------------------------------------------------------
    def start_time(self):
        """
        DOCUMENT ME!
        """
        # clear to go
        assert self.sim_time

        # inicia o relógio da simulação
        self.sim_time.set_hora((0, 0, 0))

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def emula(self):
        """
        get flight model
        """
        return self.__emula

    @emula.setter
    def emula(self, f_val):
        """
        set flight model
        """
        self.__emula = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def q_rcv_cnfg(self):
        """
        get configuration queue
        """
        return self.__q_rcv_cnfg

    @q_rcv_cnfg.setter
    def q_rcv_cnfg(self, f_val):
        """
        set configuration queue
        """
        self.__q_rcv_cnfg = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_rcv_cnfg(self):
        """
        get configuration listener
        """
        return self.__sck_rcv_cnfg

    @sck_rcv_cnfg.setter
    def sck_rcv_cnfg(self, f_val):
        """
        set configuration listener
        """
        self.__sck_rcv_cnfg = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def q_snd_cpil(self):
        """
        get configuration queue
        """
        return self.__q_snd_cpil

    @q_snd_cpil.setter
    def q_snd_cpil(self, f_val):
        """
        set configuration queue
        """
        self.__q_snd_cpil = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_snd_cpil(self):
        """
        get configuration listener
        """
        return self.__sck_snd_cpil

    @sck_snd_cpil.setter
    def sck_snd_cpil(self, f_val):
        """
        set configuration listener
        """
        self.__sck_snd_cpil = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_http(self):
        """
        get http server listener
        """
        return self.__sck_http

    @sck_http.setter
    def sck_http(self, f_val):
        """
        set http server listener
        """
        self.__sck_http = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def q_rcv_trks(self):
        """
        get data queue
        """
        return self.__q_rcv_trks

    @q_rcv_trks.setter
    def q_rcv_trks(self, f_val):
        """
        set data queue
        """
        self.__q_rcv_trks = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_rcv_trks(self):
        """
        get data listener
        """
        return self.__sck_rcv_trks

    @sck_rcv_trks.setter
    def sck_rcv_trks(self, f_val):
        """
        set data listener
        """
        self.__sck_rcv_trks = f_val

# < the end >--------------------------------------------------------------------------------------
