#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
trj_new

mantém as informações sobre um procedimento de trajetória

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
import model.items.brk_new as brktrj

# control
import control.events.events_basic as events

# < class CTrjNEW >--------------------------------------------------------------------------------

class CTrjNEW(model.CPrcModel):
    """
    mantém as informações específicas sobre procedimento de trajetória

    <trajetoria nTrj="1">
        <descricao>DEP SDJD VIA SCB</descricao>
        <star>S</star>
        <proa>123</proa>

        <breakpoint nBrk="1"> ... </breakpoint>
    </trajetoria>
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_model, f_data=None, fs_ver="0001"):
        """
        @param f_model: model manager
        @param f_data: dados do procedimento de trajetória
        @param fs_ver: versão do formato
        """
        # init super class
        super(CTrjNEW, self).__init__()

        # salva o model manager localmente
        self.__model = f_model
        assert self.__model

        # salva o event manager localmente
        self.__event = f_model.event
        assert self.__event

        # herdado de CPrcModel
        # self.v_prc_ok      # (bool)
        # self.i_prc_id      # identificação do procedimento de trajetória
        # self.s_prc_desc    # descrição do procedimento de trajetória

        # star
        self.__v_trj_star = False

        # proa a seguir após a trajetória
        self.__f_trj_proa = 0.

        # lista de break-points da trajetória
        self.__lst_trj_brk = []

        # recebeu dados ?
        if f_data is not None:
            # recebeu uma lista ?
            if isinstance(f_data, dict):
                # cria uma procedimento de trajetória com os dados da lista
                self.__load_trj(f_data, fs_ver)

            # recebeu uma procedimento de trajetória ?
            elif isinstance(f_data, CTrjNEW):
                # copia a procedimento de trajetória
                self.copy_trj(f_data)

    # ---------------------------------------------------------------------------------------------
    def copy_trj(self, f_trj):
        """
        copy constructor.
        cria uma nova procedimento de trajetória a partir de uma outra procedimento de trajetória

        @param f_trj: procedimento de trajetória a ser copiada
        """
        # check input
        assert f_trj

        # copy super class attributes
        super(CTrjNEW, self).copy_prc(f_trj)

        # flag star
        self.__v_trj_star = f_trj.v_trj_star

        # lista de break-points
        self.__lst_trj_brk = list(f_trj.lst_trj_brk)

    # ---------------------------------------------------------------------------------------------
    def __load_trj(self, fdct_data, fs_ver="0001"):
        """
        carrega os dados de procedimento de trajetória a partir de um dicionário (formato 0001)

        @param fdct_data: dicionário com os dados do procedimento de trajetória
        @param fs_ver: versão do formato dos dados
        """
        # formato versão 0.01 ?
        if "0001" == fs_ver:
            # cria a procedimento de trajetória
            self.__make_trj(fdct_data)

        # senão, formato desconhecido
        else:
            # logger
            l_log = logging.getLogger("CTrjNEW::__load_trj")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: formato desconhecido.")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # cai fora...
            sys.exit(1)

    # ---------------------------------------------------------------------------------------------
    def __make_trj(self, fdct_data):
        """
        carrega os dados de procedimento de trajetória a partir de um dicionário (formato 0001)

        @param fdct_data: dicionário com os dados do procedimento de trajetória
        """
        # identificação do procedimento de trajetória
        if "nTrj" in fdct_data:
            self.i_prc_id = int(fdct_data["nTrj"])
            self.s_prc_desc = u"Trajetória {:03d}".format(fdct_data["nTrj"])            

        # descrição
        if "descricao" in fdct_data:
            self.s_prc_desc = fdct_data["descricao"]

        # star
        if "star" in fdct_data:
            self.__v_trj_star = ('S' == fdct_data["star"].strip().upper())

        # proa
        if "proa" in fdct_data:
            self.__f_trj_proa = float(fdct_data["proa"].strip().upper())

        # break-points da trajetória
        if "breakpoints" in fdct_data:
            # para todos break-points da trajetória...
            for l_brk in sorted(fdct_data["breakpoints"], key=lambda l_k: l_k["nBrk"]):
                # cria o break-point
                lo_brk = brktrj.CBrkNEW(self.__model, self, l_brk)
                assert lo_brk

                # coloca o break-point na lista
                self.__lst_trj_brk.append(lo_brk)

        # (bool)
        self.v_prc_ok = True

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def lst_trj_brk(self):
        """
        get lista de break-points da trajetória
        """
        return self.__lst_trj_brk

    @lst_trj_brk.setter
    def lst_trj_brk(self, f_val):
        """
        set lista de break-points da trajetória
        """
        self.__lst_trj_brk = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_trj_proa(self):
        """
        get proa a seguir após a trajetória
        """
        return self.__f_trj_proa

    @f_trj_proa.setter
    def f_trj_proa(self, f_val):
        """
        set proa a seguir após a trajetória
        """
        # check input
        assert 0. <= f_val <= 360.

        # salva proa
        self.__f_trj_proa = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def v_trj_star(self):
        """
        get flag star
        """
        return False  # self.__v_trj_star

    @v_trj_star.setter
    def v_trj_star(self, f_val):
        """
        set flag star
        """
        self.__v_trj_star = f_val

# < the end >--------------------------------------------------------------------------------------
