#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
emula_model

the actual flight model

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import threading

# < class CEmulaModel >----------------------------------------------------------------------------

class CEmulaModel(threading.Thread):
    """
    the emula model class generates new flights and handles their movement. It has a list of
    flight objects holding all flights that are currently active
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_model, f_control):
        """
        constructor
        
        @param f_model: model
        @param f_control: control
        """
        # check input
        assert f_control
        assert f_model

        # init super class
        super(CEmulaModel, self).__init__()

        # control
        self.__control = f_control
        assert self.__control

        # model
        self.__model = f_model
        assert self.__model

        # initialize the dictionary for all active flights
        self.__dct_flight = {}

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def config(self):
        return self.__control.config

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_config(self):
        return self.__control.config.dct_config

    # ---------------------------------------------------------------------------------------------
    @property
    def control(self):
        return self.__control

    # ---------------------------------------------------------------------------------------------
    @property
    def event(self):
        return self.__control.event

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_flight(self):
        return self.__dct_flight

    # ---------------------------------------------------------------------------------------------
    @property
    def model(self):
        return self.__model

    # ---------------------------------------------------------------------------------------------
    '''
    @property
    def sim_time(self):
        return self._sim_time
    '''
# < the end >--------------------------------------------------------------------------------------
