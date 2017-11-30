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
import control.network.get_ctrl_net as gctln
import control.network.net_listener as listener
import control.network.net_sender as sender

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


        # cria a queue de envio de pistas
        self.__q_snd_trks = multiprocessing.Queue()
        assert self.__q_snd_trks

        # endereço de envio
        lt_ifce, ls_addr, li_port = gctln.get_ctrl_net(self.config, "net.trks")

        # cria o socket de envio de pistas
        self.__sck_snd_trks = sender.CNetSender(lt_ifce, ls_addr, li_port, self.__q_snd_trks)


        # mensagem do newton
        self.__s_msg = None

        # instancia o modelo
        self.model = model.CModelAdapter(self)
        assert self.model

    # ---------------------------------------------------------------------------------------------
    def __msg_trk(self, flst_data):
        """
        checks whether it's time to created another flight

        @param flst_data: mensagem de status
        """
        # convert lat/lng/alt to x/y/z
        (l_x, l_y, l_z) = self.model.core_location.getxyz(float(flst_data[5]), float(flst_data[6]), int(float(flst_data[4]) * cdefs.D_CNV_FT2M))

        # build node message
        l_tlv_data = ""
        l_tlv_data += coreapi.CoreNodeTlv.packstring(1, int(flst_data[1]))

        # x / CORE_TLV_NODE_XPOS
        l_tlv_data += coreapi.CoreNodeTlv.packstring(32, l_x % 65536)

        # y / CORE_TLV_NODE_YPOS
        l_tlv_data += coreapi.CoreNodeTlv.packstring(33, l_y % 65536)

        # latitude / CORE_TLV_NODE_LAT
        l_tlv_data += coreapi.CoreNodeTlv.packstring(48, flst_data[5])

        # longitude / CORE_TLV_NODE_LONG
        l_tlv_data += coreapi.CoreNodeTlv.packstring(49, flst_data[6])

        # altitude / CORE_TLV_NODE_ALT
        l_tlv_data += coreapi.CoreNodeTlv.packstring(50, l_z % 65536)

        # mensagem / CORE_TLV_NODE_OPAQUE
        l_tlv_data += coreapi.CoreNodeTlv.packstring(80, self.__s_msg)

        # pack
        l_msg = coreapi.CoreNodeMessage.pack(0, l_tlv_data)

        # envia a mensagem para o CORE Daemon 
        self.__send_to("localhost", coreapi.CORE_API_PORT, l_msg, True)

        # envia a mensagem para o node
        self.__send_to("172.17.0.{}".format(int(flst_data[1])), coreapi.CORE_API_PORT, self.__s_msg)

    # ---------------------------------------------------------------------------------------------
    def process_cnfg(self, fq_rcv_cnfg):
        """
        processa a queue de mensagens de configuração

        @param fq_rcv_cnfg: queue receive ccc (command/control/config)
        """
        # clear to go
        assert fq_rcv_cnfg

        # temporização de eventos
        lf_tim_rrbn = float(self.config.dct_config["tim.rrbn"])

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

        @param fq_rcv_trks: queue receive tracks
        """
        # clear to go
        assert fq_rcv_trks

        # temporização de eventos
        lf_tim_core = float(self.config.dct_config["tim.core"])

        # obtém o tempo inicial em segundos
        lf_now = time.time()

        # loop
        while gdata.G_KEEP_RUN:
            try:
                # obtém um item da queue de pistas
                llst_data = fq_rcv_trks.get(False)

                # queue tem dados ?
                if llst_data:
                    # mensagem de status de aeronave ?
                    if gdefs.D_MSG_NEW == int(llst_data[0]):
                        # salva a mensagem
                        self.__s_msg = '#'.join(llst_data[1:])
                        
                        # trata mensagem de status de aeronave
                        self.__msg_trk(llst_data)

                        # mensagem a enviar
                        ls_msg = str(gdefs.D_MSG_VRS) + gdefs.D_MSG_SEP + \
                                 str(gdefs.D_MSG_COR) + gdefs.D_MSG_SEP + \
                                 self.__s_msg
                        #cdbg.M_DBG.debug("self.__s_msg: {}".format(ls_msg))

                        # envia a mensagem de pista para a cntl0net
                        self.__sck_snd_trks.send_data(ls_msg)

                    # mensagem do CORE ?
                    if gdefs.D_MSG_COR == int(llst_data[0]):
                        # ignore
                        pass

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
                if lf_tim_core > lf_dif:
                    # permite o scheduler
                    time.sleep(lf_tim_core - lf_dif)

                # senão, atrasou...+ de 5% ?
                elif (lf_dif - lf_tim_core) > (lf_tim_core * .05):
                    # logger
                    l_log = logging.getLogger("CControlAdapter::process_trks")
                    l_log.setLevel(logging.WARNING)
                    l_log.warning("<E05: atrasou: {}".format(lf_dif - lf_tim_core))

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
        assert lprc_cnfg

        lprc_cnfg.start()

        # inicia o recebimento de mensagens de pista
        self.__sck_rcv_trks.start()

        # cria o processo de tratamento de pistas
        lprc_trks = multiprocessing.Process(target=self.process_trks, args=(self.__q_rcv_trks,))
        assert lprc_trks

        lprc_trks.start()

        # aguarda o término dos processos
        lprc_cnfg.join()
        lprc_trks.join()

    # ---------------------------------------------------------------------------------------------
    def __send_to(self, fs_host, fi_port, fs_msg, fv_block=False):
        """
        send message to CORE Daemon 

        @param fs_host: host to connect
        @param fi_port: port
        @param fs_msg: message to send
        @param fv_block: flag wait until done (False)
        """
        # cria o socket
        l_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        assert l_sock

        # set blocking (wait untikl is done)
        l_sock.setblocking(fv_block)

        try:
            # connect to host
            l_sock.connect((fs_host, fi_port))

        # em caso de erro...
        except Exception, ls_err:
            # logger
            l_log = logging.getLogger("CControlAdapter::__send_to")
            l_log.setLevel(logging.WARNING)
            l_log.warning("<E06: erro connecting to {}:{}: {}".format(fs_host, fi_port, ls_err))

            # return
            return

        # send message
        l_sock.sendall(fs_msg)

        # fecha o socket
        l_sock.close()

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_rcv_cnfg(self):
        return self.__sck_rcv_cnfg

    @sck_rcv_cnfg.setter
    def sck_rcv_cnfg(self, f_val):
        # check input
        assert f_val

        # save configuration listener
        self.__sck_rcv_cnfg = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def q_rcv_trks(self):
        return self.__q_rcv_trks

    @q_rcv_trks.setter
    def q_rcv_trks(self, f_val):
        self.__q_rcv_trks = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_rcv_trks(self):
        return self.__sck_rcv_trks

    @sck_rcv_trks.setter
    def sck_rcv_trks(self, f_val):
        # check input
        assert f_val

        # save data listener
        self.__sck_rcv_trks = f_val

# < the end >--------------------------------------------------------------------------------------
