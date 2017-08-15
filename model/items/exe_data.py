#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
exe_data

mantém as informações sobre o dicionário de exercícios

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
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import sys

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtXml

# model
import model.items.exe_new as model
import model.items.parser_utils as parser

# control
import control.events.events_basic as events
# import control.control_debug as cdbg

# < class CExeData >-------------------------------------------------------------------------------

class CExeData(dict):
    """
    mantém as informações sobre o dicionário de exercícios

    <exercicio nExe="SBSP5301">
        <descricao>PBN 2013 INTEGRADO RJ E SP 17/09/15/15</descricao>
        <horainicio>06:00</horainicio>
    </exercicio>
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_model, f_data=None):
        """
        @param f_model: model manager
        @param f_data: dados do exercício
        """
        # check input
        assert f_model

        # inicia a super class
        super(CExeData, self).__init__()

        # salva o model manager localmente
        self.__model = f_model
        assert self.__model

        # salva o event manager localmente
        self.__event = f_model.event
        assert self.__event

        # recebeu dados ?
        if f_data is not None:
            # recebeu uma lista ?
            if isinstance(f_data, list):
                # cria um exercício com os dados da lista
                # self.make_exe(f_data)
                pass

            # recebeu um exercício ?
            elif isinstance(f_data, CExeData):
                # copia o exercício
                # self.copy_exe(f_data)
                pass

            # senão, recebeu o pathname de um arquivo de exercício
            else:
                # carrega o dicionário de exercício de um arquivo em disco
                self.parse_exe_xml(f_data + ".exe.xml")

    # ---------------------------------------------------------------------------------------------
    def make_exe(self, fdct_root, fdct_data):
        """
        carrega os dados de exercício a partir de um dicionário

        @param fdct_data: lista de dados de exercício

        @return flag e mensagem
        """
        # check input 
        assert fdct_root is not None
        assert fdct_data is not None

        # é uma exercício do newton ?
        if "exercicios" != fdct_root["tagName"]:
            # logger
            l_log = logging.getLogger("CExeData::make_exe")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: não é um arquivo de exercício.")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # se não for, cai fora...
            sys.exit(1)

        # é um arquivo do newton ?
        if "NEWTON" != fdct_root["FORMAT"]:
            # logger
            l_log = logging.getLogger("CExeData::make_exe")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E02: não está em um formato aceito.")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # se não for, cai fora...
            sys.exit(1)

        # é a assinatura do newton ?
        if "1961" != fdct_root["CODE"]:
            # logger
            l_log = logging.getLogger("CExeData::make_exe")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E03: não tem a assinatura correta.")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # se não for, cai fora...
            sys.exit(1)

        # existe indicativo ?
        if "nExe" in fdct_data:
            # cria exercício
            l_exe = model.CExeNEW(self.__model, fdct_data, fdct_root["VERSION"])
            assert l_exe

            # coloca a exercício no dicionário
            self[fdct_data["nExe"]] = l_exe

        # senão, não existe indicativo
        else:
            # monta uma mensagem
            ls_msg = u"não tem identificação. Exercício não incluído."

            # logger
            l_log = logging.getLogger("CExeData::make_exe")
            l_log.setLevel(logging.WARNING)
            l_log.warning("<E04: {}".format(ls_msg))

            # se não for, cai fora...
            return False, ls_msg

        # retorna Ok
        return True, None

    # ---------------------------------------------------------------------------------------------
    def parse_exe_xml(self, fs_exe_path):
        """
        carrega o arquivo de exercício

        @param fs_exe_path: pathname do arquivo em disco
        """
        # check input 
        assert fs_exe_path

        # cria o QFile para o arquivo XML do exercício
        l_data_file = QtCore.QFile(fs_exe_path)
        assert l_data_file is not None

        # abre o arquivo XML do exercício
        l_data_file.open(QtCore.QIODevice.ReadOnly)

        # erro na abertura do arquivo ?
        if not l_data_file.isOpen():
           # logger
            l_log = logging.getLogger("CExeData::parse_exe_xml")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: erro na abertura de {}.".format(fs_exe_path))

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # termina a aplicação
            sys.exit(1)

        # cria o documento XML do exercício
        l_xdoc_exe = QtXml.QDomDocument("exercicios")
        assert l_xdoc_exe is not None

        # erro na carga do documento ?
        if not l_xdoc_exe.setContent(l_data_file):
            # fecha o arquivo
            l_data_file.close()

            # logger
            l_log = logging.getLogger("CExeData::parse_exe_xml")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E02: falha no parse de {}.".format(fs_exe_path))

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # termina a aplicação
            sys.exit(1)

        # fecha o arquivo
        l_data_file.close()

        # obtém o elemento raíz do documento
        l_elem_root = l_xdoc_exe.documentElement()
        assert l_elem_root is not None

        # faz o parse dos atributos do elemento raíz
        ldct_root = parser.parse_root_element(l_elem_root)

        # cria uma lista com os elementos de exercício
        l_node_list = l_elem_root.elementsByTagName("exercicio")

        # para todos os nós na lista...
        for li_ndx in xrange(l_node_list.length()):
            # inicia o dicionário de dados
            ldct_data = {}

            # obtém um nó da lista
            l_element = l_node_list.at(li_ndx).toElement()
            assert l_element is not None

            # read identification if available
            if l_element.hasAttribute("nExe"):
                ldct_data["nExe"] = str(l_element.attribute("nExe"))

            # obtém o primeiro nó da sub-árvore
            l_node = l_element.firstChild()
            assert l_node is not None

            # percorre a sub-árvore
            while not l_node.isNull():
                # tenta converter o nó em um elemento
                l_element = l_node.toElement()
                assert l_element is not None

                # o nó é um elemento ?
                if not l_element.isNull():
                    # faz o parse do elemento
                    ldct_tmp = parser.parse_exercicio(l_element)

                    # atualiza o dicionário de dados
                    ldct_data.update(ldct_tmp)

                # próximo nó
                l_node = l_node.nextSibling()
                assert l_node is not None

            # carrega os dados de exercício a partir de um dicionário
            self.make_exe(ldct_root, ldct_data)

    # ---------------------------------------------------------------------------------------------
    def save2disk(self, fs_exe_path=None):
        """
        salva os dados da exercício em um arquivo em disco

        @param fs_exe_path: path name do arquivo onde salvar

        @return flag e mensagem
        """
        # return code
        lv_ok = True

        # mensagem
        ls_msg = "save Ok"

        # retorna flag e mensagem
        return lv_ok, ls_msg

# < the end >--------------------------------------------------------------------------------------
