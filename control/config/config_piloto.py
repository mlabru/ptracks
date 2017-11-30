#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
config_piloto

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
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2016/03"

# < import >---------------------------------------------------------------------------------------

# python library
import argparse
import os

# model 
import model.common.data as data

# control
# import control.control_debug as dbg
import control.config.config_manager as config

# < class CConfigPiloto >--------------------------------------------------------------------------

class CConfigPiloto(config.CConfigManager):
    """
    mantém as informações de configuração
    """
    # informações comuns de configuração
    __CFG_PILOTO = {}  # __CFG_PILOTO

    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_config):
        """
        inicia o gerente de configuração

        @param fs_config: full path do arquivo de configuração
        """
        # init super class
        super(CConfigPiloto, self).__init__(fs_config)

        # herdados de CConfigManager
        # self.dct_config    # config manager data dictionary

        # carrega os atributos locais no dicionário de configuração
        for l_key in self.__CFG_PILOTO.keys():
            if l_key not in self.dct_config:
                self.dct_config[l_key] = self.__CFG_PILOTO[l_key]

        # cria um parser para os argumentos
        l_parser = argparse.ArgumentParser(description="Piloto (C) 2014-2016.")
        assert l_parser

        # argumento: canal de comunicação
        l_parser.add_argument("-c", "--canal",
                              dest="canal",
                              default=self.dct_config["glb.canal"],
                              help=u"Canal de comunicação (default: {})".format(self.dct_config["glb.canal"]))

        # faz o parser da linha de argumentos
        l_args = l_parser.parse_args()
        assert l_args

        # salva os argumentos no dicionário
        self.dct_config["glb.canal"] = int(l_args.canal)

        # load dirs section
        self.load_dirs()

# < the end >--------------------------------------------------------------------------------------
