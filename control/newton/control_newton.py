#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
control_newton

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
import multiprocessing
import Queue
import time

# mpi4py
# from mpi4py import MPI

# model 
import model.common.glb_data as gdata
import model.newton.model_newton as model

# view 
import view.newton.view_newton as view

# control 
import control.control_basic as control
# import control.control_debug as cdbg

import control.common.glb_defs as gdefs
import control.config.config_newton as config
import control.events.events_basic as events

import control.network.get_address as gaddr
import control.network.net_listener as listener
import control.network.net_sender as sender

import control.simula.sim_time as stime

# < class CControlNewton >-------------------------------------------------------------------------

class CControlNewton(control.CControlBasic):
    """
    control newton
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # init super class
        super(CControlNewton, self).__init__()

        # herdados de CControlManager
        # self.app       # the application
        # self.event     # event manager
        # self.config    # opções de configuração
        # self.model     # model manager
        # self.view      # view manager
        # self.voip      # biblioteca de VoIP

        # herdados de CControlBasic
        # self.ctr_flight    # flight control
        # self.sim_stat      # simulation statistics
        # self.sim_time      # simulation timer

        # carrega as opções de configuração
        self.config = config.CConfigNewton(gdefs.D_CFG_FILE)
        assert self.config

        # init MPI
        self.__mpi_comm = None  # MPI.COMM_WORLD
        # assert self.__mpi_comm

        # create simulation time engine
        self.sim_time = stime.CSimTime(self)
        assert self.sim_time


        # cria a queue de envio de comando/controle/configuração
        self.__q_snd_cnfg = multiprocessing.Queue()
        assert self.__q_snd_cnfg

        # endereço de envio
        lt_ifce, ls_addr, li_port = gaddr.get_address(self.config, "net.cnfg")

        # cria o socket de envio de comando/controle/configuração
        self.__sck_snd_cnfg = sender.CNetSender(lt_ifce, ls_addr, li_port, self.__q_snd_cnfg)
        assert self.__sck_snd_cnfg


        # cria a queue de envio de pistas
        self.__q_snd_trks = multiprocessing.Queue()
        assert self.__q_snd_trks

        # endereço de envio
        lt_ifce, ls_addr, li_port = gaddr.get_address(self.config, "net.trks")

        # cria o socket de envio de pistas
        self.__sck_snd_trks = sender.CNetSender(lt_ifce, ls_addr, li_port, self.__q_snd_trks)
        assert self.__sck_snd_trks


        # cria a queue de recebimento de comando/controle/configuração
        self.__q_rcv_cnfg = multiprocessing.Queue()
        assert self.__q_rcv_cnfg

        # endereço de recebimento
        lt_ifce, ls_addr, li_port = gaddr.get_address(self.config, "net.cnfg")

        # cria o socket de recebimento de comando/controle/configuração
        self.__sck_rcv_cnfg = listener.CNetListener(lt_ifce, ls_addr, li_port, self.__q_rcv_cnfg)
        assert self.__sck_rcv_cnfg

        # set as daemon
        # self.__sck_rcv_cnfg.daemon = True


        # cria a queue de recebimento de comandos de pilotagem
        self.__q_rcv_cpil = multiprocessing.Queue()
        assert self.__q_rcv_cpil

        # endereço de recebimento
        lt_ifce, ls_addr, li_port = gaddr.get_address(self.config, "net.cpil")

        # cria o socket de recebimento de comandos de pilotagem
        self.__sck_rcv_cpil = listener.CNetListener(lt_ifce, ls_addr, li_port, self.__q_rcv_cpil)
        assert self.__sck_rcv_cpil

        # set as daemon
        # self.__sck_rcv_cpil.daemon = True

      
        # instância o modelo
        self.model = model.CModelNewton(self)
        assert self.model

        # get flight emulation model
        self.__emula = self.model.emula
        assert self.__emula

        # create view manager
        self.view = view.CViewNewton(self.model, self)
        assert self.view

    # ---------------------------------------------------------------------------------------------
    def cbk_termina(self):
        """
        termina a aplicação
        """
        # clear to go
        assert self.event

        # cria um evento de fim de execução
        l_evt = events.CQuit()
        assert l_evt

        # dissemina o evento
        self.event.post(l_evt)

    # ---------------------------------------------------------------------------------------------
    def run(self):
        """
        drive application
        """
        # checks
        assert self.event
        assert self.__q_rcv_cnfg
        assert self.__sck_rcv_cnfg
        assert self.__emula

        # temporização de scheduler
        lf_tim_rrbn = self.config.dct_config["tim.rrbn"]

        # keep things running
        gdata.G_KEEP_RUN = True

        # ativa o relógio
        self.start_time()

        # inicia o recebimento de mensagens de comando/controle/configuração(ccc)
        self.__sck_rcv_cnfg.start()

        # starts flight model
        self.__emula.start()

        # obtém o tempo inicial em segundos
        lf_now = time.time()

        # starts web server
        self.view.start()

        # application loop
        while gdata.G_KEEP_RUN:
            try:
                # obtém um item da queue de mensagens de comando/controle/configuração (nowait)
                llst_data = self.__q_rcv_cnfg.get(False)
                # cdbg.M_DBG.debug("llst_data: {}".format(llst_data))

                # queue tem dados ?
                if llst_data:
                    # mensagem de fim de execução ?
                    if gdefs.D_MSG_FIM == int(llst_data[0]):
                        # termina a aplicação sem confirmação e sem envio de fim
                        self.cbk_termina()

                    # mensagem de aceleração ?
                    elif gdefs.D_MSG_ACC == int(llst_data[0]):
                        # acelera/desacelera a aplicação
                        self.sim_time.cbk_acelera(float(llst_data[1]))

                    # mensagem de congelamento ?
                    elif gdefs.D_MSG_FRZ == int(llst_data[0]):
                        # salva a hora atual
                        self.sim_time.cbk_congela()

                    # mensagem de descongelamento ?
                    elif gdefs.D_MSG_UFZ == int(llst_data[0]):
                        # restaura a hora
                        self.sim_time.cbk_descongela()

                    # senão, mensagem não reconhecida ou não tratavél
                    else:
                        # mensagens não tratadas ?  
                        if int(llst_data[0]) in [gdefs.D_MSG_EXE, gdefs.D_MSG_SRV, gdefs.D_MSG_TIM]:
                            # próxima mensagem
                            continue

                        # logger
                        l_log = logging.getLogger("CControlNewton::run")
                        l_log.setLevel(logging.WARNING)
                        l_log.warning("<E01: mensagem não reconhecida ou não tratável.")

            # em caso de não haver mensagens...
            except Queue.Empty:
                # salva o tempo anterior
                lf_ant = lf_now

                # tempo atual em segundos
                lf_now = time.time()

                # calcula o tempo decorrido
                lf_dif = lf_now - lf_ant

                # está adiantado ?
                if lf_tim_rrbn > lf_dif:
                    # permite o scheduler
                    time.sleep((lf_tim_rrbn - lf_dif) * .99)

                # senão, atrasou...
                else:
                    # logger
                    l_log = logging.getLogger("CControlNewton::run")
                    l_log.setLevel(logging.WARNING)
                    l_log.warning("<E02: atrasou: {}.".format(lf_dif - lf_tim_rrbn))

            # em caso de não haver mensagens...
            except Exception, l_err:
                # logger
                l_log = logging.getLogger("CControlNewton::run")
                l_log.setLevel(logging.WARNING)
                l_log.warning("<E03: control error: {}.".format(l_err))

        # self.sim_stat.noProcFlights = fe.flightsProcessed
        # self.sim_stat.printScore()

    # ---------------------------------------------------------------------------------------------
    def start_time(self):
        """
        start time
        """
        # clear to go
        assert self.model
        assert self.sim_time

        # exercício
        l_exe = self.model.exe
        assert l_exe

        # hora de início do exercício
        lt_hora = l_exe.t_exe_hor_ini

        # inicia o relógio da simulação
        self.sim_time.set_hora(lt_hora)

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def emula(self):
        return self.__emula

    @emula.setter
    def emula(self, f_val):
        self.__emula = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def mpi_comm(self):
        return self.__mpi_comm

    # ---------------------------------------------------------------------------------------------
    @property
    def mpi_rank(self):
        return 0 if self.__mpi_comm is None else self.__mpi_comm.rank

    # ---------------------------------------------------------------------------------------------
    @property
    def mpi_size(self):
        return 1 if self.__mpi_comm is None else self.__mpi_comm.size

    # ---------------------------------------------------------------------------------------------
    @property
    def q_rcv_cpil(self):
        return self.__q_rcv_cpil

    @q_rcv_cpil.setter
    def q_rcv_cpil(self, f_val):
        self.__q_rcv_cpil = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_rcv_cpil(self):
        return self.__sck_rcv_cpil

    @sck_rcv_cpil.setter
    def sck_rcv_cpil(self, f_val):
        self.__sck_rcv_cpil = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def q_rcv_cnfg(self):
        return self.__q_rcv_cnfg

    @q_rcv_cnfg.setter
    def q_rcv_cnfg(self, f_val):
        self.__q_rcv_cnfg = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_rcv_cnfg(self):
        return self.__sck_rcv_cnfg

    @sck_rcv_cnfg.setter
    def sck_rcv_cnfg(self, f_val):
        self.__sck_rcv_cnfg = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def q_snd_cnfg(self):
        return self.__q_snd_cnfg

    @q_snd_cnfg.setter
    def q_snd_cnfg(self, f_val):
        self.__q_snd_cnfg = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_snd_cnfg(self):
        return self.__sck_snd_cnfg

    @sck_snd_cnfg.setter
    def sck_snd_cnfg(self, f_val):
        self.__sck_snd_cnfg = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def q_snd_trks(self):
        return self.__q_snd_trks

    @q_snd_trks.setter
    def q_snd_trks(self, f_val):
        self.__q_snd_trks = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_snd_trks(self):
        return self.__sck_snd_trks

    @sck_snd_trks.setter
    def sck_snd_trks(self, f_val):
        self.__sck_snd_trks = f_val

# < the end >--------------------------------------------------------------------------------------
