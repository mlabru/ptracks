#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
control_super

controle do supervisor

revision 0.2  2017/jan  mlabru
pep8 style conventions

revision 0.1  2016/dez  mlabru
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/01"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import multiprocessing
import Queue
import time

# model
import model.common.glb_data as gdata
import model.super.model_super as model

# view
import view.super.view_super as view

# control
import control.control_manager as control
import control.events.events_config as events
import control.common.glb_defs as gdefs
import control.config.config_super as config
import control.network.get_address as gaddr
import control.network.net_sender as sender

# < class CControlSuper >--------------------------------------------------------------------------

class CControlSuper(control.CControlManager):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # init super class
        super(CControlSuper, self).__init__()

        # herdados de CControlManager
        # self.app       # the application
        # self.event     # event manager
        # self.config    # opções de configuração
        # self.model     # model manager
        # self.view      # view manager
        # self.voip      # biblioteca de VoIP

        # load opções de configuração
        self.config = config.CConfigSuper(gdefs.D_CFG_FILE)
        assert self.config

        # dicionário de configuração
        self.__dct_config = self.config.dct_config
        assert self.__dct_config

        # cria a queue de envio de comando/controle/configuração
        self.__q_snd_cnfg = multiprocessing.Queue()
        assert self.__q_snd_cnfg

        # endereço de envio
        lt_ifce, ls_addr, li_port = gaddr.get_address(self.config, "net.cnfg")

        # cria o socket de envio de comando/controle/configuração
        self.__sck_snd_cnfg = sender.CNetSender(lt_ifce, ls_addr, li_port, self.__q_snd_cnfg)
        assert self.__sck_snd_cnfg

        # executa em modo interativo ?
        if self.__dct_config["spr.gui"]:

            # instancia o modelo
            self.model = model.CModelSuper(self)
            assert self.model

            # create view manager
            self.view = view.CViewSuper(self, self.model)
            assert self.view

    # ---------------------------------------------------------------------------------------------
    def run(self):
        """
        drive application
        """
        # clear to go
        assert self.__dct_config

        # model and view ok ?
        if (self.model is None) or (self.view is None):
            # termina a aplicação sem confirmação e sem envio de fim
            self.cbk_termina()

        # temporização de scheduler
        lf_tim_rrbn = self.__dct_config["tim.rrbn"]

        # keep things running
        gdata.G_KEEP_RUN = True

        # obtém o tempo inicial em segundos
        lf_now = time.time()

        # application loop
        while gdata.G_KEEP_RUN:
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
    def send(self):
        """
        send command
        """
        # clear to go
        assert self.__dct_config
        assert self.__q_snd_cnfg
        assert self.__sck_snd_cnfg

        # código da mensagem
        li_type = self.__dct_config["spr.type"]

        # código válido ?
        if li_type in gdefs.SET_MSG_SUPER:
            # build message
            ls_buff  = str(gdefs.D_MSG_VRS) + gdefs.D_MSG_SEP
            ls_buff += str(li_type) + gdefs.D_MSG_SEP
        
            # fast-track simulation ? 
            if gdefs.D_MSG_ACC == li_type:
                # acrescenta velocidade de execução 
                ls_buff += str(self.__dct_config["spr.acc"]) + gdefs.D_MSG_SEP
            
            # envia a mensagem
            self.__sck_snd_cnfg.send_data(ls_buff[:-1])
        
    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_config(self):
        return self.__dct_config

    # ---------------------------------------------------------------------------------------------
    @property
    def q_snd_cnfg(self):
        return self.__q_snd_cnfg

    @q_snd_cnfg.setter
    def q_snd_cnfg(self, f_val):
        self.__q_snd_cnfg = f_val

# < the end >--------------------------------------------------------------------------------------
