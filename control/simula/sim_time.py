#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
sim_time

simulation time engine

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

revision 0.3  2015/nov  mlabru
pep8 style conventions

revision 0.2  2014/nov  mlabru
inclusão do dicionário de configuração

revision 0.1  2014/nov  mlabru
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.3$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import threading
import time

# model 
import model.common.glb_data as gdata

# control
# import control.control_debug as dbg
import control.common.glb_defs as gdefs
import control.events.events_basic as events

# < class CSimTime >-------------------------------------------------------------------------------

class CSimTime(threading.Thread):
    """
    simulation time engine
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control):
        """
        cria o relógio da simulação
        """
        # check input
        assert f_control

        # init super class
        super(CSimTime, self).__init__()

        # obtém o events manager
        self.__event = f_control.event
        assert self.__event

        # obtém o config manager
        l_config = f_control.config
        assert l_config

        # obtém o dicionário de configuração
        self.__dct_config = l_config.dct_config
        assert self.__dct_config is not None

        # flag congela
        self.__v_congela = False

        # hora zero da simulação
        self.__f_zero_sim = 0.

        # preenche a hora zero do sistema (seg)
        self.__f_zero_sys = time.time()

        # hora atual do exercício
        self.__b_ha = 0
        self.__b_ma = 0
        self.__b_sa = 0

        # hora atual formatada
        self.__s_hora = "{:02d}:{:02d}:{:02d}".format(self.__b_ha, self.__b_ma, self.__b_sa)

        # hora atual do exercício
        self.__f_hora_atu = 0

        # tempo de congelamento do exercício
        self.__f_hora_frz = 0

    # ---------------------------------------------------------------------------------------------
    def ajusta_hora(self, f_hora):
        """
        permite configurar a hora do equipamento

        @param f_hora: hora (seg)
        """
        # check input
        assert f_hora

        # preenche a hora zero da simulação (seg)
        self.__f_zero_sim = f_hora

        # preenche a hora zero do sistema (seg)
        self.__f_zero_sys = time.time()

    # ---------------------------------------------------------------------------------------------
    def cbk_congela(self):
        """
        congela o relógio da simulação
        """
        # flag congela
        self.__v_congela = True

        # obtém a hora do sistema (seg)
        self.__f_hora_frz = time.time()

    # ---------------------------------------------------------------------------------------------
    def cbk_descongela(self):
        """
        descongela o relógio da simulação
        """
        # obtem a hora do sistema (seg)
        lf_hora_now = time.time()

        # calcula quanto tempo ficou congelado
        lf_hora_dif = lf_hora_now - self.__f_hora_frz

        # incrementa ao tempo zero do sistema (seg)
        self.__f_zero_sys += lf_hora_dif

        # flag congela
        self.__v_congela = False

    # ---------------------------------------------------------------------------------------------
    def get_hora_format(self):
        """
        exibe o relógio da simulação
        """
        # obtem a hora atual do exercício
        lb_h, lb_m, lb_s, _ = self.obtem_hora()

        # checa se mudou algo
        if (lb_h != self.__b_ha) or (lb_m != self.__b_ma) or (lb_s != self.__b_sa):
            # monta a string com a hora atual
            self.__s_hora = "{:02d}:{:02d}:{:02d}".format(lb_h, lb_m, lb_s)

            # salva os valores atuais
            self.__b_ha = lb_h
            self.__b_ma = lb_m
            self.__b_sa = lb_s

        # retorna a hora da simulação formatada
        return self.__s_hora

    # ---------------------------------------------------------------------------------------------
    @staticmethod
    def notify(f_event):
        """
        callback de tratamento de eventos recebidos

        @param f_event: event
        """
        # check input
        assert f_event

    # ---------------------------------------------------------------------------------------------
    def obtem_hora(self):
        """
        obtém a hora do relógio do equipamento
        """
        # obtém a hora da simulação
        lf_hora_now = self.obtem_hora_sim()

        # calcula os milésimos de segundo
        li_msg = int(round((lf_hora_now - int(lf_hora_now)) * 1000.))

        # calcula os segundos
        li_seg = int(lf_hora_now) % 60

        # calcula os minutos
        li_min = int(lf_hora_now / 60.) % 60

        # calcula as horas
        li_hor = int(lf_hora_now / 3600.)

        # return
        return li_hor, li_min, li_seg, li_msg

    # ---------------------------------------------------------------------------------------------
    def obtem_hora_sim(self):
        """
        obtém a hora da simulação

        @return hora atual do sistema em seg
        """
        # sistema descongelado ?
        if not self.__v_congela:
            # obtém a hora do sistema (seg)
            self.__f_hora_atu = time.time()

        # calcula a diferença com a hora zero
        lf_hora_dif = self.__f_hora_atu - self.__f_zero_sys

        # incrementa a hora zero da simulação e retorna
        return self.__f_zero_sim + (lf_hora_dif * float(self.__dct_config["tim.accl"]))

    # ---------------------------------------------------------------------------------------------
    def run(self):
        """
        executa o relógio da simulação
        """
        # enquanto não inicia...
        while not gdata.G_KEEP_RUN:
            # aguarda 1 seg
            time.sleep(1)

        # loop do relógio...
        while gdata.G_KEEP_RUN:
            # cria um evento de tick do clock
            l_evt_tick = events.CTick()
            assert l_evt_tick

            # dissemina o evento
            self.__event.post(l_evt_tick)

    # ---------------------------------------------------------------------------------------------
    def send_hora(self, f_sck_scfg):
        """
        envia a hora de simulação

        @param f_sck_scfg: net sender
        """
        # check input
        assert f_sck_scfg

        # envia a hora de simulação pela linha de configuração
        f_sck_scfg.send_data(str(gdefs.D_MSG_VRS) + gdefs.D_MSG_SEP +
                             str(gdefs.D_MSG_TIM) + gdefs.D_MSG_SEP + str(self.obtem_hora()))

    # ---------------------------------------------------------------------------------------------
    def set_hora(self, ft_hora):
        """
        configura a hora de simulação

        @param ft_hora: tupla no formato(hor, min, seg, csg)
        """
        # check input
        assert ft_hora

        assert 0 <= ft_hora[0] <= 23  # hora
        assert 0 <= ft_hora[1] <= 59  # minutos
        assert 0 <= ft_hora[2] <= 59  # segundos

        # preenche a hora zero da simulação (seg)
        self.__f_zero_sim = (((ft_hora[0] * 60) + ft_hora[1]) * 60) + ft_hora[2]

        # preenche a hora zero do sistema (seg) em relação a simulação
        self.__f_zero_sys = time.time()

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def v_congela(self):
        return self.__v_congela

    @v_congela.setter
    def v_congela(self, fv_val):

        # check input
        assert isinstance(True, type(fv_val))

        # flag congela
        self.__v_congela = fv_val

# < the end >--------------------------------------------------------------------------------------
