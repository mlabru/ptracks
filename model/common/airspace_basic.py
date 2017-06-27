#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
airspace_basic

basic model manager
load from one configuration file all configured tables

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
inclusão do event manager e config manager

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.3$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import os

# model
import model.items.aer_data as aerdata
import model.items.fix_data as fixdata

# < class CAirspaceBasic >-------------------------------------------------------------------------

class CAirspaceBasic(object):
    """
    basic airspace model manager
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_model):
        """
        @param f_model: model manager
        """
        # check input
        assert f_model

        # init super class
        super(CAirspaceBasic, self).__init__()

        # model manager
        self.__model = f_model

        # event manager
        self.__event = f_model.event

        # registra-se como recebedor de eventos
        self.__event.register_listener(self)

        # config manager
        self.__config = f_model.config

        # inicia dicionários
        self.__dct_aer = {}
        self.__lst_arr_dep = []
        self.__dct_fix = {}

        # carrega as tabelas de dados nos dicionários
        self.__load_dicts()
        
    # ---------------------------------------------------------------------------------------------
    def __load_dicts(self):
        """
        carrega os dicionários
        """
        # monta o nome da tabela de fixos
        ls_path = os.path.join(self.dct_config["dir.tab"], self.dct_config["tab.fix"])

        # carrega a tabela de fixos em um dicionário
        self.dct_fix = fixdata.CFixData(self.model, ls_path)
        assert self.dct_fix is not None

        # monta o nome da tabela de waypoints
        ls_path = os.path.join(self.dct_config["dir.tab"], self.dct_config["tab.wpt"])

        # carrega a tabela de waypoints em um dicionário
        ldct_wpt = fixdata.CFixData(self.model, ls_path)
        assert ldct_wpt is not None

        # coloca os waypoints no dicionário de fixos
        self.dct_fix.update(ldct_wpt) 

        # salva referência da tabela de fixos no sistema de coordenadas
        self.model.coords.dct_fix = self.dct_fix

        # monta o nome da tabela de aeródromos
        ls_path = os.path.join(self.dct_config["dir.tab"], self.dct_config["tab.aer"])

        # carrega a tabela de aeródromos em um dicionário
        self.dct_aer = aerdata.CAerData(self.model, ls_path)

        # monta a lista de pousos/decolagens

        # para todos os aeródromos...
        for l_aer, l_aer_data in self.dct_aer.iteritems():
            # para todas as pistas...
            for l_pst in l_aer_data.dct_aer_pistas:                
                # salva a tupla (aeródromo, pista)
                self.__lst_arr_dep.append("{}/{}".format(l_aer, l_pst))

    # ---------------------------------------------------------------------------------------------
    def get_aer_pst(self, fs_aer, fs_pst):
        """
        obtém o pointer para o aeródromo e pista

        @param fs_aer: indicativo do aeródromo
        @param fs_pst: indicativo da pista

        @return pointer para o aeródromo e pista
        """
        # obtém o aeródromo
        l_aer = self.__dct_aer.get(fs_aer, None)

        if l_aer is None:
            # logger
            l_log = logging.getLogger("CAirspaceBasic::get_aer_pst")
            l_log.setLevel(logging.ERROR)
            l_log.error(u"<E01: não existe aeródromo [{}].".format(fs_aer))

            # retorna pointers
            return None, None

        # obtém a pista
        l_pst = l_aer.dct_aer_pistas.get(fs_pst, None)

        if l_pst is None:
            # logger
            l_log = logging.getLogger("CAirspaceBasic::get_aer_pst")
            l_log.setLevel(logging.ERROR)
            l_log.error(u"<E02: não existe pista [{}] no aeródromo [{}].".format(fs_pst, fs_aer))

            # retorna pointers
            return l_aer, None

        # retorna pointers
        return l_aer, l_pst

    # ---------------------------------------------------------------------------------------------
    def notify(self, f_event):
        """
        callback de tratamento de eventos recebidos

        @param f_event: evento recebido
        """
        # return
        return
        
    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_aer(self):
        """
        get aeródromos
        """
        return self.__dct_aer

    @dct_aer.setter
    def dct_aer(self, f_val):
        """
        set aeródromos
        """
        self.__dct_aer = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def lst_arr_dep(self):
        """
        get pousos/decolagens
        """
        return self.__lst_arr_dep

    @lst_arr_dep.setter
    def lst_arr_dep(self, f_val):
        """
        set pousos/decolagens
        """
        self.__lst_arr_dep = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def config(self):
        """
        get config manager
        """
        return self.__config

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_config(self):
        """
        get configuration dictionary
        """
        return self.__config.dct_config if self.__config is not None else {}

    # ---------------------------------------------------------------------------------------------
    @property
    def event(self):
        """
        get event manager
        """
        return self.__event

    @event.setter
    def event(self, f_val):
        """
        get event manager
        """
        self.__event = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_fix(self):
        """
        get fixos
        """
        return self.__dct_fix

    @dct_fix.setter
    def dct_fix(self, f_val):
        """
        set fixos
        """
        self.__dct_fix = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def model(self):
        """
        get model manager
        """
        return self.__model

# < the end >--------------------------------------------------------------------------------------
