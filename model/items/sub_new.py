#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
sub_new

mantém as informações sobre um procedimento de subida

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

# model
import model.items.prc_model as model
import model.items.brk_new as brknew

# control
import control.events.events_basic as event

# < class CSubNEW >--------------------------------------------------------------------------------

class CSubNEW(model.CPrcModel):
    """
    mantém as informações específicas sobre procedimento de subida

    <subida nSub="1">
      <descricao>BGC 2A</descricao>
      <aerodromo>SBGR</aerodromo>
      <pista>09R</pista>

      <breakpoint nBrk="1"> ... </breakpoint>
    </subida>
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_model, f_data=None, fs_ver="0001"):
        """
        @param f_model: model manager
        @param f_data: dados do procedimento de subida
        @param fs_ver: versão do formato
        """
        # check input
        assert f_model

        # init super class
        super(CSubNEW, self).__init__()

        # salva o model manager localmente
        self.__model = f_model

        # salva o event manager localmente
        self.__event = f_model.event

        # herdados de CPrcModel
        # self.v_prc_ok      # (bool)
        # self.i_prc_id      # identificação do procedimento de subida
        # self.s_prc_desc    # descrição do procedimento de subida (nome)

        # pointer to o aeródromo da subida
        self.__ptr_sub_aer = None
        # pointer to a pista da subida
        self.__ptr_sub_pis = None

        # procedimento de decolagem associado
        self.__ptr_sub_prc_dec = None

        # lista de break-points da subida
        self.__lst_sub_brk = []

        # recebeu dados ?
        if f_data is not None:
            # recebeu uma lista ?
            if isinstance(f_data, dict):
                # cria uma procedimento de subida com os dados da lista
                self.__load_sub(f_data, fs_ver)

            # recebeu uma procedimento de subida ?
            elif isinstance(f_data, CSubNEW):
                # copia a procedimento de subida
                self.copy_sub(f_data)

    # ---------------------------------------------------------------------------------------------
    def copy_sub(self, f_sub):
        """
        copy constructor
        cria um novo procedimento de subida a partir de um outro procedimento de subida

        @param f_sub: procedimento de subida a ser copiado
        """
        # check input
        assert f_sub

        # init super class
        super(CSubNEW, self).copy_prc(f_sub)

        # pointer to aeródromo da subida
        self.__ptr_sub_aer = f_sub.ptr_sub_aer

        # pointer to pista da subida
        self.__ptr_sub_pis = f_sub.ptr_sub_pis

        # procedimento de decolagem associado
        self.__ptr_sub_prc_dec = f_sub.ptr_sub_prc_dec

        # lista de break-points da subida
        self.__lst_sub_brk = list(f_sub.lst_sub_brk)

    # ---------------------------------------------------------------------------------------------
    def __load_sub(self, fdct_data, fs_ver="0001"):
        """
        carrega os dados de procedimento de subida a partir de um dicionário (formato 0001)

        @param fdct_data: dicionário com os dados do procedimento de subida
        @param fs_ver: versão do formato dos dados
        """
        # formato versão 0.01 ?
        if "0001" == fs_ver:
            # cria a procedimento de subida
            self.__make_sub(fdct_data)

        # otherwise, formato desconhecido
        else:
            # logger
            l_log = logging.getLogger("CSubNEW::__load_sub")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: formato desconhecido.")

            # cria um evento de quit
            l_evt = event.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # cai fora...
            sys.exit(1)

    # ---------------------------------------------------------------------------------------------
    def __make_sub(self, fdct_data):
        """
        carrega os dados de procedimento de subida a partir de um dicionário (formato 0001)

        @param fdct_data: dicionário com os dados do procedimento de subida
        """
        # identificação do procedimento de subida
        if "nSub" in fdct_data:
            self.i_prc_id = int(fdct_data["nSub"])
            self.s_prc_desc = u"Subida {:03d}".format(fdct_data["nSub"])

        # descrição
        if "descricao" in fdct_data:
            self.s_prc_desc = fdct_data["descricao"]

        # aeródromo da subida
        if "aerodromo" in fdct_data:
            # obtém o dicionário de aeródromos
            ldct_aer = self.__model.airspace.dct_aer

            # obtém o indicativo do aeródromo
            ls_aer_id = fdct_data["aerodromo"]

            # obtém o aeródromo de subida
            self.__ptr_sub_aer = ldct_aer.get(ls_aer_id, None)

            # não existe o aeródromo no dicionário ?
            if self.__ptr_sub_aer is None:
                # logger
                l_log = logging.getLogger("CSubNEW::__make_sub")
                l_log.setLevel(logging.WARNING)
                l_log.warning(u"<E01: aerodromo [{}] não existe no dicionário.".format(ls_aer_id))

        # pista de subida
        if "pista" in fdct_data:
            # existe o aeródromo ?
            if self.__ptr_sub_aer is not None:
                # obtém o dicionário de pistas
                ldct_pis = self.__ptr_sub_aer.dct_aer_pistas

                # obtém o indicativo do aeródromo
                ls_pis_id = fdct_data["pista"]

                # obtém o pista de subida
                self.__ptr_sub_pis = ldct_pis.get(ls_pis_id, None)

                # não existe a pista no dicionário ?
                if self.__ptr_sub_pis is None:
                    # logger
                    l_log = logging.getLogger("CSubNEW::__make_sub")
                    l_log.setLevel(logging.WARNING)
                    l_log.warning(u"<E02: pista [{}] não existe no dicionário.".format(ls_pis_id))

        # break-points da subida
        if "breakpoints" in fdct_data:
            # para todos break-points da subida...
            for l_brk in sorted(fdct_data["breakpoints"], key=lambda l_k: l_k["nBrk"]):
                # cria o break-points
                lo_brk = brknew.CBrkNEW(self.__model, self, l_brk)
                assert lo_brk

                # coloca o break-point na lista
                self.__lst_sub_brk.append(lo_brk)

        # (bool)
        self.v_prc_ok = True

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def ptr_sub_aer(self):
        """
        get aeródromo da subida
        """
        return self.__ptr_sub_aer

    @ptr_sub_aer.setter
    def ptr_sub_aer(self, f_val):
        """
        set aeródromo da subida
        """
        self.__ptr_sub_aer = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def lst_sub_brk(self):
        """
        get lista de break-points da subida
        """
        return self.__lst_sub_brk

    @lst_sub_brk.setter
    def lst_sub_brk(self, f_val):
        """
        set lista de break-points da subida
        """
        self.__lst_sub_brk = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def ptr_sub_pis(self):
        """
        get pista da subida
        """
        return self.__ptr_sub_pis

    @ptr_sub_pis.setter
    def ptr_sub_pis(self, f_val):
        """
        set pista da subida
        """
        self.__ptr_sub_pis = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def ptr_sub_prc_dec(self):
        """
        get procedimento de decolagem associado
        """
        return self.__ptr_sub_prc_dec

    @ptr_sub_prc_dec.setter
    def ptr_sub_prc_dec(self, f_val):
        """
        set procedimento de decolagem associado
        """
        self.__ptr_sub_prc_dec = f_val

# < the end >--------------------------------------------------------------------------------------
