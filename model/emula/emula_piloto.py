#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
emula_piloto

the actual flight control

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
import json
import logging
import threading
import time

# model
import model.common.glb_data as gdata
import model.emula.emula_model as model
import model.visil.aircraft_visil as canv

# control
import control.common.glb_defs as gdefs
import control.events.events_flight as events

# < class CEmulaPiloto >---------------------------------------------------------------------------

class CEmulaPiloto(model.CEmulaModel):
    """
    the flight model class generates new flights and handles their movement. It has a list of
    flight objects holding all flights that are currently active. The flights are generated when
    activation time comes, or quando ja foi ativado na confecção do exercicio. Once a flight has
    been generated it is handed by the flight engine
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_model, f_control):
        """
        @param f_model: model manager
        @param f_control: control manager
        """
        # check input
        assert f_control
        assert f_model

        # inicia a super classe
        super(CEmulaPiloto, self).__init__(f_model, f_control)

        # herdados de CFlightModel
        # self.config        # config manager
        # self.dct_config    # dicionário de configuração
        # self.control       # control manager
        # self.event         # event manager
        # self.dct_flight    # dictionary for active flights
        # self.model         # model manager

        # queue de dados
        self.__q_rcv_trks = f_control.q_rcv_trks
        assert self.__q_rcv_trks

        # data listener
        self.__sck_rcv_trks = f_control.sck_rcv_trks
        assert self.__sck_rcv_trks

        # http server listener
        self.__sck_http = f_control.sck_http
        assert self.__sck_http

        # relógio da simulação
        self.__sim_time = f_control.sim_time
        assert self.__sim_time

        # dicionário de performances
        self.__dct_prf = f_model.dct_prf
        assert self.__dct_prf is not None

        # cria a trava da lista de vôos
        gdata.G_LCK_FLIGHT = threading.Lock()
        assert gdata.G_LCK_FLIGHT
                        
    # ---------------------------------------------------------------------------------------------
    def __msg_trk(self, flst_data):
        """
        checks whether it's time to created another flight

        @param flst_data: mensagem de status
        """
        # clear to go
        assert self.__sck_http is not None
        assert self.dct_config is not None
        assert self.dct_flight is not None
        assert self.__dct_prf is not None
                
        # callsign da aeronave
        ls_callsign = flst_data[10]
                            
        # trava a lista de vôos
        gdata.G_LCK_FLIGHT.acquire()

        try:
            # aeronave já está no dicionário ?
            if ls_callsign in self.dct_flight:
                # atualiza os dados da aeronave
                self.dct_flight[ls_callsign].update_data(flst_data[1:])

            # senão, aeronave nova...
            else:
                # create new aircraft
                self.dct_flight[ls_callsign] = canv.CAircraftVisil(self, flst_data[1:])
                assert self.dct_flight[ls_callsign]
                                                                                                                                                                                                                                                            
        finally:
            # libera a lista de vôos
            gdata.G_LCK_FLIGHT.release()

        # indicativo da performance
        ls_prf_ind = flst_data[11]
                            
        # performance não está no dicionário ?
        if self.__dct_prf.get(ls_prf_ind, None) is None:
            # monta o request da performance
            ls_req = "data/prf.json?{}".format(ls_prf_ind)

            # get server address
            l_srv = self.dct_config.get("srv.addr", None)
            
            if l_srv is not None:
                # dados de performance do servidor
                l_prf = self.__sck_http.get_data(l_srv, ls_req)

                if (l_prf is not None) and (l_prf != ""):
                    # salva a performance no dicionário
                    self.__dct_prf[ls_prf_ind] = json.loads(l_prf)

                # senão, não achou no servidor...
                else:
                    # logger
                    l_log = logging.getLogger("CEmulaPiloto::__msg_trk")
                    l_log.setLevel(logging.WARNING)
                    l_log.error(u"<E01: performance({}) não existe no servidor.".format(ls_prf_ind))

            # senão, não achou endereço do servidor
            else:
                # logger
                l_log = logging.getLogger("CEmulaPiloto::__msg_trk")
                l_log.setLevel(logging.WARNING)
                l_log.warning(u"<E02: srv.addr não existe na configuração.")

        # cria um evento de atualização de aeronave
        l_evt = events.CFlightUpdate(ls_callsign)
        assert l_evt

        # dissemina o evento
        self.event.post(l_evt)

    # ---------------------------------------------------------------------------------------------
    def run(self):
        """
        checks whether it's time to created another flight
        """
        # check de colisão
        lf_tim_rrbn = float(self.dct_config["tim.rrbn"])

        # enquanto não inicia...
        while not gdata.G_KEEP_RUN:
            # aguarda 1 seg
            time.sleep(1)

        # inicia o recebimento de mensagens de pista
        self.__sck_rcv_trks.start()

        # tempo inicial em segundos
        lf_now = time.time()

        # loop
        while gdata.G_KEEP_RUN:
            # item da queue de entrada
            llst_data = self.__q_rcv_trks.get()

            # queue tem dados ?
            if llst_data:
                # mensagem de status de aeronave ?
                if gdefs.D_MSG_NEW == int(llst_data[0]):
                    # trata mensagem de status de aeronave
                    self.__msg_trk(llst_data)
                    
                # mensagem de eliminação de aeronave ?
                elif gdefs.D_MSG_Kll == int(llst_data[0]):
                    # coloca a mensagem na queue

                    # trava a lista de vôos
                    gdata.G_LCK_FLIGHT.acquire()

                    try:
                        # aeronave está no dicionário ?
                        if ls_callsign in self.dct_flight:
                            # retira a aeronave do dicionário
                            del self.dct_flight[ls_callsign]

                    finally:
                        # libera a lista de vôos
                        gdata.G_LCK_FLIGHT.release()

                    # cria um evento de eliminação de aeronave
                    l_evt = events.FlightKill(ls_callsign)
                    assert l_evt

                    # dissemina o evento
                    self._event.post(l_evt)

                # senão, mensagem não reconhecida ou não tratada
                else:
                    # logger
                    l_log = logging.getLogger("CEmulaPiloto::run")
                    l_log.setLevel(logging.WARNING)
                    l_log.warning("<E01: mensagem não reconhecida ou não tratada.")

            # salva o tempo anterior
            lf_ant = lf_now

            # tempo atual em segundos
            lf_now = time.time()
                                    
            # tempo final em segundos e calcula o tempo decorrido
            lf_dif = lf_now - lf_ant
                                                                            
            # está adiantado ?
            if lf_tim_rrbn > lf_dif:
                # permite o scheduler
                time.sleep(lf_tim_rrbn - lf_dif)

    # =============================================================================================
    # data
    # =============================================================================================
            
    # ---------------------------------------------------------------------------------------------
    @property
    def sck_rcv_trks(self):
        """
        data listener
        """
        return self.__sck_rcv_trks

# < the end >--------------------------------------------------------------------------------------
