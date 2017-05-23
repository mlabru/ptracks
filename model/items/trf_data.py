#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
trf_data

mantém as informações sobre o dicionário de tráfegos

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
from PyQt4 import QtCore, QtXml

# model
import model.items.trf_new as model
import model.items.parser_utils as parser

# control
import control.events.events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CTrfData >-------------------------------------------------------------------------------

class CTrfData(dict):
    """
    mantém as informações sobre o dicionário de tráfegos

    <trafego nTrf="1">
        <designador>A319</designador>
        <ssr>7001</ssr>
        <indicativo>TAM3912</indicativo>
        <origem>SBSP</origem>
        <destino>SBRJ</destino>
        <procedimento>SUB307</procedimento>
        <programa>PRG001</programa>
        <coord> ... </coord>
        <temptrafego>0</temptrafego>
        <rvsm>S</rvsm>
        <rota>LOPES OPREV CANO</rota>
        <niveltrj>270</niveltrj>
        <veltrj>380</veltrj>
    </trafego>
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_model, f_data=None, f_exe=None):
        """
        @param f_model: event manager
        @param f_data: dados das tráfegos
        @param f_exe: exercício
        """
        # check input
        assert f_model
        assert f_exe

        # inicia a super class
        super(CTrfData, self).__init__()

        # salva o model manager localmente
        self.__model = f_model

        # salva o event manager localmente
        self.__event = f_model.event
        assert self.__event

        # salva o exercício localmente
        self.__exe = f_exe

        # recebeu dados ?
        if f_data is not None:
            # recebeu uma lista ?
            if isinstance(f_data, list):
                # cria uma tráfego com os dados da lista
                # self.make_trf(f_data)
                pass

            # recebeu uma tráfego ?
            elif isinstance(f_data, CTrfData):
                # copia a tráfego
                # self.copy_trf(f_data)
                pass

            # otherwise, recebeu o pathname de uma tráfego
            else:
                # carrega a tráfego de um arquivo em disco
                self.load_file(f_data)

    # ---------------------------------------------------------------------------------------------
    def load_file(self, fs_trf_pn):
        """
        carrega os dados do tráfego de um arquivo em disco

        @param fs_trf_pn: pathname do arquivo em disco
        """
        # check input
        assert fs_trf_pn

        # carrega o arquivo de tráfego
        self.parse_trf_xml(fs_trf_pn + ".trf.xml")

    # ---------------------------------------------------------------------------------------------
    def make_trf(self, fdct_root, fdct_data):
        """
        carrega os dados de tráfego a partir de um dicionário

        @param fdct_root: DOCUMENT ME!
        @param fdct_data: lista de dados de tráfego

        @return flag e mensagem
        """
        # check input
        assert fdct_root is not None
        assert fdct_data is not None

        # return code
        lv_ok = True

        # mensagem
        ls_msg = None

        # é uma tráfego do newton ?
        if "trafegos" != fdct_root["tagName"]:
            # logger
            l_log = logging.getLogger("CTrfData::make_trf")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: não é um arquivo de tráfego.")

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
            l_log = logging.getLogger("CTrfData::make_trf")
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
            l_log = logging.getLogger("CTrfData::make_trf")
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
        if "nTrf" in fdct_data:
            # cria a tráfego
            l_trf = model.CTrfNEW(self.__model, fdct_data, fdct_root["VERSION"])
            assert l_trf

            # coloca a tráfego no dicionário
            self[fdct_data["nTrf"]] = l_trf

        # otherwise, não existe indicativo
        else:
            # monta uma mensagem
            ls_msg = u"não tem identificação. Tráfego não incluído."

            # logger
            l_log = logging.getLogger("CTrfData::make_trf")
            l_log.setLevel(logging.WARNING)
            l_log.warning(u"<E04: {}".format(ls_msg))

            # se não for, cai fora...
            return False, ls_msg

        # retorna Ok
        return lv_ok, ls_msg

    # ---------------------------------------------------------------------------------------------
    def parse_trf_xml(self, fs_trf_pn):
        """
        carrega o arquivo de tráfego

        @param fs_trf_pn: pathname do arquivo em disco
        """
        # check input
        assert fs_trf_pn

        # cria o QFile para o arquivo XML do tráfego
        l_data_file = QtCore.QFile(fs_trf_pn)
        assert l_data_file is not None

        # abre o arquivo XML do tráfego
        l_data_file.open(QtCore.QIODevice.ReadOnly)

        # erro na abertura do arquivo ?
        if not l_data_file.isOpen():
            # logger
            l_log = logging.getLogger("CTrfData::parse_trf_xml")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: erro na abertura de {}.".format(fs_trf_pn))

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # termina a aplicação
            sys.exit(1)

        # cria o documento XML do tráfego
        l_xdoc_trf = QtXml.QDomDocument("trafegos")
        assert l_xdoc_trf is not None

        # erro na carga do documento ?
        if not l_xdoc_trf.setContent(l_data_file):
            # fecha o arquivo
            l_data_file.close()

            # logger
            l_log = logging.getLogger("CTrfData::parse_trf_xml")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E02: falha no parse de {}.".format(fs_trf_pn))

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
        l_elem_root = l_xdoc_trf.documentElement()
        assert l_elem_root is not None

        # faz o parse dos atributos do elemento raíz
        ldct_root = parser.parse_root_element(l_elem_root)

        # cria uma lista com os elementos de tráfego
        l_node_list = l_elem_root.elementsByTagName("trafego")

        # para todos os nós na lista...
        for li_ndx in xrange(l_node_list.length()):
            # inicia o dicionário de dados
            ldct_data = {}

            # obtém um nó da lista
            l_element = l_node_list.at(li_ndx).toElement()
            assert l_element is not None

            # read identification if available
            if l_element.hasAttribute("nTrf"):
                ldct_data["nTrf"] = int(l_element.attribute("nTrf"))

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
                    # atualiza o dicionário de dados
                    ldct_data.update(parser.parse_trafego(l_element))

                # próximo nó
                l_node = l_node.nextSibling()
                assert l_node is not None

            # carrega os dados de tráfego a partir de um dicionário
            self.make_trf(ldct_root, ldct_data)

    # ---------------------------------------------------------------------------------------------
    def save2disk(self, fs_trf_pn=None):
        """
        salva os dados da tráfego em um arquivo em disco

        @param fs_trf_pn: path name do arquivo onde salvar

        @return flag e mensagem
        """
        # return code
        lv_ok = True

        # mensagem
        ls_msg = "save ok"

        # retorna flag e mensagem
        return lv_ok, ls_msg

# < the end >--------------------------------------------------------------------------------------
