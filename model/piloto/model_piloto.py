#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
model_piloto

model manager da pilotagem

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import os
import sys

# PyQt library
from PyQt4 import QtCore

# libs
import libs.coords.coord_sys as coords
import libs.geomag.geomag.geomag.geomag as gm

# model
import model.model_manager as model

import model.piloto.emula_piloto as emula
import model.newton.airspace_newton as airs

# control
# import control.events.events_basic as events
import control.common.glb_defs as gdefs

# < class CModelPiloto >---------------------------------------------------------------------------

class CModelPiloto(model.CModelManager):
    """
    piloto model object
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control):
        """
        constructor
        
        @param f_control: control manager
        """
        # check input
        assert f_control

        # init super class
        super(CModelPiloto, self).__init__(f_control)

        # herdados de CModelManager
        # self.app           # the application
        # self.control       # control manager
        # self.event         # event manager
        # self.config        # config manager
        # self.dct_config    # dicionário de configuração

        self.control.splash.showMessage("creating coordinate system...", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.white)
                
        # obtém as coordenadas de referência
        lf_ref_lat = float(self.dct_config["map.lat"])
        lf_ref_lng = float(self.dct_config["map.lng"])
        lf_dcl_mag = float(self.dct_config["map.dcl"])
                                                                
        self.control.splash.showMessage("loading cenary...", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.white)
        
        # coordinate system
        self.__coords = coords.CCoordSys(lf_ref_lat, lf_ref_lng, lf_dcl_mag)
        assert self.__coords

        # create magnectic converter
        self.__geomag = gm.GeoMag("data/tabs/WMM.COF")
        assert self.__geomag

        # variáveis de instância
        self.__airspace = None

        # dicionário de performances
        self.__dct_prf = {}
                
        # carrega o cenário (airspace & landscape)
        self.__load_cenario("SBSP")

        self.control.splash.showMessage("creating emulation model...", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.white)
                        
        # create emula model
        self.__emula = emula.CEmulaPiloto(self, f_control)
        assert self.__emula
                        
    # ---------------------------------------------------------------------------------------------
    def __load_air(self, fs_cena):
        """
        faz a carga do airspace

        @param fs_cena: cenário
        
        @return flag e mensagem
        """
        # obtém o diretório padrão de airspaces
        ls_dir = self.dct_config["dir.air"]

        # nome do diretório vazio ?
        if ls_dir is None:
            # diretório padrão de airspaces
            self.dct_config["dir.air"] = gdefs.D_DIR_AIR

            # diretório padrão de airspaces
            ls_dir = gdefs.D_DIR_AIR

        # expand user (~)
        ls_dir = os.path.expanduser(ls_dir)

        # create airspace
        self.__airspace = airs.CAirspaceNewton(self)
        assert self.__airspace

        # carrega os dicionários
        self.__airspace.load_dicts()

        # retorna ok
        return True, None

    # ---------------------------------------------------------------------------------------------
    def __load_cenario(self, fs_cena):
        """
        abre/cria as tabelas do sistema

        @param fs_cena: cenário
        
        @return flag e mensagem
        """
        # carrega o airspace
        lv_ok, ls_msg = self.__load_air(fs_cena)
                                                        
        # houve erro em alguma fase ?
        if not lv_ok:
            # logger
            l_log = logging.getLogger("CModelPiloto::__load_cenario")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: erro na carga da base de dados: {}.".format(ls_msg))

            # cria um evento de quit
            l_evt = event.CQuit()
            assert l_evt

            # dissemina o evento
            self.event.post(l_evt)

            # termina a aplicação
            sys.exit(1)

    # ---------------------------------------------------------------------------------------------
    def notify(self, f_evt):
        """
        callback de tratamento de eventos recebidos

        @param f_evt: evento recebido
        """
        # return
        return  
                
    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def airspace(self):
        return self.__airspace

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_apx(self):
        return self.__airspace.dct_apx

    # ---------------------------------------------------------------------------------------------
    @property
    def lst_arr_dep(self):
        return self.__airspace.lst_arr_dep

    # ---------------------------------------------------------------------------------------------
    @property
    def coords(self):
        return self.__coords
    '''
    @coords.setter
    def coords(self, f_val):
        self.__coords = f_val
    '''
    # ---------------------------------------------------------------------------------------------
    @property
    def emula(self):
        return self.__emula

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_esp(self):
        return self.__airspace.dct_esp

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_fix(self):
        return self.__airspace.dct_fix

    # ---------------------------------------------------------------------------------------------
    @property
    def geomag(self):
        return self.__geomag

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_prf(self):
        return self.__dct_prf

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_sub(self):
        return self.__airspace.dct_sub

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_trj(self):
        return self.__airspace.dct_trj

# < the end >--------------------------------------------------------------------------------------
