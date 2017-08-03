#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
trj_data

mantém as informações sobre o dicionário de procedimento de trajetórias

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

revision 0.3  2017/jul  matias
coding the save2disk method

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
from __future__ import print_function

__version__ = "$revision: 0.2$"
__author__ = "Ivan Matias"
__date__ = "2017/07"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import sys

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtXml

# libs
import libs.coords.coord_defs as cdefs

# model
import model.items.trj_new as model
import model.items.parser_utils as parser

# control
import control.events.events_basic as events
import control.control_debug as cdbg

# < class CTrjData >-------------------------------------------------------------------------------

class CTrjData(dict):
    """
    mantém as informações sobre o dicionário de procedimento de trajetória

    <trajetoria nTrj="1">
        <descricao>DEP SDJD VIA SCB</descricao>
        <star>S</star>
        <proa>123</proa>

        <breakpoint nBrk="1"> ... </breakpoint>
    </trajetoria>
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_model, f_data=None):
        """
        @param f_model: model manager
        @param f_data: dados dos procedimento de trajetórias
        """
        # check input
        assert f_model

        # inicia a super class
        super(CTrjData, self).__init__()

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
                # cria um procedimento de trajetória com os dados da lista
                # self.make_trj(f_data)
                pass

            # recebeu um procedimento de trajetória ?
            elif isinstance(f_data, CTrjData):
                # copia o procedimento de trajetória
                # self.copy_trj(f_data)
                pass

            # senão, recebeu o pathname de um arquivo de procedimento de trajetória
            else:
                # carrega o dicionário de procedimento de trajetória de um arquivo em disco
                self.parse_trj_xml(f_data + ".xml")

    # ---------------------------------------------------------------------------------------------
    def make_trj(self, fdct_root, fdct_data):
        """
        carrega os dados de procedimento de trajetória a partir de um dicionário

        @param fdct_data: dados do procedimento de trajetória

        @return flag e mensagem
        """
        # check input
        assert fdct_root is not None
        assert fdct_data is not None

        # é um arquivo de trajetória do newton ?
        if "trajetorias" != fdct_root["tagName"]:
            # logger
            l_log = logging.getLogger("CTrjData::make_trj")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: não é um arquivo de procedimentos de trajetória.")

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
            l_log = logging.getLogger("CTrjData::make_trj")
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
            l_log = logging.getLogger("CTrjData::make_trj")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E03: não tem a assinatura correta.")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # se não for, cai fora...
            sys.exit(1)

        # verifica se existe identificação
        if "nTrj" in fdct_data:
            # cria procedimento de trajetória
            l_trj = model.CTrjNEW(self.__model, fdct_data, fdct_root["VERSION"])
            assert l_trj

            # coloca a procedimento de trajetória no dicionário
            self[fdct_data["nTrj"]] = l_trj

        # senão, não existe identificação
        else:
            # monta uma mensagem
            ls_msg = u"não tem identificação. Trajetória não incluída."

            # logger
            l_log = logging.getLogger("CTrjData::make_trj")
            l_log.setLevel(logging.WARNING)
            l_log.warning(u"<E04: {}".format(ls_msg))

            # se não for, cai fora...
            return False, ls_msg

        # retorna Ok
        return True, None

    # ---------------------------------------------------------------------------------------------
    def parse_trj_xml(self, fs_trj_pn):
        """
        carrega o arquivo de procedimentos de trajetória

        @param fs_trj_pn: pathname do arquivo em disco
        """
        # check input
        assert fs_trj_pn

        # cria o QFile para o arquivo XML do procedimentos de trajetória
        l_data_file = QtCore.QFile(fs_trj_pn)
        assert l_data_file is not None

        # abre o arquivo XML do procedimentos de trajetória
        l_data_file.open(QtCore.QIODevice.ReadOnly)

        # erro na abertura do arquivo ?
        if not l_data_file.isOpen():
            # logger
            l_log = logging.getLogger("CTrjData::parse_trj_xml")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: erro na abertura de {}.".format(fs_trj_pn))

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # termina a aplicação
            sys.exit(1)

        # cria o documento XML do procedimento de trajetória
        l_xdoc_trj = QtXml.QDomDocument("trajetorias")
        assert l_xdoc_trj is not None

        # erro na carga do documento ?
        if not l_xdoc_trj.setContent(l_data_file):
            # fecha o arquivo
            l_data_file.close()

            # logger
            l_log = logging.getLogger("CTrjData::parse_trj_xml")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E02: falha no parse de {}.".format(fs_trj_pn))

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
        l_elem_root = l_xdoc_trj.documentElement()
        assert l_elem_root is not None

        # faz o parse dos atributos do elemento raíz
        ldct_root = parser.parse_root_element(l_elem_root)

        # cria uma lista com os elementos de procedimento de trajetória
        l_node_list = l_elem_root.elementsByTagName("trajetoria")

        # para todos os nós na lista...
        for li_ndx in xrange(l_node_list.length()):
            # inicia o dicionário de dados
            ldct_data = {}

            # inicia a lista de breakpoints
            ldct_data["breakpoints"] = []

            # obtém um nó da lista
            l_element = l_node_list.at(li_ndx).toElement()
            assert l_element is not None

            # read identification if available
            if l_element.hasAttribute("nTrj"):
                ldct_data["nTrj"] = int(l_element.attribute("nTrj"))

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
                    ldct_tmp = parser.parse_trajetoria(l_element)

                    # atualiza o dicionário com o breakpoint
                    if "breakpoint" in ldct_tmp:
                        # atualiza o dicionário com o breakpoint
                        ldct_data["breakpoints"].append(ldct_tmp["breakpoint"])

                        # apaga este elemento
                        del ldct_tmp["breakpoint"]

                    # atualiza o dicionário de dados
                    ldct_data.update(ldct_tmp)

                # próximo nó
                l_node = l_node.nextSibling()
                assert l_node is not None

            # cdbg.M_DBG.debug("trajetória: " + str(ldct_data))

            # carrega os dados de procedimento de trajetória a partir de um dicionário
            self.make_trj(ldct_root, ldct_data)

    # ---------------------------------------------------------------------------------------------
    def save2disk(self, fs_trj_pn=None):
        """
        salva os dados da procedimento de trajetória em um arquivo em disco

        @param fs_trj_pn: path name do arquivo onde salvar

        @return flag e mensagem
        """
        # tem colocar o .xml do final do parâmetro fs_trj_pn para montar o nome do arquivo.
        cdbg.M_DBG.debug("Saving file [%s.xml]" % fs_trj_pn)

        l_file = open("%s.xml" % fs_trj_pn, 'w')

        print ( "<?xml version='1.0' encoding='UTF-8'?>", file = l_file )
        print ( "<!DOCTYPE trafegos>", file = l_file )
        print ( "<trajetorias VERSION=\"0001\" CODE=\"1961\" FORMAT=\"NEWTON\">", file = l_file )

        for li_nTrf, l_oTrjNew in self.__model.dct_trj.items():
            print ( "", file=l_file )
            print ( "    <trajetoria nTrj=\"%s\">" % str(l_oTrjNew.i_prc_id), file = l_file )
            print ( "        <descricao>%s</descricao>" % l_oTrjNew.s_prc_desc, file = l_file )
            print ( "        <star>N</star>", file = l_file )
            # Breakpoints da trajetória
            for l_oBrkNew in l_oTrjNew.lst_trj_brk:
                print ( "", file=l_file )
                print ( "        <breakpoint nBrk=\"%d\">" % l_oBrkNew.i_brk_id, file=l_file)
                print ( "          <coord>", file = l_file )
                print ( "            <tipo>%s</tipo>" % l_oBrkNew.s_brk_tipo, file = l_file )
                print ( "            <cpoA>%s</cpoA>" % l_oBrkNew.s_brk_cpoA, file = l_file )
                print ( "            <cpoB>%s</cpoB>" % l_oBrkNew.s_brk_cpoB, file = l_file )
                print ( "            <cpoC>%s</cpoC>" % l_oBrkNew.s_brk_cpoC, file = l_file )
                print ( "            <cpoD>%s</cpoD>" % l_oBrkNew.s_brk_cpoD, file = l_file )
                print ( "          </coord>", file = l_file)
                # converte a altitude de m para ft
                lf_AltFt = l_oBrkNew.f_brk_alt * cdefs.D_CNV_M2FT
                li_AltFt = int(lf_AltFt)
                if (lf_AltFt - li_AltFt) > 0.5:
                    li_AltFt = li_AltFt + 1
                print ( "          <altitude>%d</altitude>" % li_AltFt, file = l_file )
                # converte a velocidade de m/s para kt
                li_VelKt = int(l_oBrkNew.f_brk_vel * cdefs.D_CNV_MS2KT)
                print ( "          <velocidade>%d</velocidade>" % li_VelKt, file = l_file )
                print ( "          <procedimento>%s</procedimento>" % l_oBrkNew.s_brk_prc, file = l_file )
                print ( "        </breakpoint>", file=l_file)

            print ( "    </trajetoria>", file = l_file )

        print ( "", file=l_file )
        print ( "</trajetorias>", file = l_file )

        l_file.close ()

        # return code
        lv_ok = True

        # mensagem
        ls_msg = "save Ok"

        # logger
        cdbg.M_DBG.info("save2disk:<<")

        # retorna flag e mensagem
        return lv_ok, ls_msg

# < the end >--------------------------------------------------------------------------------------
