#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
apx_new

mantém as informações sobre um procedimento de aproximação

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
import control.events.events_basic as events

# < class CApxNEW >--------------------------------------------------------------------------------

class CApxNEW(model.CPrcModel):
    """
    mantém as informações específicas sobre procedimento de aproximação

    <aproximacao nApx="1">
      <descricao>FINAL H3</descricao>
      <aerodromo>SBSP</aerodromo>
      <pista>17R</pista>
      <ils>N</ils>
      <aproxperd>N</aproxperd>
      <espera>2</espera>
      <breakpoint nBrk="1"> ... </breakpoint>
    </aproximacao>
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_model, f_data=None, fs_ver="0001"):
        """
        @param f_model: model manager
        @param f_data:  dados do procedimento de aproximação
        @param fs_ver:  versão do formato
        """
        # check input
        assert f_model
                
        # init super class
        super(CApxNEW, self).__init__()

        # salva o model manager
        self.__model = f_model

        # salva o event manager
        self.__event = f_model.event

        # herdado de PrcModel
        # self.v_prc_ok      # ok (bool)
        # self.i_prc_id      # identificação do procedimento
        # self.s_prc_desc    # descrição do procedimento

        # pointer do aeródromo
        self.__ptr_apx_aer = None
        # pointer da pista
        self.__ptr_apx_pis = None
        # procedimento de pouso associado
        self.__ptr_apx_prc_pouso = None

        # ILS
        self.__v_apx_ils = False
        self.__ptr_apx_prc_ils = None

        # aproximação perdida
        self.__v_apx_ape = False
        self.__ptr_apx_prc_ape = None

        # espera
        self.__ptr_apx_prc_esp = None

        # lista de breakpoints da aproximação
        self.__lst_apx_brk = []

        # recebeu dados ?
        if f_data is not None:
            # recebeu uma lista ?
            if isinstance(f_data, dict):
                # cria uma procedimento de aproximação com os dados da lista
                self.__load_apx(f_data, fs_ver)

            # recebeu uma procedimento de aproximação ?
            elif isinstance(f_data, CApxNEW):
                # copia a procedimento de aproximação
                self.copy_apx(f_data)

    # ---------------------------------------------------------------------------------------------
    def copy_apx(self, f_apx):
        """
        copy constructor
        cria um novo procedimento de aproximação a partir de uma outra aproximação

        @param f_apx: procedimento de aproximação a ser copiada
        """
        # check input
        assert f_apx

        # copy super class attributes
        super(CApxNEW, self).copy_prc(f_apx)

        # pointer do aeródromo
        self.__ptr_apx_aer = f_apx.ptr_apx_aer
        # pointer da pista
        self.__ptr_apx_pis = f_apx.ptr_apx_pis
        # procedimento de pouso associado
        self.__ptr_apx_prc_pouso = f_apx.ptr_apx_prc_pouso

        # flag ILS
        self.__v_apx_ils = f_apx.v_apx_ils
        # flag apxPerdida
        self.__v_apx_ape = f_apx.v_apx_ape
        # número da espera
        self.__ptr_apx_prc_esp = f_apx.ptr_apx_prc_esp

        # lista de breakpoints da subida              !!!REVER!!! deepcopy ?
        self.__lst_apx_brk = list(f_apx.lst_apx_brk)

    # ---------------------------------------------------------------------------------------------
    def __load_apx(self, fdct_data, fs_ver="0001"):
        """
        carrega os dados de procedimento de aproximação a partir de um dicionário

        @param fdct_data: dicionário com os dados do procedimento de aproximação
        @param fs_ver: versão do formato dos dados
        """
        # formato versão 0.01 ?
        if "0001" == fs_ver:
            # cria a procedimento de aproximação
            self.__make_apx(fdct_data)

        # senão, formato desconhecido
        else:
            # logger
            l_log = logging.getLogger("CApxNEW::__load_apx")
            l_log.setLevel(logging.DEBUG)
            l_log.critical(u"<E01: formato desconhecido.")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # cai fora...
            sys.exit(1)

    # ---------------------------------------------------------------------------------------------
    def __make_apx(self, fdct_data):
        """
        carrega os dados de procedimento de aproximação a partir de um dicionário (formato 0001)

        @param fdct_data: dicionário com os dados do procedimento de aproximação
        """
        # identificação do procedimento de aproximação
        if "nApx" in fdct_data:
            self.i_prc_id = int(fdct_data["nApx"])
            self.s_prc_desc = u"Aproximação {:03d}".format(fdct_data["nApx"])

        # descrição do procedimento de aproximação
        if "descricao" in fdct_data:
            self.s_prc_desc = fdct_data["descricao"].strip()

        # aeródromo da aproximação
        if "aerodromo" in fdct_data:
            # obtém o dicionário de aeródromos
            ldct_aer = self.__model.airspace.dct_aer

            # obtém o indicativo do aeródromo
            ls_aer_indc = fdct_data["aerodromo"]

            # obtém o aeródromo de aproximação
            self.__ptr_apx_aer = ldct_aer.get(ls_aer_indc, None)

            # não existe o aeródromo no dicionário ?
            if self.__ptr_apx_aer is None:
                # logger
                l_log = logging.getLogger("CSubNEW::__make_apx")
                l_log.setLevel(logging.WARNING)
                l_log.warning(u"<E01: aeródromo [{}] não existe.".format(ls_aer_indc))

        # pista de aproximação
        if "pista" in fdct_data:
            # existe o aeródromo ?
            if self.__ptr_apx_aer is not None:
                # obtém o dicionário de pistas
                ldct_pis = self.__ptr_apx_aer.dct_aer_pistas

                # obtém o indicativo do aeródromo
                ls_pst_indc = fdct_data["pista"]

                # obtém o pista de subida
                self.__ptr_apx_pis = ldct_pis.get(ls_pst_indc, None)

                # não existe a pista no dicionário ?
                if self.__ptr_apx_pis is None:
                    # logger
                    l_log = logging.getLogger("CApxNEW::__make_apx")
                    l_log.setLevel(logging.WARNING)
                    l_log.warning(u"<E02: aeródromo [{}]/pista [{}] não existe.".format(self.__ptr_apx_aer.s_aer_indc, ls_pst_indc))

        # flag ILS
        if "ils" in fdct_data:
            self.__v_apx_ils = ('S' == fdct_data["ils"].strip().upper())

        # flag aproximação perdida
        if "aproxperd" in fdct_data:
            self.__v_apx_ape = ('S' == fdct_data["aproxperd"].strip().upper())

        # número da espera
        if "espera" in fdct_data:
            self.__ptr_apx_prc_esp = int(fdct_data["espera"])

        # breakpoints da aproximação
        if "breakpoints" in fdct_data:
            # para todos breakpoints da aproximação...
            for l_brk in sorted(fdct_data["breakpoints"], key=lambda l_k: l_k["nBrk"]):
                # cria o breakpoints
                lo_brk = brknew.CBrkNEW(self.__model, self, l_brk)
                assert lo_brk

                # coloca o breakpoint na lista
                self.__lst_apx_brk.append(lo_brk)

        # (bool)
        self.v_prc_ok = True

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def ptr_apx_aer(self):
        """
        get aeródromo
        """
        return self.__ptr_apx_aer

    @ptr_apx_aer.setter
    def ptr_apx_aer(self, f_val):
        """
        set aeródromo
        """
        self.__ptr_apx_aer = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def v_apx_ape(self):
        """
        get flag aproximação perdida
        """
        return self.__v_apx_ape

    @v_apx_ape.setter
    def v_apx_ape(self, f_val):
        """
        set flag aproximação perdida
        """
        self.__v_apx_ape = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def lst_apx_brk(self):
        """
        get lista de breakpoints da aproximação
        """
        return self.__lst_apx_brk

    @lst_apx_brk.setter
    def lst_apx_brk(self, f_val):
        """
        set lista de breakpoints da aproximação
        """
        self.__lst_apx_brk = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def v_apx_ils(self):
        """
        get flag ILS
        """
        return self.__v_apx_ils

    @v_apx_ils.setter
    def v_apx_ils(self, f_val):
        """
        set flag ILS
        """
        self.__v_apx_ils = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def ptr_apx_pis(self):
        """
        get pista
        """
        return self.__ptr_apx_pis

    @ptr_apx_pis.setter
    def ptr_apx_pis(self, f_val):
        """
        set pista
        """
        self.__ptr_apx_pis = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def ptr_apx_prc_ape(self):
        """
        get procedimento de aproximação perdida
        """
        return self.__ptr_apx_prc_ape

    @ptr_apx_prc_ape.setter
    def ptr_apx_prc_ape(self, f_val):
        """
        set procedimento de aproximação perdida
        """
        self.__ptr_apx_prc_ape = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def ptr_apx_prc_esp(self):
        """
        get número da espera
        """
        return self.__ptr_apx_prc_esp

    @ptr_apx_prc_esp.setter
    def ptr_apx_prc_esp(self, f_val):
        """
        set número da espera
        """
        self.__ptr_apx_prc_esp = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def ptr_apx_prc_ils(self):
        """
        get procedimento de ILS
        """
        return self.__ptr_apx_prc_ils

    @ptr_apx_prc_ils.setter
    def ptr_apx_prc_ils(self, f_val):
        """
        set procedimento de ILS
        """
        self.__ptr_apx_prc_ils = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def ptr_apx_prc_pouso(self):
        """
        get procedimento de pouso
        """
        return self.__ptr_apx_prc_pouso

    @ptr_apx_prc_pouso.setter
    def ptr_apx_prc_pouso(self, f_val):
        """
        set procedimento de pouso
        """
        self.__ptr_apx_prc_pouso = f_val

# < the end >--------------------------------------------------------------------------------------
