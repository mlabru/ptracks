#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
comando_piloto

DOCUMENT ME!

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

revision 0.2  2015/dez  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2016/01"

# < imports >--------------------------------------------------------------------------------------

# model
import model.newton.defs_newton as ldefs

import model.common.instruction as inst

# control
import control.control_debug as cdbg

# < class CComandoPil >----------------------------------------------------------------------------

class CComandoPil(inst.CInstruction):
    """
    DOCUMENT ME
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_msg=""):
        """
        constructor
        """
        # inicia a super classe
        super(CComandoPil, self).__init__()

        # herdados de CInstruction
        # self.en_cmd_ope    # comando
        # self.f_param_1     # grau / velocidade / altitude / aeródromo
        # self.f_param_2     # proa / nivel / pista
        # self.f_param_3     # razão
        # self.v_running     # flag em execução
        # self.s_text        # texto do comando

        # recebeu uma mensagem ?
        if "" != fs_msg:
            # salva o texto da mensagem
            self.s_text = fs_msg

            # parse mensagem
            self.__parse_comando(fs_msg)

    # ---------------------------------------------------------------------------------------------
    def __str__(self):
        """
        object's human-readable representation
        """
        # return super classe
        return super(CComandoPil, self).__str__()

    # ---------------------------------------------------------------------------------------------
    def __cmd_altitude(self, flst_tok):
        """
        DOCUMENT ME!
        """
        # check input
        assert flst_tok

        # comando
        self.en_cmd_ope = ldefs.E_ALT

        # altitude em pés(ft)
        self.f_param_1 = float(flst_tok[0])

        # possível razão ?
        if len(flst_tok) > 2:
            # parâmetro razão ?
            if "RAZ" == flst_tok[1]:
                # parse command
                self.__cmd_razao(flst_tok[2:])

    # ---------------------------------------------------------------------------------------------
    def __cmd_curva(self, flst_tok):
        """
        DOCUMENT ME!
        """
        # check input
        assert flst_tok

        # parâmetro direita ?
        if "DIR" == flst_tok[0]:
            # comando curva direita
            self.en_cmd_ope = ldefs.E_CDIR

        # parâmetro esquerda ?
        elif "ESQ" == flst_tok[0]:
            # comando curva esquerda
            self.en_cmd_ope = ldefs.E_CESQ

        # parâmetro menor ?
        elif "MNR" == flst_tok[0]:
            # comando curva esquerda
            self.en_cmd_ope = ldefs.E_CMNR

        # senão,...
        else:
            # comando curva menor
            self.en_cmd_ope = ldefs.E_CMNR

        # possível direção/razão ?
        if len(flst_tok) > 2:
            # parâmetro proa ?
            if "PROA" == flst_tok[1]:
                # parse proa
                self.__cmd_proa(flst_tok[2:])
            
            # parâmetro graus ?
            elif "GRAUS" == flst_tok[2]:
                # parse graus
                self.__cmd_graus(flst_tok[1:])
            
            # parâmetro razão ?
            elif "RAZ" == flst_tok[1]:
                # parse razão
                self.__cmd_razao(flst_tok[2:])

    # ---------------------------------------------------------------------------------------------
    def __cmd_decolagem(self, flst_tok):
        """
        DOCUMENT ME!
        """
        # check input
        assert flst_tok

        # comando
        self.en_cmd_ope = ldefs.E_DECOLAGEM

        # aeródromo/pista (AAAA/PPP)
        llst_param = flst_tok[0].split('/')

        # aeródromo
        self.f_param_1 = str(llst_param[0]).strip()  # .upper())

        # pista
        self.f_param_2 = str(llst_param[1]).strip()  # .upper())

    # ---------------------------------------------------------------------------------------------
    def __cmd_graus(self, flst_tok):
        """
        DOCUMENT ME!
        """
        # check input
        assert flst_tok
        
        # graus
        self.f_param_1 = float(flst_tok[0])

        # possível razão ?
        if len(flst_tok) > 3:
            # parâmetro razão ?
            if "RAZ" == flst_tok[2]:
                # parse command razão
                self.__cmd_razao(flst_tok[3:])

    # ---------------------------------------------------------------------------------------------
    def __cmd_nivel(self, flst_tok):
        """
        DOCUMENT ME!
        """
        # check input
        assert flst_tok
        
        # comando nível
        self.en_cmd_ope = ldefs.E_NIV

        # nível
        self.f_param_2 = float(flst_tok[0])

        # possível razão ?
        if len(flst_tok) > 2:
            # parâmetro razão ?
            if "RAZ" == flst_tok[1]:
                # parse command
                self.__cmd_razao(flst_tok[2:])

    # ---------------------------------------------------------------------------------------------
    def __cmd_pouso(self, flst_tok):
        """
        DOCUMENT ME!
        """
        # check input
        assert flst_tok

        # comando
        self.en_cmd_ope = ldefs.E_POUSO

        # aeródromo/pista (AAAA/PPP)
        llst_param = flst_tok[0].split('/')

        # aeródromo
        self.f_param_1 = str(llst_param[0]).strip().upper()

        # pista
        self.f_param_2 = str(llst_param[1]).strip().upper()

    # ---------------------------------------------------------------------------------------------
    def __cmd_proa(self, flst_tok):
        """
        DOCUMENT ME!
        """
        # check input
        assert flst_tok
        
        # proa
        self.f_param_2 = float(flst_tok[0])

        # possível razão ?
        if len(flst_tok) > 2:
            # parâmetro razão ?
            if "RAZ" == flst_tok[1]:
                # parse command razão
                self.__cmd_razao(flst_tok[2:])

    # ---------------------------------------------------------------------------------------------
    def __cmd_razao(self, flst_tok):
        """
        DOCUMENT ME!
        """
        # check input
        assert flst_tok
        
        # razão
        self.f_param_3 = float(flst_tok[0])

    # ---------------------------------------------------------------------------------------------
    def __parse_comando(self, fs_cmd=""):
        """
        DOCUMENT ME!
        """
        # recebeu um comando ?
        if "" == fs_cmd:
            # linha de comando vazia. cai fora...
            return

        # faz o split do comando
        llst_tok = fs_cmd.strip().split()
        cdbg.M_DBG.debug("__parse_comando: llst_tok: {}".format(llst_tok))

        # comando de altitude ?
        if "ALT" == llst_tok[0]:
            # parse command
            self.__cmd_altitude(llst_tok[1:])

        # pouso ?
        elif "ARR" == llst_tok[0]:
            # parse command
            self.__cmd_pouso(llst_tok[1:])

        # comando de curva ?
        elif "CURVA" == llst_tok[0]:
            # parse command
            self.__cmd_curva(llst_tok[1:])

        # decolagem ?
        elif "DEP" == llst_tok[0]:
            # parse command
            self.__cmd_decolagem(llst_tok[1:])

        # comando de espera ?
        elif "ESP" == llst_tok[0]:
            # comando
            self.en_cmd_ope = ldefs.E_ESPERA

            # espera
            self.f_param_1 = float(llst_tok[1])

        # comando de direcionamento a fixo ?
        elif "FIX" == llst_tok[0]:
            # comando
            self.en_cmd_ope = ldefs.E_DIRFIXO

            # número do fixo
            self.f_param_1 = str(llst_tok[1]).strip()

        # comando de nível ?
        elif "NIV" == llst_tok[0]:
            # parse command
            self.__cmd_nivel(llst_tok[1:])

        # comando de subida ?
        elif "SUB" == llst_tok[0]:
            # comando
            self.en_cmd_ope = ldefs.E_SUBIDA

            # subida
            self.f_param_1 = float(llst_tok[1])

        # comando de trajetória ?
        elif "TRJ" == llst_tok[0]:
            # comando
            self.en_cmd_ope = ldefs.E_TRAJETORIA

            # trajetória
            self.f_param_1 = float(llst_tok[1])

        # comando de velocidade ?
        elif "VEL" == llst_tok[0]:
            # comando
            self.en_cmd_ope = ldefs.E_IAS

            # velocidade
            self.f_param_1 = float(llst_tok[1])

    # =============================================================================================
    # data
    # =============================================================================================
            
    # ---------------------------------------------------------------------------------------------
    '''                
    @property
    def en_cmd_ope(self):
        """
        get comando operacional
        """
        return self.__en_cmd_ope
                                                        
    @en_cmd_ope.setter
    def en_cmd_ope(self, f_val):
        """
        set comando operacional
        """
        self.__en_cmd_ope = f_val
    '''                                                        
# < the end >--------------------------------------------------------------------------------------
