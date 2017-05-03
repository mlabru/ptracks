#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
control_visil

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
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/12"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import multiprocessing
import os
import Queue
import sys
import time

import sip
sip.setapi('QString', 2)

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

# model 
import model.common.glb_data as gdata
import model.visil.model_visil as model

# view 
import view.visil.view_visil as view

# control 
# import control.control_debug as cdbg
import control.control_basic as control

import control.common.glb_defs as gdefs
import control.config.config_visil as config
import control.events.events_config as events

import control.network.get_address as gaddr
import control.network.net_http_get as httpsrv
import control.network.net_listener as listener

import control.simula.sim_time as stime

# < class CControlVisil >--------------------------------------------------------------------------

class CControlVisil(control.CControlBasic):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # inicia a super classe
        super(CControlVisil, self).__init__()

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
        self.config = config.CConfigVisil("tracks.cfg")
        assert self.config

        # obtém o dicionário de configuração
        self.__dct_config = self.config.dct_config
        assert self.__dct_config

        # create application
        self.create_app("visil")

        # create simulation statistics control
        # self.sim_stat = simStats.simStats()
        # assert self.sim_stat

        # create simulation time engine
        self.sim_time = stime.CSimTime(self)
        assert self.sim_time

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
        self.model = model.CModelVisil(self)
        assert self.model

        # get flight model
        self.__emula = self.model.emula
        assert self.__emula

        # create view manager
        self.view = view.CViewVisil(self, self.model)
        assert self.view

    # ---------------------------------------------------------------------------------------------
    def run(self):
        """
        drive application
        """
        # verifica condições de execução (I)
        assert self.event
        assert self.__emula
        assert self.__q_rcv_cnfg
        assert self.__sck_rcv_cnfg

        # temporização de eventos
        lf_tim_rrbn = self.config.dct_config["tim.rrbn"]

        # ativa o relógio da simulação
        self.start_time()

        # inicia o recebimento de mensagens de configuração
        self.__sck_rcv_cnfg.start()

        # starts flight model
        self.__emula.start()

        # keep things running
        gdata.G_KEEP_RUN = True

        # obtém o tempo inicial em segundos
        lf_now = time.time()

        # application loop
        while gdata.G_KEEP_RUN:
            try:
                # obtém um item da queue de configuração
                llst_data = self.__q_rcv_cnfg.get(False)

                # queue tem dados ?
                if llst_data:
                    # mensagem de aceleração ?
                    if gdefs.D_MSG_ACC == int(llst_data[0]):
                        # acelera/desacelera a aplicação
                        pass  # self.cbkAcelera(float(llst_data [ 1 ]))

                    # mensagem toggle call sign ?
                    elif gdefs.D_MSG_CSG == int(llst_data[0]):
                        # liga/desliga call-sign
                        pass  # self._oView.cbkToggleCallSign()

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

                    # mensagem de congelamento ?
                    elif gdefs.D_MSG_FRZ == int(llst_data[0]):
                        # freeze application
                        pass  # self._oView.cbkFreeze(False)

                    # mensagem toggle range mark ?
                    elif gdefs.D_MSG_RMK == int(llst_data[0]):
                        # liga/desliga range mark
                        pass  # self._oView.cbkToggleRangeMark()

                    # mensagem de endereço do servidor ?
                    elif gdefs.D_MSG_SRV == int(llst_data[0]):
                        # salva o endereço do servidor
                        self.__dct_config["srv.addr"] = str(llst_data[1])
                                                                                        
                    # mensagem de hora ?
                    elif gdefs.D_MSG_TIM == int(llst_data[0]):
                        # monta uma tupla com a mensagem de hora
                        lt_hora = tuple(int(l_s) for l_s in llst_data[1][1: -1].split(','))

                        # seta a hora de simulação
                        self.sim_time.set_hora(lt_hora)
                                                                                                                                        
                        # cria um evento de configuração de hora de simulação
                        l_evt = events.CConfigHora(self.sim_time.get_hora_format())
                        assert l_evt
                                                                                                                                                                                                                
                        # dissemina o evento
                        self.event.post(l_evt)
                                                                                                                                                                                                                                                                
                    # mensagem de descongelamento ?
                    elif gdefs.D_MSG_UFZ == int(llst_data[0]):
                        # defreeze application
                        pass  # self._oView.cbkDefreeze(False)

                    # senão, mensagem não reconhecida ou não tratavél
                    else:
                        # logger
                        l_log = logging.getLogger("CControlVisil::run")
                        l_log.setLevel(logging.WARNING)
                        l_log.warning("<E02: mensagem não reconhecida ou não tratável.")

            # em caso de não haver mensagens...
            except Queue.Empty:
                # salva o tempo anterior
                lf_ant = lf_now

                # obtém o tempo atual em segundos
                lf_now = time.time()

                # obtém o tempo final em segundos e calcula o tempo decorrido
                lf_dif = lf_now - lf_ant

                # está adiantado ?
                if lf_tim_rrbn > lf_dif:
                    # permite o scheduler
                    time.sleep((lf_tim_rrbn - lf_dif) * .99)

                # senão, atrasou...
                else:
                    # logger
                    l_log = logging.getLogger("CControlVisil::run")
                    l_log.setLevel(logging.WARNING)
                    l_log.warning("<E03: atrasou: {}".format(lf_dif - lf_tim_rrbn))

    # ---------------------------------------------------------------------------------------------
    def start_time(self):
        """
        DOCUMENT ME!
        """
        # verifica condições de execução
        assert self.sim_time

        # inicia o relógio da simulação
        self.sim_time.set_hora((0, 0, 0))

    # =============================================================================================
    # dados
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
        # check input
        assert f_val

        # save flight model
        self.__emula = f_val

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
        # check input
        assert f_val

        # save configuration listener
        self.__sck_rcv_cnfg = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def q_rcv_trks(self):
        """
        get tracks queue
        """
        return self.__q_rcv_trks

    @q_rcv_trks.setter
    def q_rcv_trks(self, f_val):
        """
        set tracks queue
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
        # check input
        assert f_val

        # save data listener
        self.__sck_rcv_trks = f_val

# < the end >--------------------------------------------------------------------------------------
