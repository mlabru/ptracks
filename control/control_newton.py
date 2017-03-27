#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
control_newton

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
    DOCUMENT ME!
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
        self.__sck_rcv_cnfg.daemon = True

        # cria a queue de recebimento de comandos de pilotagem
        self.__q_rcv_cpil = multiprocessing.Queue()
        assert self.__q_rcv_cpil

        # endereço de recebimento
        lt_ifce, ls_addr, li_port = gaddr.get_address(self.config, "net.cpil")

        # cria o socket de recebimento de comandos de pilotagem
        self.__sck_rcv_cpil = listener.CNetListener(lt_ifce, ls_addr, li_port, self.__q_rcv_cpil)
        assert self.__sck_rcv_cpil

        # set as daemon
        self.__sck_rcv_cpil.daemon = True

        # create application
        # self.__create_app()

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
    def __create_app(self):
        """
        DOCUMENT ME!
        """
        # create application
        # self.app = QtCore.QCoreApplication(sys.argv)
        # assert self.app

        # setup application parameters
        # self.app.setOrganizationName("sophosoft")
        # self.app.setOrganizationDomain("sophosoft.com.br")
        # self.app.setApplicationName("newton")

        # self.app.setWindowIcon(QtGui.QIcon(os.path.join(self.__dct_config["dir.img"], "icon_app.png")))

        # load logo
        # l_pix_logo = QtGui.QPixmap(os.path.join(self.__dct_config["dir.img"], "logo_python.png"))
        # assert l_pix_logo

        # create splash screen
        # self.splash = QtGui.QSplashScreen(l_pix_logo, QtCore.Qt.WindowStaysOnTopHint)
        # assert self.splash

        # self.splash.setMask(l_pix_logo.mask())

        # create the progress bar
        # self.progressBar = QtGui.QProgressBar(self.splash)
        # self.progressBar.setGeometry(    self.splash.width() / 10, 8 * self.splash.height() / 10,
        #                              8 * self.splash.width() / 10,     self.splash.height() / 10)

        # message = 'hello'
        # label = QtGui.QLabel("<font color=red size=72><b>{0}</b></font>".format(message), self.splash)
        # label.setGeometry(1 * self.splash.width() / 10, 8 * self.splash.height() / 10,
        #                   8 * self.splash.width() / 10, 1 * self.splash.height() / 10)

        # show splash screen
        # self.splash.show()

        # update the progress bar
        # self.progressBar.setValue(50)

        # process events (before main loop)
        # self.app.processEvents()

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

        # ativa o relógio da simulação
        self.start_time()

        # inicia o recebimento de mensagens de comando/controle/configuração(ccc)
        self.__sck_rcv_cnfg.start()

        # starts flight model
        self.__emula.start()

        # starts web server
        self.view.start()

        # keep things running
        gdata.G_KEEP_RUN = True

        # tempo inicial em segundos
        lf_now = time.time()

        # application loop
        while gdata.G_KEEP_RUN:
            try:
                # obtém um item da queue de mensagens de comando/controle/configuração (nowait)
                llst_data = self.__q_rcv_cnfg.get(False)

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

        # self.sim_stat.noProcFlights = fe.flightsProcessed
        # self.sim_stat.printScore()

    # ---------------------------------------------------------------------------------------------
    def start_time(self):
        """
        DOCUMENT ME!
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
        """
        get flight emulation model
        """
        return self.__emula

    @emula.setter
    def emula(self, f_val):
        """
        set flight emulation model
        """
        self.__emula = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def mpi_comm(self):
        """
        get MPI Comm
        """
        return self.__mpi_comm

    # ---------------------------------------------------------------------------------------------
    @property
    def mpi_rank(self):
        """
        get MPI rank
        """
        return 0 if self.__mpi_comm is None else self.__mpi_comm.rank

    # ---------------------------------------------------------------------------------------------
    @property
    def mpi_size(self):
        """
        get MPI size
        """
        return 1 if self.__mpi_comm is None else self.__mpi_comm.size

    # ---------------------------------------------------------------------------------------------
    @property
    def q_rcv_cpil(self):
        """
        get pilot commands queue
        """
        return self.__q_rcv_cpil

    @q_rcv_cpil.setter
    def q_rcv_cpil(self, f_val):
        """
        set pilot commands queue
        """
        self.__q_rcv_cpil = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_rcv_cpil(self):
        """
        get pilot commands listener
        """
        return self.__sck_rcv_cpil

    @sck_rcv_cpil.setter
    def sck_rcv_cpil(self, f_val):
        """
        set pilot commands listener
        """
        self.__sck_rcv_cpil = f_val

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
    def q_snd_cnfg(self):
        """
        get configuration queue
        """
        return self.__q_snd_cnfg

    @q_snd_cnfg.setter
    def q_snd_cnfg(self, f_val):
        """
        set configuration queue
        """
        self.__q_snd_cnfg = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_snd_cnfg(self):
        """
        get configuration sender
        """
        return self.__sck_snd_cnfg

    @sck_snd_cnfg.setter
    def sck_snd_cnfg(self, f_val):
        """
        set configuration sender
        """
        self.__sck_snd_cnfg = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def q_snd_trks(self):
        """
        get tracks queue
        """
        return self.__q_snd_trks

    @q_snd_trks.setter
    def q_snd_trks(self, f_val):
        """
        set tracks queue
        """
        self.__q_snd_trks = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_snd_trks(self):
        """
        get tracks sender
        """
        return self.__sck_snd_trks

    @sck_snd_trks.setter
    def sck_snd_trks(self, f_val):
        """
        set tracks sender
        """
        self.__sck_snd_trks = f_val

# < the end >--------------------------------------------------------------------------------------
