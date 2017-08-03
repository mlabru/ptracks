#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
aer_new

mantém as informações sobre um aeródromo

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

# libs
import libs.coords.coord_defs as cdefs

# model
import model.items.aer_model as model
import model.items.pst_new as pstnew

# control
import control.events.events_basic as events
import control.control_debug as cdbg

# < class CAerNEW >--------------------------------------------------------------------------------

class CAerNEW(model.CAerModel):
    """
    mantém as informações específicas sobre um aeródromo

    <aerodromo nAer="SBSP">
      <descricao>Congonhas</descricao>
      <coord> ... </coord>
      <elevacao>2189</elevacao>
      <declmag>-21</declmag>
      <pista> ... </pista>
    </aerodromo>
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_model, f_data=None, fs_ver="0001"):
        """
        constructor
        
        @param f_model: model
        @param f_data: dados do aeródromo
        @param fs_ver: versão do formato
        """
        # check input
        assert f_model

        # init super class
        super(CAerNEW, self).__init__()

        # salva o model manager
        self.__model = f_model

        # salva o event manager
        self.__event = f_model.event

        # heradados de CAerModel
        # self.v_aer_ok      # ok
        # self.s_aer_indc    # identificação do aeródromo (indicativo)
        # self.s_aer_desc    # descrição do aeródromo (nome)
        # self.f_aer_elev    # elevação do aeródromo (m)

        # latitude do ARP (gr)
        self.__f_aer_lat = 0.
        # longitude do ARP (gr)
        self.__f_aer_lng = 0.
                                
        # declinação magnética (gr)
        self.__f_aer_dcl_mag = 0.

        # dicionário de pistas
        self.__dct_aer_pistas = {}
        '''
        # meteorologia

        # limite influência vento superfície
        self._fAerLimVento = 0.
        # abscissa do vento de superfície
        self._fAerVentoX = 0.
        # ordenada do vento de superfície
        self._fAerVentoY = 0.

        # indicativo da existência de registro de condição meteorológica associado ao aeródromo
        self._vAerTemMet = False
        # dados de condições meteorológicas do aeródromo
        self._oAerMeteoro = None
        '''
        # recebeu dados ?
        if f_data is not None:
            # recebeu uma lista ?
            if isinstance(f_data, dict):
                # cria uma aeródromo com os dados da lista
                self.load_aer(f_data, fs_ver)

            # recebeu uma aeródromo ?
            elif isinstance(f_data, CAerNEW):
                # copia a aeródromo
                self.copy_aer(f_data)

    # ---------------------------------------------------------------------------------------------
    def calc_cab_oposta(self):
        """
        calcula as coordenadas da cabeceira oposta de cada pista
        """
        # para todas as pistas...
        for lp_pst in self.__dct_aer_pistas.values():
            # pista não ok ?
            if not lp_pst.v_pst_ok:
                # próximo
                continue

            # cabeceira
            ls_cab = "%-3s" % lp_pst.s_pst_indc

            # cabeceira oposta
            ls_oposta = ls_cab

            # obtém o rumo da pista
            li_rumo = int(ls_cab[:2])

            # calcula o rumo inverso
            if li_rumo <= 18:
                li_rumo += 18

            else:
                li_rumo -= 18

            # converte para string
            ls_oposta = "%02d" % li_rumo

            if 'C' == ls_cab[2]:
                ls_oposta += 'C'

            elif 'L' == ls_cab[2]:
                ls_oposta += 'R'

            elif 'R' == ls_cab[2]:
                ls_oposta += 'L'

            # para todas as pistas, busca a oposta...
            for lp_pst_op in self.__dct_aer_pistas.values():
                # é a pista procurada ?
                if lp_pst_op.s_pst_indc.strip() == ls_oposta.strip():
                    # salva os dados da cabeceira oposta
                    lp_pst_op.f_pst_cab_opos_x = lp_pst.f_pst_x
                    lp_pst_op.f_pst_cab_opos_y = lp_pst.f_pst_y

                    # obtém a latitude/longitude
                    lf_lat, lf_lng, _ = self.__model.coords.xyz2geo(lp_pst.f_pst_x, lp_pst.f_pst_y, 0.)

                    # salva os dados da cabeceira oposta
                    lp_pst_op.f_pst_cab_opos_lat = lf_lat
                    lp_pst_op.f_pst_cab_opos_lng = lf_lng

                    # sai fora...
                    break

            # otherwise, não achou a oposta ?
            else:
                # logger
                l_log = logging.getLogger("CAerNEW::calc_cab_oposta")
                l_log.setLevel(logging.WARNING)
                l_log.warning("pista:[{}/{}][{}] cabeceira oposta não encontrada.".format(lp_pst.ptr_pst_aer.s_aer_indc, lp_pst.s_pst_indc, ls_oposta))

    # ---------------------------------------------------------------------------------------------
    def copy_aer(self, f_aer):
        """
        copy constructor
        cria um novo aeródromo a partir de um outro aeródromo

        @param f_aer: aeródromo a ser copiado
        """
        # check input
        assert f_aer

        # copy super class attributes
        super(CAerNEW, self).copy_aer(f_aer)

        # latitude do ARP (gr)
        self.__f_aer_lat = f_aer.f_aer_lat
        # longitude do ARP (gr)
        self.__f_aer_lng = f_aer.f_aer_lng
                                
        # declinação magnética (gr)
        self.__f_aer_dcl_mag = f_aer.f_aer_dcl_mag

        # flag ok (bool)
        self.v_aer_ok = f_aer.v_aer_ok

    # ---------------------------------------------------------------------------------------------
    def load_aer(self, f_dct_data, fs_ver="0001"):
        """
        carrega os dados de um aeródromo a partir de um dicionário (formato 0001)

        @param f_dct_data: dicionário com os dados do aeródromo
        @param fs_ver: versão do formato dos dados
        """
        # formato versão 0.01 ?
        if "0001" == fs_ver:
            # cria a aeródromo
            self.make_aer(f_dct_data)

        # otherwise, formato desconhecido
        else:
            # logger
            l_log = logging.getLogger("CAerNEW::load_aer")
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
    def make_aer(self, fdct_data):
        """
        carrega os dados do aeródromo a partir de um dicionário (formato 0001)

        @param fdct_data: dicionário com os dados do aeródromo
        """
        # identificação do aeródromo
        if "nAer" in fdct_data:
            self.s_aer_indc = unicode(fdct_data["nAer"]).strip().upper()

        # descrição (nome)
        if "descricao" in fdct_data:
            self.s_aer_desc = unicode(fdct_data["descricao"]).strip()

        # declinação magnética (gr)
        if "declmag" in fdct_data:
            # declinação magnética em graus
            self.__f_aer_dcl_mag = float(fdct_data["declmag"])

        # elevação (m)
        if "elevacao" in fdct_data:
            # elevação (m)
            self.f_aer_elev = float(fdct_data["elevacao"]) * cdefs.D_CNV_FT2M

        # posição (lat, lng)
        if "coord" in fdct_data:
            self.__f_aer_lat, self.__f_aer_lng = self.__model.coords.from_dict(fdct_data["coord"])

        # pistas do aeródromo
        if "pistas" in fdct_data:
            # para todas pistas do aeródromo...
            for l_pst in fdct_data["pistas"]:
                # obtém a identificação da pista
                li_pst = l_pst.get("nPst", None)

                if li_pst is not None:
                    # cria pista
                    self.__dct_aer_pistas[li_pst] = pstnew.CPstNEW(self.__model, self, l_pst)
                    assert self.__dct_aer_pistas[li_pst]

                    # ajusta rumo magnético e verdadeiro
                    self.__dct_aer_pistas[li_pst].f_pst_true = self.__dct_aer_pistas[li_pst].f_pst_rumo + self.__f_aer_dcl_mag

                    # normaliza o rumo
                    if self.__dct_aer_pistas[li_pst].f_pst_true < 0.:   
                        self.__dct_aer_pistas[li_pst].f_pst_true += 360. 

                    elif self.__dct_aer_pistas[li_pst].f_pst_true > 360.:
                        self.__dct_aer_pistas[li_pst].f_pst_true -= 360.

            # calcula a cabeceira oposta de cada pista
            self.calc_cab_oposta()

        # (bool)
        self.v_aer_ok = True

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def f_aer_dcl_mag(self):
        """
        get declinação magnética
        """
        return self.__f_aer_dcl_mag

    @f_aer_dcl_mag.setter
    def f_aer_dcl_mag(self, f_val):
        """
        set declinação magnética
        """
        self.__f_aer_dcl_mag = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_aer_lat(self):
        """
        get latitude do ARP
        """
        return self.__f_aer_lat

    @f_aer_lat.setter
    def f_aer_lat(self, f_val):
        """
        set latitude do ARP
        """
        self.__f_aer_lat = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_aer_lng(self):
        """
        get longitude do ARP
        """
        return self.__f_aer_lng

    @f_aer_lng.setter
    def f_aer_lng(self, f_val):
        """
        set longitude do ARP
        """
        self.__f_aer_lng = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_aer_pistas(self):
        """
        pistas
        """
        return self.__dct_aer_pistas

# < the end >--------------------------------------------------------------------------------------
