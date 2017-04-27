#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
control_adapter

interface to CORE

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

revision 0.1  2017/abr  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/04"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import multiprocessing
import os
import Queue
import socket
import sys
import time

# core
from core.api import coreapi

# libs
import libs.coords.coord_defs as cdefs

# model 
import model.common.glb_data as gdata
import model.adapter.model_adapter as model

# control 
import control.control_debug as cdbg
import control.control_manager as control

import control.common.glb_defs as gdefs
import control.config.config_adapter as config
import control.events.events_config as events

import control.network.get_address as gaddr
import control.network.net_listener as listener

# < class CControlAdapter >------------------------------------------------------------------------

class CControlAdapter(control.CControlManager):
    """
    adapter control
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # inicia a super classe
        super(CControlAdapter, self).__init__()

        # herdados de CControlManager
        # self.event     # event manager
        # self.config    # opções de configuração
        # self.model     # model manager
        # self.view      # view manager
        # self.voip      # biblioteca de VoIP

        # carrega o arquivo com as opções de configuração
        self.config = config.CConfigAdapter("tracks.cfg")
        assert self.config

        # obtém o dicionário de configuração
        self.__dct_config = self.config.dct_config
        assert self.__dct_config

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

        # mensagem do newton
        self.__s_msg = None

        # instancia o modelo
        self.model = model.CModelAdapter(self)
        assert self.model

        # cria a trava da lista de vôos
        gdata.G_LCK_FLIGHT = multiprocessing.Lock()
        assert gdata.G_LCK_FLIGHT

    # ---------------------------------------------------------------------------------------------
    def __msg_trk(self, flst_data):
        """
        checks whether it's time to created another flight

        @param flst_data: mensagem de status
        """
        # clear to go
        # assert self.__dct_config is not None
                
        # callsign da aeronave
        # ls_callsign = flst_data[10]
        '''
        # aeronave já está no dicionário ?
        if ls_callsign in self.dct_flight:
            # atualiza os dados da aeronave
            pass  # self.dct_flight[ls_callsign].update_data(flst_data[1:])

        # senão, aeronave nova...
        else:
            # create new aircraft
            pass  # self.dct_flight[ls_callsign] = canv.CAircraftVisil(self, flst_data[1:])
            # assert self.dct_flight[ls_callsign]

                  gdefs.D_MSG_SEP + str(gdefs.D_MSG_NEW) + \
                  gdefs.D_MSG_SEP + str(self.__atv.i_trf_id) + \
                  gdefs.D_MSG_SEP + str(self.__atv.i_trf_ssr) + \
                  gdefs.D_MSG_SEP + str(self.__atv.i_atv_spi) + \
                  gdefs.D_MSG_SEP + str(round(lf_alt, 1)) + \
                  gdefs.D_MSG_SEP + str(round(lf_lat, 6)) + \
                  gdefs.D_MSG_SEP + str(round(lf_lng, 6)) + \
                  gdefs.D_MSG_SEP + str(round(self.__atv.f_trf_vel_atu * cdefs.D_CNV_MS2KT, 1)) + \
                  gdefs.D_MSG_SEP + str(round(self.__atv.f_atv_raz_sub, 1)) + \
                  gdefs.D_MSG_SEP + str(round(self.__atv.f_trf_pro_atu, 1)) + \
                  gdefs.D_MSG_SEP + str(self.__atv.s_trf_ind) + \
                  gdefs.D_MSG_SEP + str(self.__atv.ptr_trf_prf.s_prf_id) + \
                  gdefs.D_MSG_SEP + str(self.__sim_time.obtem_hora_sim() + \
                  gdefs.D_MSG_SEP + str(self.__atv.s_atv_icao24))

        '''
        # convert lat/lng/alt to x/y/z
        (l_x, l_y, l_z) = self.model.core_location.getxyz(float(flst_data[5]), float(flst_data[6]), int(float(flst_data[4]) * cdefs.D_CNV_FT2M))

        # build node message
        l_tlv_data = ""
        l_tlv_data += coreapi.CoreNodeTlv.packstring(1, int(flst_data[1]))

        # x / CORE_TLV_NODE_XPOS
        l_tlv_data += coreapi.CoreNodeTlv.packstring(32, l_x)

        # y / CORE_TLV_NODE_YPOS
        l_tlv_data += coreapi.CoreNodeTlv.packstring(33, l_y)

        # latitude / CORE_TLV_NODE_LAT
        l_tlv_data += coreapi.CoreNodeTlv.packstring(48, flst_data[5])

        # longitude / CORE_TLV_NODE_LONG
        l_tlv_data += coreapi.CoreNodeTlv.packstring(49, flst_data[6])

        # altitude / CORE_TLV_NODE_ALT
        l_tlv_data += coreapi.CoreNodeTlv.packstring(50, l_z)

        # mensagem / CORE_TLV_NODE_OPAQUE
        l_tlv_data += coreapi.CoreNodeTlv.packstring(80, self.__s_msg)

        # pack
        l_msg = coreapi.CoreNodeMessage.pack(0, l_tlv_data)

        # envia a mensagem para o CORE Daemon 
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setblocking(True)

        try:
            sock.connect(("localhost", coreapi.CORE_API_PORT))

        except Exception, e:
            print "Error connecting to %s:%s:\n\t%s" % ("localhost", coreapi.CORE_API_PORT, e)
            sys.exit(1)

        sock.sendall(l_msg)
        sock.close()

        # envia a mensagem para o node
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setblocking(False)

        try:
            sock.connect(("172.17.0.{}".format(int(flst_data[1])), coreapi.CORE_API_PORT))

        except Exception, ls_msg:
            # logger
            l_log = logging.getLogger("CControlAdapter::__msg_trk")
            l_log.setLevel(logging.WARNING)
            l_log.warning("<E03: erro: {}".format(ls_msg))

        sock.sendall(l_msg)
        sock.close()

    # ---------------------------------------------------------------------------------------------
    def process_cnfg(self, fq_rcv_cnfg):
        """
        processa a queue de mensagens de configuração
        """
        # clear to go
        # assert self.event
        assert fq_rcv_cnfg

        # temporização de eventos
        lf_tim_rrbn = self.config.dct_config["tim.rrbn"]

        # obtém o tempo inicial em segundos
        lf_now = time.time()

        # application loop
        while gdata.G_KEEP_RUN:
            try:
                # obtém um item da queue de configuração
                llst_data = fq_rcv_cnfg.get(False)

                # queue tem dados ?
                if llst_data:
                    # mensagem de fim de execução ?
                    if gdefs.D_MSG_FIM == int(llst_data[0]):
                        # termina a aplicação
                        self.cbk_termina()

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
                    time.sleep(lf_tim_rrbn - lf_dif)

                # senão, atrasou...+ de 5% ?
                elif (lf_dif - lf_tim_rrbn) > (lf_tim_rrbn * .05):
                    # logger
                    l_log = logging.getLogger("CControlAdapter::process_cnfg")
                    l_log.setLevel(logging.WARNING)
                    l_log.warning("<E03: atrasou: {}".format(lf_dif - lf_tim_rrbn))

    # ---------------------------------------------------------------------------------------------
    def process_trks(self, fq_rcv_trks):
        """
        processa a queue de mensagens de pista
        """
        # clear to go
        assert fq_rcv_trks

        # temporização de eventos
        lf_tim_rrbn = self.config.dct_config["tim.rrbn"]

        # obtém o tempo inicial em segundos
        lf_now = time.time()

        # loop
        while gdata.G_KEEP_RUN:
            try:
                # obtém um item da queue de pistas
                llst_data = fq_rcv_trks.get(False)
                # cdbg.M_DBG.debug("llst_data: {}".format(llst_data))

                # queue tem dados ?
                if llst_data:
                    # mensagem de status de aeronave ?
                    if gdefs.D_MSG_NEW == int(llst_data[0]):
                        # salva a mensagem
                        self.__s_msg = '#'.join(llst_data[1:])
                        # cdbg.M_DBG.debug("self.__s_msg: {}".format(self.__s_msg))
                        
                        # trata mensagem de status de aeronave
                        self.__msg_trk(llst_data)

                    # senão, mensagem não reconhecida ou não tratavél
                    else:
                        # logger
                        l_log = logging.getLogger("CControlAdapter::process_trks")
                        l_log.setLevel(logging.WARNING)
                        l_log.warning("<E04: mensagem não reconhecida ou não tratável. ({})".format(llst_data))

            # em caso de não haver mensagens...
            except Queue.Empty:
                # tempo anterior
                lf_ant = lf_now

                # tempo atual (em segundos)
                lf_now = time.time()

                # calcula o tempo decorrido
                lf_dif = lf_now - lf_ant

                # está adiantado ?
                if lf_tim_rrbn > lf_dif:
                    # permite o scheduler
                    time.sleep(lf_tim_rrbn - lf_dif)

                # senão, atrasou...+ de 5% ?
                elif (lf_dif - lf_tim_rrbn) > (lf_tim_rrbn * .05):
                    # logger
                    l_log = logging.getLogger("CControlAdapter::process_trks")
                    l_log.setLevel(logging.WARNING)
                    l_log.warning("<E05: atrasou: {}".format(lf_dif - lf_tim_rrbn))

    # ---------------------------------------------------------------------------------------------
    def run(self):
        """
        drive application
        """
        # clear to go
        assert self.__q_rcv_cnfg
        assert self.__sck_rcv_cnfg

        # keep things running
        gdata.G_KEEP_RUN = True

        # inicia o recebimento de mensagens de configuração
        self.__sck_rcv_cnfg.start()

        # cria o processo de tratamento de configuração
        lprc_cnfg = multiprocessing.Process(target=self.process_cnfg, args=(self.__q_rcv_cnfg,))
        lprc_cnfg.start()

        # inicia o recebimento de mensagens de pista
        self.__sck_rcv_trks.start()

        # cria o processo de tratamento de pistas
        lprc_trks = multiprocessing.Process(target=self.process_trks, args=(self.__q_rcv_trks,))
        lprc_trks.start()

        # aguarda o término dos processos
        lprc_cnfg.join()
        lprc_trks.join()

    # =============================================================================================
    # dados
    # =============================================================================================

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
