#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
model_super

supervisor model

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

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import os
import sys

# model
import model.model_manager as model

import model.items.exe_data as exedata

# control
import control.events.events_basic as events

# < class CModelSuper >----------------------------------------------------------------------------

class CModelSuper(model.CModelManager):
    """
    modelo do super
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control):
        """
        @param f_control: control manager
        """
        # check input
        assert f_control

        # init super class
        super(CModelSuper, self).__init__(f_control)

        # herdados de CModelManager
        # self.control       # control manager
        # self.event         # event manager
        # self.config        # config manager
        # self.dct_config    # dicionário de configuração

        # variáveis de instância
        self.__dct_exe = {}

        # carrega as tabelas do sistema
        lv_ok = self.__load_tables()

        # houve erro em alguma fase ?
        if not lv_ok:
            # logger
            l_log = logging.getLogger("CModelSuper::__init__")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: erro na carga da base de dados.")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.event.post(l_evt)

            # termina a aplicação
            sys.exit(1)

    # ---------------------------------------------------------------------------------------------
    def __load_tables(self):
        """
        abre/cria as tabelas do sistema

        @return flag e mensagem
        """
        # carrega a tabela de exercícios
        lv_ok = self.load_table_exe()

        if lv_ok:
            # carrega a tabela de tráfegos
            # lv_ok = self.load_table_anv()
            pass

        # return
        return True

    # ---------------------------------------------------------------------------------------------
    def load_table_exe(self):
        """
        faz a carga da tabela de exercícios
        """
        # obtém o diretório padrão de exercícios
        ls_dir = self.dct_config["dir.exe"]

        # nome do diretório vazio ?
        if ls_dir is None:
            # diretório padrão de exercícios
            ls_dir = self.dct_config["dir.exe"] = gdefs.D_DIR_EXE

        # diretório não existe ?
        if not os.path.exists(ls_dir):
            # diretório não existe. cai fora...
            return False

        # percorre o diretório
        for ls_file in os.listdir(ls_dir):
            # monta o path completo do arquivo de exercício
            ls_path = os.path.join(ls_dir, ls_file)

            # não é um arquivo ?
            if not os.path.isfile(ls_path):
                # passa ao próximo
                continue

            # split name and extension
            _, l_fext = os.path.splitext(ls_file)

            # não é um arquivo XML ?
            if ".xml" != l_fext:
                # passa ao próximo
                continue

            # cria um dicionário de exercícios
            ldct_exe = exedata.CExeData(self, ls_path)

            if ldct_exe is None:
                # logger
                l_log = logging.getLogger("CModelSuper::load_table_exe")
                l_log.setLevel(logging.WARNING)
                l_log.warning(u"<E01: tabela de exercícios não existe.")

                # cai fora...
                return False

            # salva no dicionário
            self.__dct_exe.update(ldct_exe)

        # retorna
        return True

    # ---------------------------------------------------------------------------------------------
    def notify(self, f_event):
        """
        callback de tratamento de eventos recebidos

        @param f_event: evento recebido
        """
        # recebeu um evento de "save to disk" ?
        if isinstance(f_event, events.CSave2Disk):
            pass

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_exe(self):
        """
        get dicionário de exercícios
        """
        return self.__dct_exe

    @dct_exe.setter
    def dct_exe(self, f_val):
        """
        get dicionário de exercícios
        """
        self.__dct_exe = f_val

# < the end >--------------------------------------------------------------------------------------
