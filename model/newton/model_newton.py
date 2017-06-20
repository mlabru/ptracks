#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
model_newton

newton model

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
import os.path

# libs
import libs.coords.coord_sys as coords

# model
import model.model_manager as model

import model.newton.emula_newton as emula

#import model.items.aer_data as aerdata
import model.items.exe_data as exedata
#import model.items.fix_data as fixdata
import model.items.prf_data as prfdata
import model.items.trf_data as trfdata

import model.newton.airspace_newton as airs
import model.newton.defs_newton as ldefs

# < class CModelNewton >----------------------------------------------------------------------------

class CModelNewton(model.CModelManager):
    """
    newton model
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control):
        """
        @param f_control: control
        """
        # check input
        assert f_control
        
        # init super class
        super(CModelNewton, self).__init__(f_control)
 
        # herdados de CModelManager
        # self.app           # application
        # self.config        # config
        # self.dct_config    # dicionário de configuração
        # self.control       # control
        # self.event         # event

        # obtém as coordenadas de referência
        lf_ref_lat = float(self.dct_config["map.lat"])
        lf_ref_lng = float(self.dct_config["map.lng"])
        lf_dcl_mag = float(self.dct_config["map.dcl"])
                                
        # coordinate system
        self.__coords = coords.CCoordSys(lf_ref_lat, lf_ref_lng, lf_dcl_mag)
        assert self.__coords
                                                        
        # airspace
        self.__airspace = None

        # dicionário de performances
        self.__dct_prf = {}

        # dicionário de tráfegos
        self.__dct_trf = {}

        # exercício
        self.__exe = None

        # carrega o cenário de simulação (airspace & landscape)
        self.__load_cenario()

        # carrega as tabelas (base de dados)
        self.__load_dicts()

        # create flight emulation model
        self.__emula = emula.CEmulaNewton(self, f_control)
        assert self.__emula

        # set as daemon
        self.__emula.daemon = True

    # ---------------------------------------------------------------------------------------------
    def __load_air(self):
        """
        faz a carga do airspace

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

        # carrega as tabelas do sistema
        self.__airspace.load_dicts()

        # retorna ok
        return True, None

    # ---------------------------------------------------------------------------------------------
    def __load_cenario(self):
        """
        abre/cria as tabelas do sistema

        @return flag e mensagem
        """
        # carrega o airspace
        lv_ok, ls_msg = self.__load_air()

        # houve erro em alguma fase ?
        if not lv_ok:
            # logger
            l_log = logging.getLogger("CModelNewton::__load_cenario")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: erro na carga da base de dados [{}].".format(ls_msg))

            # cria um evento de quit
            l_evt = event.CQuit()
            assert l_evt

            # dissemina o evento
            self.event.post(l_evt)

            # termina a aplicação
            sys.exit(1)

    # ---------------------------------------------------------------------------------------------
    def __load_dicts(self):
        """
        carrega as tabelas do sistema
        """
        # monta o nome da tabela de performances
        ls_path = os.path.join(self.dct_config["dir.tab"], self.dct_config["tab.prf"])

        # carrega a tabela de performance em um dicionário
        self.__dct_prf = prfdata.CPrfData(self, ls_path)
        assert self.__dct_prf is not None

        # monta o nome do arquivo de exercício
        ls_path = os.path.join(self.dct_config["dir.exe"], self.dct_config["glb.exe"])

        # carrega o exercício em um dicionário
        ldct_exe = exedata.CExeData(self, ls_path + ".exe.xml")
        assert ldct_exe is not None

        # obtém o exercício
        self.__exe = ldct_exe[self.dct_config["glb.exe"]]
        assert self.__exe

        # monta o nome do arquivo de tráfegos
        ls_path = os.path.join(self.dct_config["dir.trf"], self.dct_config["glb.exe"])

        # carrega a tabela de tráfegos do exercício
        self.__dct_trf = trfdata.CTrfData(self, ls_path, self.__exe)
        assert self.__dct_trf is not None

        # coloca a tabela de tráfegos no exercício
        self.__exe.dct_exe_trf = self.__dct_trf

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def airspace(self):
        return self.__airspace

    # ---------------------------------------------------------------------------------------------
    @property
    def coords(self):
        return self.__coords

    @coords.setter
    def coords(self, f_val):
        self.__coords = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def emula(self):
        return self.__emula

    # ---------------------------------------------------------------------------------------------
    @property
    def exe(self):
        return self.__exe

    # ---------------------------------------------------------------------------------------------
    @property
    def lst_arr_dep(self):
        return self.__airspace.lst_arr_dep

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
    def dct_prf(self):
        return self.__dct_prf

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_sub(self):
        return self.__airspace.dct_sub

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_trf(self):
        return self.__dct_trf

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_trj(self):
        return self.__airspace.dct_trj

# < the end >--------------------------------------------------------------------------------------
