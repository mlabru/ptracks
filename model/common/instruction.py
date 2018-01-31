#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
instruction

an instruction

revision 0.2  2015/dez  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2016/01"

# < class CInstruction >---------------------------------------------------------------------------

class CInstruction(object):
    """
    class CInstruction
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """ 
        # inicia a super classe
        super(CInstruction, self).__init__()

        # comando
        self.__en_cmd_ope = 0

        # parâmetros

        # grau / velocidade / altitude & flag Ok
        self.__t_param_1 = (0., False)
        # proa / nivel & flag Ok
        self.__t_param_2 = (0., False)
        # razão & flag Ok
        self.__t_param_3 = (0., False)

        # texto da instrução
        self.__s_text = ""
 
        # em execução
        self.__v_running = False

        # self.__i_type = 0
        # self.__f_number = 0.
        # self.__o_react_time = None

    # ---------------------------------------------------------------------------------------------
    def __str__(self):
        """
        object's human-readable representation
        """
        # return
        return "text:[{}] = {}/{}/{}/{}".format(self.__s_text, self.__en_cmd_ope, self.__t_param_1,
                                                self.__t_param_2, self.__t_param_3)

    # =============================================================================================
    # data
    # =============================================================================================
            
    # ---------------------------------------------------------------------------------------------
    @property
    def en_cmd_ope(self):
        return self.__en_cmd_ope
                                                        
    @en_cmd_ope.setter
    def en_cmd_ope(self, f_val):
        self.__en_cmd_ope = f_val
                                                        
    # ---------------------------------------------------------------------------------------------
    @property
    def t_param_1(self):
        return self.__t_param_1
                                                        
    @t_param_1.setter
    def t_param_1(self, f_val):
        self.__t_param_1 = f_val
                                                        
    # ---------------------------------------------------------------------------------------------
    @property
    def t_param_2(self):
        return self.__t_param_2
                                                        
    @t_param_2.setter
    def t_param_2(self, f_val):
        self.__t_param_2 = f_val
                                                        
    # ---------------------------------------------------------------------------------------------
    @property
    def t_param_3(self):
        return self.__t_param_3
                                                        
    @t_param_3.setter
    def t_param_3(self, f_val):
        self.__t_param_3 = f_val
                                                        
    # ---------------------------------------------------------------------------------------------
    @property
    def v_running(self):
        return self.__v_running
                                                        
    @v_running.setter
    def v_running(self, f_val):
        self.__v_running = f_val
                                                        
    # ---------------------------------------------------------------------------------------------
    @property
    def s_text(self):
        return self.__s_text
                                                        
    @s_text.setter
    def s_text(self, f_val):
        self.__s_text = f_val
                                                        
# < the end >--------------------------------------------------------------------------------------
