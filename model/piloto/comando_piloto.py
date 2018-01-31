#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
comando_piloto

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
        # self.t_param_1     # grau / velocidade / altitude / aeródromo
        # self.t_param_2     # proa / nivel / pista
        # self.t_param_3     # razão
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
        self.t_param_1 = (float(flst_tok[0]), True)

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
        self.t_param_1 = (str(llst_param[0]).strip(), True)

        # pista
        self.t_param_2 = (str(llst_param[1]).strip(), True)

    # ---------------------------------------------------------------------------------------------
    def __cmd_graus(self, flst_tok):
        """
        DOCUMENT ME!
        """
        # check input
        assert flst_tok
        
        # graus
        self.t_param_1 = (float(flst_tok[0]), True)

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
        self.t_param_2 = (float(flst_tok[0]), True)

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
        self.t_param_1 = (str(llst_param[0]).strip().upper(), True)

        # pista
        self.t_param_2 = (str(llst_param[1]).strip().upper(), True)

    # ---------------------------------------------------------------------------------------------
    def __cmd_proa(self, flst_tok):
        """
        DOCUMENT ME!
        """
        # check input
        assert flst_tok
        
        # proa
        self.t_param_2 = (float(flst_tok[0]), True)

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
        self.t_param_3 = (float(flst_tok[0]), True)

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

        # cancela ?
        elif "CNL" == llst_tok[0]:
            # comando
            self.en_cmd_ope = ldefs.E_CANCELA

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
            self.t_param_1 = (float(llst_tok[1]), True)

        # comando de direcionamento a fixo ?
        elif "FIX" == llst_tok[0]:
            # comando
            self.en_cmd_ope = ldefs.E_DIRFIXO

            # indicativo do fixo
            self.t_param_1 = (str(llst_tok[1]).strip(), True)

        # comando de nível ?
        elif "NIV" == llst_tok[0]:
            # parse command
            self.__cmd_nivel(llst_tok[1:])

        # comando de orbita ?
        elif "ORB" == llst_tok[0]:
            # comando
            self.en_cmd_ope = ldefs.E_ORBITA

            # latitude
            self.t_param_1 = (float(llst_tok[1]), True)

            # longitude
            self.t_param_2 = (float(llst_tok[2]), True)

        # comando de direcionamento a ponto ?
        elif "PTO" == llst_tok[0]:
            # comando
            self.en_cmd_ope = ldefs.E_DIRPNTO

            # latitude
            self.t_param_1 = (float(llst_tok[1]), True)

            # longitude
            self.t_param_2 = (float(llst_tok[2]), True)

        # comando de subida ?
        elif "SUB" == llst_tok[0]:
            # comando
            self.en_cmd_ope = ldefs.E_SUBIDA

            # subida
            self.t_param_1 = (float(llst_tok[1]), True)

        # comando de trajetória ?
        elif "TRJ" == llst_tok[0]:
            # comando
            self.en_cmd_ope = ldefs.E_TRAJETORIA

            # trajetória
            self.t_param_1 = (float(llst_tok[1]), True)

        # comando de velocidade ?
        elif "VEL" == llst_tok[0]:
            # comando
            self.en_cmd_ope = ldefs.E_IAS

            # velocidade
            self.t_param_1 = (float(llst_tok[1]), True)

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
