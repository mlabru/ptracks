#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
config_super

configuração do supervisor

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

revision 0.2  2017/jan  mlabru
pep8 style conventions

revision 0.1  2016/dez  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/01"

# < import >---------------------------------------------------------------------------------------

# python library
import argparse
import os
import sys

# model 
import model.common.data as data

# control
import control.common.glb_defs as gdefs
import control.config.config_manager as config

# < class CConfigSuper >---------------------------------------------------------------------------

class CConfigSuper(config.CConfigManager):
    """
    mantém as informações de configuração
    """
    # informações comuns de configuração
    __CFG_SUPER = {"spr.acc": 1.,
                   "spr.freeze": False,
                   "spr.gui": False,
                   "spr.stop": True,
                   "spr.type": None, 
                   "spr.unfreeze": True
    }  # __CFG_SUPER

    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_config):
        """
        inicia o gerente de configuração

        @param fs_config: full path do arquivo de configuração
        """
        # init super class
        super(CConfigSuper, self).__init__(fs_config)

        # herdados de CConfigManager
        # self.dct_config    # config manager data dictionary

        # carrega os atributos locais no dicionário de configuração
        for l_key in self.__CFG_SUPER.keys():
            if l_key not in self.dct_config:
                self.dct_config[l_key] = self.__CFG_SUPER[l_key]

        # cria um parser para os argumentos
        l_parser = argparse.ArgumentParser(description="super (C) 2014-2017.")
        assert l_parser

        # # argumento: version
        l_parser.add_argument("-v", "--version", action="version", version=__version__)

        # create newton subparsers
        l_subparsers = l_parser.add_subparsers(title="newton commands", description="valid newton subcommands", help="subcommands help")
        assert l_subparsers 
      
        # argumento: canal de comunicação
        l_parser.add_argument("canal", type=int, default=self.dct_config["glb.canal"], help="communication channel")

        # argumento: congela o exercício
        l_freeze_parser = l_subparsers.add_parser("freeze", help="freeze simulation")  # aliases=["frz"], 
        l_freeze_parser.set_defaults(func=self.__cbk_freeze)

        # argumento: interativo
        l_gui_parser = l_subparsers.add_parser("gui")
        l_gui_parser.set_defaults(func=self.__cbk_gui)

        # argumento: velocidade de execução
        l_speed_parser = l_subparsers.add_parser("fts", help="fast-track simulation")
        l_speed_parser.add_argument("-s", "--speed", default=self.dct_config["tim.accl"], type=float, help="simulation speed")
        l_speed_parser.set_defaults(func=self.__cbk_speed)

        # argumento: termina o simulador
        l_stop_parser = l_subparsers.add_parser("stop", help="stop simulation")  # aliases=["stp"],
        l_stop_parser.set_defaults(func=self.__cbk_stop)

        # argumento: descongela o exercício
        l_unfreeze_parser = l_subparsers.add_parser("unfreeze", help="unfreeze simulation")  # aliases=["ufz"], 
        l_unfreeze_parser.set_defaults(func=self.__cbk_unfreeze)

        # faz o parser da linha de argumentos
        l_args = l_parser.parse_args()
        assert l_args

        # salva os argumentos no dicionário
        l_args.func(l_args)

        # salva os argumentos no dicionário
        self.dct_config["glb.canal"] = abs(int(l_args.canal))

        # load dirs section
        self.load_dirs()

    # ---------------------------------------------------------------------------------------------
    def __cbk_freeze(self, f_args):
        self.dct_config["spr.freeze"] = True
        self.dct_config["spr.type"] = gdefs.D_MSG_FRZ

    def __cbk_gui(self, f_args):
        self.dct_config["spr.gui"] = True
        self.dct_config["spr.type"] = None

    def __cbk_speed(self, f_args):
        self.dct_config["spr.acc"] = f_args.speed
        self.dct_config["spr.type"] = gdefs.D_MSG_ACC

    def __cbk_stop(self, f_args):
        self.dct_config["spr.stop"] = True
        self.dct_config["spr.type"] = gdefs.D_MSG_FIM

    def __cbk_unfreeze(self, f_args):
        self.dct_config["spr.unfreeze"] = True
        self.dct_config["spr.type"] = gdefs.D_MSG_UFZ

# < the end >--------------------------------------------------------------------------------------
