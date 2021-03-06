#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
model_dbedit

model manager do editor da base de dados

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
import os
import sys

# PyQt library
from PyQt4 import QtCore

# libs
import libs.coords.coord_sys as coords

# model
import model.model_manager as model
import model.newton.airspace_newton as airs

import model.items.aer_data as aerdata
import model.items.exe_data as exedata
import model.items.fix_data as fixdata
import model.items.prf_data as prfdata
# import model.items.sen_data as sendata
import model.items.trf_data as trfdata
import model.items.trj_data as trjdata

# control
import control.control_debug as cdbg
import control.events.events_basic as events
import control.events.events_config as evtConfig

# < class CModelDBEdit >---------------------------------------------------------------------------

class CModelDBEdit(model.CModelManager):
    """
    DBEdit model object. Views and controllers interact with this
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
        super(CModelDBEdit, self).__init__(f_control)

        # herdados de CModelManager
        # self.app           # the application
        # self.config        # config manager
        # self.dct_config    # dicionário de configuração
        # self.control       # control manager
        # self.event         # event manager

        # show message
        self.control.splash.showMessage("creating coordinate system...", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.white)
        
        # obtém as coordenadas de referência
        lf_ref_lat = float(self.dct_config["map.lat"])
        lf_ref_lng = float(self.dct_config["map.lng"])
        lf_dcl_mag = float(self.dct_config["map.dcl"])
                                
        # coordinate system
        self.__coords = coords.CCoordSys(lf_ref_lat, lf_ref_lng, lf_dcl_mag)
        assert self.__coords
                                                        
        # airspace
        self.__airspace = None

        # exercício
        self.__exe = None

        # dicionário de exercícios
        self.__dct_exe = {}

        # dicionário de performances
        self.__dct_prf = {}

        # dicionário de sensores
        # self.__dct_sns = {}

        # dicionário de tráfegos
        self.__dct_trf = {}

        # carrega as tabelas do sistema
        self.__load_cenario()

        # carrega os exercicios do sistema
        self.__load_exes()

    # ---------------------------------------------------------------------------------------------
    def get_ptr_prc(self, fs_prc):
        """
        DOCUMENT ME!
        """
        return None, 0

    # ---------------------------------------------------------------------------------------------
    def __load_airs(self):
        """
        faz a carga do airspace

        @return flag e mensagem
        """
        # show message
        self.control.splash.showMessage("loading airspace...", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.white)

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

        # diretório não existe ?
        if not os.path.exists(ls_dir):
            # cria o diretório
            os.mkdir(ls_dir)

        # create airspace (aeródomos, fixos, pistas, pousos e decolagens)
        self.__airspace = airs.CAirspaceNewton(self)
        assert self.__airspace

        # carrega os dicionários (aproximações, esperas, subidas e trajetórias)
        self.__airspace.load_dicts()

        # retorna ok
        return True, None

    # ---------------------------------------------------------------------------------------------
    def __load_cenario(self):
        """
        faz a carga das tabelas do sistema (airspace & landscape)

        @return flag e mensagem
        """
        # show message
        self.control.splash.showMessage("loading cenary...", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.white)

        # carrega o landscape
        # lv_ok, ls_msg = self.__load_land()
                
        # tudo Ok ?
        # if lv_ok:

        # carrega o airspace
        lv_ok, ls_msg = self.__load_airs()

        # ok ?
        if lv_ok:
            # carrega as tabelas do sistema
            lv_ok, ls_msg = self.__load_tables()

        # houve erro em alguma fase ?
        if not lv_ok:
            # logger
            l_log = logging.getLogger("CModelDBEdit::__load_cenario")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: erro na carga da base de dados: {}".format(ls_msg))

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self._event.post(l_evt)

            # termina a aplicação
            sys.exit(1)

    # ---------------------------------------------------------------------------------------------
    def __load_tables(self):
        """
        abre/cria as tabelas do sistema

        @return flag e mensagem
        """
        # show message
        self.control.splash.showMessage("loading tables...", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.white)

        # monta o nome da tabela de performances
        ls_path = os.path.join(self.dct_config["dir.tab"], self.dct_config["tab.prf"])

        # carrega a tabela de performance em um dicionário
        self.__dct_prf = prfdata.CPrfData(self, ls_path)
        assert self.__dct_prf is not None
        '''
        # monta o nome do arquivo de exercício
        ls_path = os.path.join(self.dct_config["dir.exe"], self.dct_config["glb.exe"])

        # carrega o exercício em um dicionário
        ldct_exe = exedata.CExeData(self, ls_path)
        assert ldct_exe is not None

        # obtém o exercício
        self.__exe = ldct_exe[self.dct_config["glb.exe"]]
        assert self.__exe

        cdbg.M_DBG.debug("Exercicio default: {}".format(self.__exe))

        # monta o nome do arquivo de tráfegos
        ls_path = os.path.join(self.dct_config["dir.trf"], self.dct_config["glb.exe"])

        # carrega a tabela de tráfegos do exercício
        self.__dct_trf = trfdata.CTrfData(self, ls_path, self.__exe)
        assert self.__dct_trf is not None

        # coloca a tabela de tráfegos no exercício
        self.__exe.dct_exe_trf = self.__dct_trf

        cdbg.M_DBG.debug("tráfegos do exercício: {}".format(self.__exe.dct_exe_trf))
        '''
        # retorna
        return True, None

    # ---------------------------------------------------------------------------------------------
    def __load_exes(self):
        """
        faz a carga da tabela de exercícios
        """
        # obtém o diretório padrão de exercícios
        ls_dir = self.dct_config["dir.exe"]

        # nome do diretório vazio ?
        if ls_dir is None:
            # diretório padrão de tabelas
            ls_dir = self.dct_config["dir.exe"] = "exes"

        # diretório não existe ?
        if not os.path.exists(ls_dir):
            # cria o diretório
            os.mkdir(ls_dir)

        # percorre o diretório
        for ls_file in os.listdir(ls_dir):
            # monta o path completo do arquivo de exercício
            ls_path = os.path.join(ls_dir, ls_file)

            # não é um arquivo ?
            if not os.path.isfile(ls_path):
                # passa ao próximo
                continue

            # split name and extension
            ls_name, l_fext = os.path.splitext(ls_file)

            # não é um arquivo XML ?
            if ".xml" != l_fext:
                # passa ao próximo
                continue

            # split name and extension
            ls_name, l_fext = os.path.splitext(ls_name)

            # não é um arquivo de exercício ?
            if ".exe" != l_fext:
                # passa ao próximo
                continue

            cdbg.M_DBG.debug("filename: {}".format(os.path.join(ls_dir, ls_name)))

            # cria um dicionário de exercícios
            ldct_exe = exedata.CExeData(self, os.path.join(ls_dir, ls_name))

            if ldct_exe is None:
                # logger
                l_log = logging.getLogger("CModelDBEdit::__load_exes")
                l_log.setLevel(logging.WARNING)
                l_log.warning("<E01: tabela de exercícios: {} não existe.".format(ls_path))

                # cai fora...
                return False

            # carrega os tráfegos do exercício
            ls_exe_key = ldct_exe.keys()[0]

            # atualiza o exercicio corrente
            self.__exe = ldct_exe[ls_exe_key]

            # carrega os tráfegos do exercício
            ldct_trf = self.__load_trafs(ls_exe_key, ldct_exe)

            cdbg.M_DBG.debug("dicionario de tráfegos: {}".format(ldct_trf))

            if ldct_trf:
                # obtém o exercício
                l_exe = ldct_exe[ls_exe_key]

                # coloca a tabela de tráfegos no exercício
                l_exe.dct_exe_trf = ldct_trf

                # coloca o exercício no dicionário
                ldct_exe[ls_exe_key] = l_exe

            # salva no dicionário
            self.__dct_exe.update(ldct_exe)

        # retorna
        return True

    # ---------------------------------------------------------------------------------------------
    def __load_trafs(self, fs_exe, fdct_exe):
        """
        faz a carga da tabela de tráfegos de um exercício
        """
        # obtém o diretório padrão tráfegos do exercício
        ls_dir = self.dct_config["dir.trf"]

        # nome do diretório vazio ?
        if ls_dir is None:
            # diretório padrão de tabelas
            ls_dir = self.dct_config["dir.trf"] = "traf"

        # diretório não existe ?
        if not os.path.exists(ls_dir):
            # cria o diretório
            os.mkdir(ls_dir)

        # monta o path completo do arquivo de tráfego do exercício
        ls_path = os.path.join(ls_dir, fs_exe)

        cdbg.M_DBG.debug("Carregando tráfegos do exercicio: {}".format(ls_path))

        # carrega a tabela de tráfegos do exercício
        ldct_trf = trfdata.CTrfData(self, ls_path, fdct_exe)
        assert ldct_trf is not None

        # retorna
        return ldct_trf

    # ---------------------------------------------------------------------------------------------
    def notify(self, f_event):
        """
        callback de tratamento de eventos recebidos

        @param f_event: evento recebido
        """
        # recebeu um evento de "config exe" ?
        if isinstance(f_event, evtConfig.CConfigExe):
            # atualiza o exercicio corrente
            cdbg.M_DBG.debug("exercicio corrente: {}".format(f_event.s_exe))

            self.__exe = self.__dct_exe.get(f_event.s_exe, None)

            if self.__exe is None:
                l_log = logging.getLogger("CModelDBEdit::notify")
                l_log.setLevel(logging.WARNING)
                l_log.warning(u"<E01: exercício {} não existe no dicionário.".format(f_event.s_exe))

        # recebeu um evento de "save to disk" ?
        if isinstance(f_event, events.CSave2Disk):
            # salvar tabela de aeródromos ?
            if "AER" == f_event.s_table.upper():
                # salva a tabela de aeródromos
                self.dct_aer.save2disk()

            # salvar tabela de fixos ?
            elif "FIX" == f_event.s_table.upper():
                # salva a tabela de fixos
                self.dct_fix.save2disk()

            # salvar tabela de performances ?
            elif "PRF" == f_event.s_table.upper():
                # salva a tabela de performances
                self.__dct_prf.save2disk()

            # salvar tabela de exercícios ?
            elif "EXE" == f_event.s_table.upper():
                ls_exe_path = self.dct_config["dir.exe"]
                cdbg.M_DBG.debug("CSave2Disk dir EXE [%s]" % ls_exe_path)

                # salva as tabela de exercícios
                for l_key, l_exe in self.__dct_exe.items():
                    l_exe.save2disk(fs_exe_path=ls_exe_path)

            # salvar tabela de tráfegos ?
            elif "ANV" == f_event.s_table.upper():
                # salva a tabela de tráfegos
                cdbg.M_DBG.debug(" Exercicio atual [%s]" % self.__exe.s_exe_id)
                ls_trf_path = self.dct_config["dir.trf"]
                cdbg.M_DBG.debug(" CSave2Disk dir ANV [%s]" % ls_trf_path)
                l_oTrfData = trfdata.CTrfData(self, f_exe=self.__exe)

                l_oTrfData.save2disk(ls_trf_path)

            # salvar tabela de trajetórias ?
            elif "TRJ" == f_event.s_table.upper():
                # salva a tabela de trajetórias
                cdbg.M_DBG.debug("Salvar a tabela de trajetórias no disco.")
                # monta o nome da tabela de procedimentos de trajetória
                ls_trj_path = os.path.join(self.dct_config["dir.prc"], self.dct_config["tab.trj"])
                l_oTrjData = trjdata.CTrjData(self)
                l_oTrjData.save2disk(ls_trj_path)

            '''
            # salvar tabela de esperas ?
            elif "ESP" == f_event.table.upper():
                # salva a tabela de esperas
                self.dct_esp.save2disk()

            # salvar tabela de figuras ?
            elif "FIG" == f_event.table.upper():
                # salva a tabela de figuras
                self.dct_fig.save2disk()

            # salvar tabela de navegações ?
            elif "NAV" == f_event.table.upper():
                # salva a tabela de navegações
                self.dct_Nav.save2disk()

            # salvar tabela de pontos no solo ?
            elif "PNS" == f_event.table.upper():
                # salva a tabela de pontos no solo
                self.dct_pNS.save2disk()

            # salvar tabela de procedimentos ?
            elif "PRC" == f_event.table.upper():
                # salva a tabela de procedimentos
                self.dct_prc.save2disk()

            # salvar tabela de pistas ?
            elif "PST" == f_event.table.upper():
                # salva a tabela de pistas
                self.dct_pst.save2disk()

            # salvar tabela de trajetórias ?
            elif "TRJ" == f_event.table.upper():
                # salva a tabela de trajetórias
                self.__dct_trj.save2disk()
        '''

        # recebeu um evento de "update from disk" ?
        if isinstance(f_event, events.CUpd2Disk):
            # salvar tabela de aeródromos ?
            if "AER" == f_event.s_table.upper():
                # salva a tabela de aeródromos
                self.dct_aer.save2disk()

            # salvar tabela de fixos ?
            elif "FIX" == f_event.s_table.upper():
                # salva a tabela de fixos
                self.dct_fix.save2disk()

            # salvar tabela de performances ?
            elif "PRF" == f_event.s_table.upper():
                # salva a tabela de performances
                self.__dct_prf.save2disk()

            # salvar tabela de exercícios ?
            elif "EXE" == f_event.s_table.upper():
                # remove a tabela de exercício
                l_oExeNew = self.__dct_exe[f_event.s_filename]
                ls_exe_path = self.dct_config["dir.exe"]
                cdbg.M_DBG.debug(" CUpd2Disk exe path [%s]" % ls_exe_path)
                l_oExeNew.save2disk(fs_exe_path=ls_exe_path)

            # salvar tabela de tráfegos ?
            elif "ANV" == f_event.s_table.upper():
                # salva a tabela de tráfegos
                cdbg.M_DBG.debug(" Exercicio atual [%s]" % self.__exe.s_exe_id)
                ls_trf_path = self.dct_config["dir.trf"]
                cdbg.M_DBG.debug(" CSave2Disk dir ANV [%s]" % ls_trf_path)
                l_oTrfData = trfdata.CTrfData(self, f_exe=self.__exe)

                l_oTrfData.save2disk(ls_trf_path)

        # recebeu um evento de "delete from disk" ?
        if isinstance(f_event, events.CDelFromDisk):
            # excluir tabela de aeródromos ?
            if "AER" == f_event.s_table.upper():
                # salva a tabela de aeródromos
                self.dct_aer.del_from_disk()

            # excluir tabela de fixos ?
            elif "FIX" == f_event.s_table.upper():
                # salva a tabela de fixos
                self.dct_fix.del_from_disk()

            # excluir tabela de performances ?
            elif "PRF" == f_event.s_table.upper():
                # salva a tabela de performances
                self.__dct_prf.del_from_disk()

            # excluir tabela de exercícios ?
            elif "EXE" == f_event.s_table.upper():
                # remove a tabela de exercício
                l_oExeNew = self.__dct_exe[f_event.s_filename]
                ls_exe_path = self.dct_config["dir.exe"] + "/" + f_event.s_filename + ".exe.xml"
                cdbg.M_DBG.debug(" CDelFromDisk filename [%s]" % ls_exe_path)
                l_oExeNew.del_from_disk(fs_exe_path=ls_exe_path)

                # remove o exercicio do dicionario de exercicios
                del self.__dct_exe[f_event.s_filename]

            # excluir tabela de tráfegos ?
            elif "ANV" == f_event.s_table.upper():
                # remove a tabela de tráfegos do exercício
                ls_trf_path = self.dct_config["dir.trf"] + "/" + f_event.s_filename + ".trf.xml"
                cdbg.M_DBG.debug(" CDelFromDisk filename [%s]" % ls_trf_path)
                l_oTrfData = trfdata.CTrfData(self, f_exe=self.__exe)

                # remove o arquivo de tráfegos do exercicio
                l_oTrfData.del_from_disk(ls_trf_path)

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_aer(self):
        """
        dicionário de aeródromos
        """
        return self.__airspace.dct_aer

    # ---------------------------------------------------------------------------------------------
    @property
    def airspace(self):
        """
        get airspace
        """
        return self.__airspace

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_apx(self):
        """
        dicionário de aproximações
        """
        return self.__airspace.dct_apx

    # ---------------------------------------------------------------------------------------------
    @property
    def coords(self):
        """
        get coordinate system
        """
        return self.__coords

    @coords.setter
    def coords(self, f_val):
        """
        set coordinate system
        """
        self.__coords = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def exe(self):
        """
        get exercício
        """
        return self.__exe

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_esp(self):
        """
        get esperas
        """
        return self.__airspace.dct_esp

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_exe(self):
        """
        dicionário de exercícios
        """
        return self.__dct_exe

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_fix(self):
        """
        dicionário de fixos
        """
        return self.__airspace.dct_fix

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_prf(self):
        """
        get performances
        """
        return self.__dct_prf

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_sen(self):
        """
        dicionário de sensores
        """
        return self.__dct_sen

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_sub(self):
        """
        get subidas
        """
        return self.__airspace.dct_sub

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_trf(self):
        """
        get tráfegos
        """
        return self.__dct_trf

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_trj(self):
        """
        get trajetórias
        """
        return self.__airspace.dct_trj

# < the end >--------------------------------------------------------------------------------------
