#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
emula_visil

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

revision 0.1  2015/fev  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/12"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import sys
import threading
import time

# model
import model.common.glb_data as gdata
import model.emula.emula_model as model
import model.visil.aircraft_visil as canv

# control
import control.common.glb_defs as gdefs
import control.events.events_flight as events

# < class CEmulaVisil >----------------------------------------------------------------------------

class CEmulaVisil (model.CEmulaModel):
    """
    the flight model class generates new flights and handles their movement. It has a list of
    flight objects holding all flights that are currently active. The flights are generated when
    activation time comes, or quando ja foi ativado na confecção do exercicio. Once a flight has
    been generated it is handed by the flight engine
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_model, f_control):
        """
        initializes the app and prepares everything

        @param f_model: model manager
        @param f_control: control manager
        """
        # check input
        assert f_control

        # inicia a super classe
        super(CEmulaVisil, self).__init__(f_model, f_control)

        # herdados de CEmulaModel
        # self.config        # config manager
        # self.dct_config    # dicionário de configuração
        # self.control       # control manager
        # self.event         # event manager
        # self.dct_flight    # dictionary for all active flights
        # self.model         # model manager

        # queue de dados
        self.__q_rcv_trks = f_control.q_rcv_trks
        assert self.__q_rcv_trks

        # data listener
        self.__sck_rcv_trks = f_control.sck_rcv_trks
        assert self.__sck_rcv_trks

        # cria a trava da lista de vôos
        gdata.G_LCK_FLIGHT = threading.Lock()
        assert gdata.G_LCK_FLIGHT

    # ---------------------------------------------------------------------------------------------
    def run(self):
        """
        checks whether it's time to created another flight
        """
        # check de colisão
        lf_tim_evnt = self.dct_config["tim.evnt"]

        # enquanto não inicia...
        while not gdata.G_KEEP_RUN:
            # aguarda 1 seg
            time.sleep(1)

        # inicia o recebimento de mensagens de dados
        self.__sck_rcv_trks.start()

        # loop
        while gdata.G_KEEP_RUN:
            # tempo inicial em segundos
            ll_now = time.time()

            # item da queue de entrada
            llst_data = self.__q_rcv_trks.get()
            # cdbg.M_DBG.debug("llst_data: (%s)" % str(llst_data))

            # queue tem dados ?
            if llst_data:
                # mensagem de status de aeronave ?
                if gdefs.D_MSG_NEW == int(llst_data[0]):
                    # callsign
                    ls_callsign = llst_data[10]
                    # cdbg.M_DBG.debug("run:callsign:[{}]".format(llst_data[10]))

                    # trava a lista de vôos
                    gdata.G_LCK_FLIGHT.acquire()

                    try:
                        # aeronave já está no dicionário ?
                        if ls_callsign in self.dct_flight:
                            # atualiza os dados da aeronave
                            self.dct_flight[ls_callsign].update_data(llst_data[1:])

                        # senão, aeronave nova...
                        else:
                            # create new aircraft
                            self.dct_flight[ls_callsign] = canv.CAircraftVisil(self, llst_data[1:])
                            assert self.dct_flight[ls_callsign]

                    finally:
                        # libera a lista de vôos
                        gdata.G_LCK_FLIGHT.release()

                    # cria um evento de atualização de aeronave
                    l_evt = events.CFlightUpdate(ls_callsign)
                    assert (l_evt)

                    # dissemina o evento
                    self.event.post(l_evt)

                # mensagem de eliminação de aeronave ?
                # elif gdefs.D_MSG_KLL == int(llst_data[0]):
                    '''
                    # coloca a mensagem na queue
                    # cdbg.M_DBG.debug("Elimina: (%s)" % str(ls_callsign))

                    # trava a lista de vôos
                    gdata.G_LCK_FLIGHT.acquire()

                    try:
                        # aeronave está no dicionário ?
                        if ls_callsign in self.dctFlight:
                            # retira a aeronave do dicionário
                            del self.dctFlight[ls_callsign]

                    finally:
                        # libera a lista de vôos
                        gdata.G_LCK_FLIGHT.release()

                    # cria um evento de eliminação de aeronave
                    l_evt = events.CFlightKill(ls_callsign)
                    assert l_evt
                    # cdbg.M_DBG.debug("l_evt: " + str(l_evt))

                    # dissemina o evento
                    self.event.post(l_evt)'''

                # senão, mensagem não reconhecida ou não tratada
                else:
                    # logger
                    l_log = logging.getLogger("CEmulaVisil::run")
                    l_log.setLevel(logging.WARNING)
                    l_log.warning("<E01: mensagem não reconhecida ou não tratada.")

            # tempo final em segundos e calcula o tempo decorrido
            ll_dif = time.time() - ll_now

            # esta adiantado ?
            if lf_tim_evnt > ll_dif:
                # permite o scheduler (1/10th)
                time.sleep(lf_tim_evnt - ll_dif)

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_rcv_trks(self):
        """
        get data listener
        """
        return self.__sck_rcv_trks

# < the end >--------------------------------------------------------------------------------------
