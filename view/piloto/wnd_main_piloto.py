#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wnd_main_piloto

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

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2015/fev  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2015/12"

# < imports >--------------------------------------------------------------------------------------

# Python library
import datetime
import json
import logging
import random
import sys
import time

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

# model
import model.common.glb_data as gdata
import model.common.defs_strips as ldefs
# import model.common.strip_model as mstp
import model.common.strip_table_model as stm

import model.visil.aircraft_visil as anv

# view
import view.common.dock_procedures as dckprc
import view.common.slate_radar as sltrdr
# import view.common.strip_basic as strips

import view.piloto.statusbar_piloto as statusbar
import view.piloto.wnd_main_piloto_ui as wndmain_ui

import view.piloto.dlg_altitude as dlgalt
import view.piloto.dlg_aproximacao as dlgapx
import view.piloto.dlg_decolagem as dlgdep
import view.piloto.dlg_direcao as dlgdir
import view.piloto.dlg_dir_fixo as dlgfix
import view.piloto.dlg_espera as dlgesp
import view.piloto.dlg_pouso as dlgarr
import view.piloto.dlg_subida as dlgsub
import view.piloto.dlg_trajetoria as dlgtrj
import view.piloto.dlg_velocidade as dlgvel

# control
import control.control_debug as cdbg
import control.common.glb_defs as gdefs

import control.events.events_basic as events
import control.events.events_config as evtcfg

# resources
import view.resources.resources_rc

# < class CWndMainPiloto >---------------------------------------------------------------------------

class CWndMainPiloto(QtGui.QMainWindow, wndmain_ui.Ui_wndMainPiloto):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    # signals
    # C_SIG_STRIP_CHG = QtCore.pyqtSignal(anv.CAircraftVisil)
    # C_SIG_STRIP_DEL = QtCore.pyqtSignal(anv.CAircraftVisil)
    C_SIG_STRIP_INS = QtCore.pyqtSignal(anv.CAircraftVisil)
    C_SIG_STRIP_SEL = QtCore.pyqtSignal(anv.CAircraftVisil)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control):
        """
        constructor

        @param f_control: control manager
        """
        # check input
        assert f_control

        # inicia a super classe
        super(CWndMainPiloto, self).__init__()

        # control manager
        self.__control = f_control
        assert self.__control

        # dicionário de aproximações
        self.__dct_apx = f_control.model.dct_apx
        assert self.__dct_apx is not None

        # lista de pousos
        self.__lst_arr = f_control.model.lst_arr_dep
        assert self.__lst_arr is not None

        # lista de decolagens
        self.__lst_dep = f_control.model.lst_arr_dep
        assert self.__lst_dep is not None

        # dicionário de esperas
        self.__dct_esp = f_control.model.dct_esp
        assert self.__dct_esp is not None

        # dicionário de fixos
        self.__dct_fix = f_control.model.dct_fix
        assert self.__dct_fix is not None

        # dicionário de performances
        self.__dct_prf = f_control.model.dct_prf
        assert self.__dct_prf is not None

        # dicionário de subidas
        self.__dct_sub = f_control.model.dct_sub
        assert self.__dct_sub is not None

        # dicionário de trajetórias
        self.__dct_trj = f_control.model.dct_trj
        assert self.__dct_trj is not None

        # airspace
        self.__airspace = f_control.model.airspace

        # dicionário de aeronaves
        self.__dct_flight = f_control.model.emula.dct_flight
        assert self.__dct_flight is not None

        # dicionário de configuração
        self.__dct_config = f_control.config.dct_config
        assert self.__dct_config

        # socket de envio
        self.__sck_snd_cpil = f_control.sck_snd_cpil
        assert self.__sck_snd_cpil

        # socket de recebimento
        self.__sck_http = f_control.sck_http
        assert self.__sck_http

        # event manager
        self.__event = f_control.event
        assert self.__event

        # init color dictionary
        gdata.G_DCT_COLORS = {}

        # load color dictionary
        for l_key, l_val in f_control.view.colors.c_dct_color.iteritems():
            gdata.G_DCT_COLORS[l_key] = QtGui.QColor(l_val[1][0], l_val[1][1], l_val[1][2])

        # current strip
        self.__strip_cur = None

        # create main menu Ui
        self.setupUi(self)

        # config dock
        self.dck_lista_voos.setMinimumSize(QtCore.QSize(620, 600))

        # window title
        self.setWindowTitle(self.tr("Piloto 0.1 [Pilotagem]", None))

        # the slate radar is the main widget
        self.__slate_radar = sltrdr.CSlateRadar(f_control, self)
        assert self.__slate_radar
                        
        # the radar screen goes to central widget
        self.setCentralWidget(self.__slate_radar)

        # create status bar
        self.status_bar = statusbar.CStatusBarPiloto(self)
        assert self.status_bar

        # config statusBar
        self.setStatusBar(self.status_bar)

        # create windows elements
        self.__config_strips()

        # create windows elements
        self.__config_buttons()

        self.__create_actions()
        # self.createDocks()
        # self.createMenus()
        self.__create_toolbars()
        self.__config_toolboxes()

        # make SIGNAL-SLOT connections
        self.__make_connections()

        # read saved settings
        self.__read_settings()

        # registro para receber eventos
        self.__event.register_listener(self)

        # strips
        # self.e_strips()

        # fetch aircrafts data timer (1s cycle)
        self.__i_timer_fetch = self.startTimer(1000)

        # fetch status data timer (2s cycle)
        self.__i_timer_status = self.startTimer(2000)

        # config tableview
        self.qtv_stp.setFocus()
        self.qtv_stp.setCurrentIndex(self.__stp_model.index(0, 0))

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def about(self):
        """
        DOCUMENT ME!
        """
        # show about box
        QtGui.QMessageBox.about(self, self.tr("About Piloto", None),
                                      self.tr("Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
                                              "Duis in feugiat odio. Vestibulum ante ipsum primis in faucibus \n"
                                              "orci luctus et ultrices posuere cubilia Curae; Donec at venenatis magna.\n"
                                              "Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
                                              "Ut tempor felis ut orci interdum egestas. In vestibulum dolor ipsum.\n"
                                              "\n", None))

    # ---------------------------------------------------------------------------------------------
    # @QtCore.pyqtSlot()
    def closeEvent(self, f_evt):
        """
        DOCUMENT ME!
        """
        # really quit ?
        if self.__really_quit():
            # save actual config
            self.__write_settings()

            # accept
            f_evt.accept()

            # create CQuit event
            l_evt = events.CQuit()
            assert l_evt

            # dispatch event
            self.__event.post(l_evt)

        # otherwise, continua...
        else:
            # ignore
            f_evt.ignore()

    # ---------------------------------------------------------------------------------------------
    def __config_buttons(self):
        """
        DOCUMENT ME!
        """
        ###
        # buttons

        # nenhuma aeronave selecionada ?
        if self.__strip_cur is None:
            # disable all buttons
            self.btn_cancela.setEnabled(False)

            self.btn_cmd_altitude.setEnabled(False)
            self.btn_cmd_direcao.setEnabled(False)
            self.btn_cmd_velocidade.setEnabled(False)

            self.btn_prc_ape.setEnabled(False)
            self.btn_prc_apx.setEnabled(False)
            self.btn_prc_arr.setEnabled(False)
            self.btn_prc_dep.setEnabled(False)
            self.btn_prc_dir_fixo.setEnabled(False)
            self.btn_prc_esp.setEnabled(False)
            self.btn_prc_ils.setEnabled(False)
            # self.btn_prc_sub.setEnabled(False)
            self.btn_prc_trj.setEnabled(False)

            self.btn_cod_emg.setEnabled(False)
            self.btn_cod_spi.setEnabled(False)
            self.btn_cod_ssr.setEnabled(False)

        # senão, tem aeronave selecionada
        else:
            # enable buttons
            self.btn_cancela.setEnabled(False)

            self.btn_cmd_altitude.setEnabled(True)
            self.btn_cmd_direcao.setEnabled(True)
            self.btn_cmd_velocidade.setEnabled(True)

            self.btn_prc_ape.setEnabled(False)
            self.btn_prc_apx.setEnabled(True)
            self.btn_prc_arr.setEnabled(self.__strip_cur.f_alt > 0.)
            self.btn_prc_dep.setEnabled(self.__strip_cur.f_alt == 0.)
            self.btn_prc_dir_fixo.setEnabled(True)
            self.btn_prc_esp.setEnabled(True)
            self.btn_prc_ils.setEnabled(False)
            # self.btn_prc_sub.setEnabled(True)
            self.btn_prc_trj.setEnabled(True)

            self.btn_cod_emg.setEnabled(False)
            self.btn_cod_spi.setEnabled(False)
            self.btn_cod_ssr.setEnabled(False)

    # ---------------------------------------------------------------------------------------------
    def __config_strips(self):
        """
        DOCUMENT ME!
        """
        ###
        # strips

        # strips table model
        self.__stp_model = stm.CStripTableModel()
        assert self.__stp_model

        # make connections
        # self.__stp_model.dataChanged.connect(self.__on_strip_data_changed)

        # config strip tableview
        self.qtv_stp.setModel(self.__stp_model)
        self.qtv_stp.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.qtv_stp.setSelectionBehavior(QtGui.QTableView.SelectRows)
        self.qtv_stp.setColumnHidden(ldefs.D_STP_0, True)
        self.qtv_stp.setColumnHidden(ldefs.D_STP_ID, True)
        self.qtv_stp.setColumnHidden(ldefs.D_STP_RAZ, True)
        self.qtv_stp.setColumnHidden(ldefs.D_STP_HORA, True)
        self.qtv_stp.resizeColumnsToContents()

        # make connections
        self.qtv_stp.selectionModel().currentRowChanged.connect(self.__on_strip_row_changed)

        # initial change
        self.__on_strip_row_changed(self.qtv_stp.currentIndex(), self.qtv_stp.currentIndex())

        # config ins/del buttons
        # self.btn_stp_ins.clicked.connect(self.__on_strip_add)
        # self.btn_stp_del.clicked.connect(self.__on_strip_remove)

    # ---------------------------------------------------------------------------------------------
    def __config_toolboxes(self):
        """
        DOCUMENT ME!
        """
        ###
        # procedures

        self.dck_procedures = dckprc.CDockProcedures(self.__control, self)
        assert self.dck_procedures
                
        # config dock
        self.dck_procedures.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.dck_procedures.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
                                        
        # add dock
        self.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dck_procedures)
                                                        
    # ---------------------------------------------------------------------------------------------
    def __create_actions(self):
        """
        DOCUMENT ME!
        """
        # action pause
        self.__act_pause = QtGui.QAction(QtGui.QIcon(":/pixmaps/gamepause.xpm"), self.tr("&Pause"), self)
        assert self.__act_pause is not None

        # config action pause
        self.__act_pause.setCheckable(True)
        self.__act_pause.setChecked(False)
        self.__act_pause.setShortcut(self.tr("Ctrl+P"))
        self.__act_pause.setStatusTip(self.tr("Pause the console"))

        self.__act_pause.setEnabled(False)

        # action quit
        self.__act_quit = QtGui.QAction(QtGui.QIcon(":/pixmaps/gamequit.xpm"), self.tr("&Quit"), self)
        assert self.__act_quit is not None

        # config action quit
        self.__act_quit.setShortcut(self.tr("Ctrl+Q"))
        self.__act_quit.setStatusTip(self.tr("Leave the console"))

        # connect action quit
        self.__act_quit.triggered.connect(QtGui.qApp.closeAllWindows)

        # action zoomIn
        self.__act_zoom_in = QtGui.QAction(QtGui.QIcon(":/pixmaps/zoomin.xpm"), self.tr("Zoom &In"), self)
        assert self.__act_zoom_in is not None

        # config action zoomIn
        self.__act_zoom_in.setShortcut(self.tr("Ctrl++"))
        self.__act_zoom_in.setStatusTip(self.tr("Set coverage of radar screen"))

        self.__act_zoom_in.triggered.connect(self.__slate_radar.zoom_in)
        self.__act_zoom_in.triggered.connect(self.__slate_radar.showRange)

        # action zoomOut
        self.__act_zoom_out = QtGui.QAction(QtGui.QIcon(":/pixmaps/zoomout.xpm"), self.tr("Zoom &Out"), self)
        assert self.__act_zoom_out is not None

        # config action zoomOut
        self.__act_zoom_out.setShortcut(self.tr("Ctrl+-"))
        self.__act_zoom_out.setStatusTip(self.tr("Set coverage of radar screen"))

        self.__act_zoom_out.triggered.connect(self.__slate_radar.zoom_out)
        self.__act_zoom_out.triggered.connect(self.__slate_radar.showRange)

        # action invert
        self.__act_invert = QtGui.QAction(QtGui.QIcon(":/pixmaps/invert.xpm"), self.tr("&Invert Screen"), self)
        assert self.__act_invert is not None

        # config action invert
        self.__act_invert.setCheckable(True)
        self.__act_invert.setChecked(False)
        self.__act_invert.setShortcut(self.tr("Ctrl+I"))
        self.__act_invert.setStatusTip(self.tr("Invert radar screen"))

        # action about
        self.__act_about = QtGui.QAction(self.tr("&About"), self)
        assert self.__act_about is not None

        # config action about
        self.__act_about.setStatusTip(self.tr("About Piloto"))

        # connect action about
        self.__act_about.triggered.connect(self.about)

        # action aboutQt
        self.__act_about_qt = QtGui.QAction(self.tr("About &Qt"), self)
        assert self.__act_about_qt is not None

        # config action aboutQt
        self.__act_about_qt.setStatusTip(self.tr("About Qt"))

        # connect action aboutQt
        self.__act_about_qt.triggered.connect(QtGui.qApp.aboutQt)

    # ---------------------------------------------------------------------------------------------
    def __create_toolbars(self):
        """
        DOCUMENT ME!
        """
        # create toolBar file
        ltbr_file = self.addToolBar(self.tr("File"))
        assert ltbr_file is not None

        ltbr_file.addAction(self.__act_quit)
        ltbr_file.addAction(self.__act_pause)

        # create toolBar view
        ltbr_view = self.addToolBar(self.tr("View"))
        assert ltbr_view is not None

        ltbr_view.addAction(self.__act_zoom_out)
        ltbr_view.addAction(self.__act_zoom_in)
        ltbr_view.addAction(self.__act_invert)

        # create toolBar help
        ltbr_help = self.addToolBar(self.tr("Help"))
        assert ltbr_help is not None

        ltbr_help.addAction(self.__act_about)
        ltbr_help.addAction(self.__act_about_qt)

    # ---------------------------------------------------------------------------------------------
    def __get_current_strip(self):
        """
        DOCUMENT ME!
        """
        # get current index
        l_index = self.qtv_stp.currentIndex()

        if not l_index.isValid():
            # return
            return None

        # get current row
        l_row = l_index.row()

        # get strip
        self.__strip_cur = self.__stp_model.lst_strips[l_row]
        assert self.__strip_cur

        # get strip info
        # l_info = self.__stp_model.data(self.__stp_model.index(l_row, ldefs.D_FIX_INFO)).toString()

        # return current strip
        return self.__strip_cur

    # ---------------------------------------------------------------------------------------------
    def __get_status(self, f_strip):
        """
        obtém o status da aeronave selecionada

        @param f_strip: strip selecionada
        """
        # nenhuma strip selecionada ?
        if f_strip is None:
            # nenhuma strip selecionada. cai fora...
            return

        # status request
        ls_req = "data/status.json?{}".format(f_strip.s_callsign)

        # get server address
        l_srv = self.__dct_config.get("srv.addr", None)

        if l_srv is not None:
            # obtém os dados de status da aneronave
            l_status = self.__sck_http.get_data(l_srv, ls_req)

            if (l_status is not None) and (l_status != ""):
                # obtém os dados de status
                ldct_status = json.loads(l_status)

                # coloca os dados nos widgets
                self.__set_status(f_strip.s_callsign, ldct_status)

            # senão, não achou no servidor...
            else:
                # logger
                l_log = logging.getLogger("CWndMainPiloto::__get_status")
                l_log.setLevel(logging.ERROR)
                l_log.error(u"<E01({}): aeronave({}) não existe no servidor.".format(datetime.time().strftime("%H:%M:%S"), f_strip.s_callsign))

        # senão, não achou endereço do servidor
        else:
            # logger
            l_log = logging.getLogger("CWndMainPiloto::__get_status")
            l_log.setLevel(logging.WARNING)
            l_log.warning(u"<E02({}): srv.addr não existe na configuração.".format(datetime.time().strftime("%H:%M:%S")))

    # ---------------------------------------------------------------------------------------------
    def __make_connections(self):
        """
        DOCUMENT ME!
        """
        # clear to go
        # assert self._oWeather is not None
        # assert self._widPageWeatherConfig is not None
        # assert self.__widRadarScope is not None

        assert self.__act_pause is not None
        assert self.__act_zoom_in is not None
        assert self.__act_zoom_out is not None
        assert self.__act_invert is not None

        self.__act_pause.toggled.connect(self.__slate_radar.pause)
        self.__act_invert.toggled.connect(self.__slate_radar.invert)

        # self._oWeather.qnhChanged.connect(self._widPageWeatherConfig.setQNH)
        # self._oWeather.surfaceWindChanged.connect(self._widPageWeatherConfig.setSurfaceWind)
        # self._oWeather.aloftWindChanged.connect(self._widPageWeatherConfig.setAloftWind)
        # self._oWeather.qnhChanged.connect(self.showQNH)
        # self._oWeather.qnhChanged.connect(self.showTL)
        # self._oWeather.surfaceWindChanged.connect(self.showWind)

        # self.C_SIG_STRIP_CHG.connect(self.__on_strip_data_changed)

        # clear to go
        assert self.btn_cmd_altitude
        assert self.btn_cmd_direcao
        assert self.btn_cmd_velocidade

        # buttons connection
        self.btn_cmd_altitude.clicked.connect(self.__on_btn_cmd_altitude)
        self.btn_cmd_direcao.clicked.connect(self.__on_btn_cmd_direcao)
        self.btn_cmd_velocidade.clicked.connect(self.__on_btn_cmd_velocidade)

        self.btn_prc_apx.clicked.connect(self.__on_btn_prc_apx)
        self.btn_prc_arr.clicked.connect(self.__on_btn_prc_arr)
        self.btn_prc_dep.clicked.connect(self.__on_btn_prc_dep)
        self.btn_prc_dir_fixo.clicked.connect(self.__on_btn_prc_dir_fixo)
        self.btn_prc_esp.clicked.connect(self.__on_btn_prc_esp)
        # self.btn_prc_sub.clicked.connect(self.__on_btn_prc_sub)
        self.btn_prc_trj.clicked.connect(self.__on_btn_prc_trj)

        # clear to go
        assert self.btn_send

        # send connection
        self.btn_send.clicked.connect(self.__on_btn_send)

    # ---------------------------------------------------------------------------------------------
    # @QtCore.pyqtSlot()
    def notify(self, f_evt):
        """
        DOCUMENT ME!
        """
        # check input
        assert f_evt

        # recebeu um aviso de término da aplicação ?
        if isinstance(f_evt, events.CQuit):
            # para todos os processos
            # gdata.G_KEEP_RUN = False

            # aguarda o término das tasks
            time.sleep(1)

            # termina a aplicação
            # sys.exit()

        # recebeu um aviso de configuração de exercício ?
        elif isinstance(f_evt, evtcfg.CConfigExe):
            # atualiza exercício
            self.status_bar.update_exe(f_evt.s_exe)

        # recebeu um aviso de hora de simulação ?
        elif isinstance(f_evt, evtcfg.CConfigHora):
            # atualiza horário
            self.status_bar.update_hora(f_evt.t_hora)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_cmd_altitude(self):
        """
        callback do botão altitude da botoeira
        """
        # existe strip selecionada ?
        if self.__get_current_strip() is not None:
            # obtém os dados de performance
            ldct_prf = self.__dct_prf.get(self.__strip_cur.s_prf, None)

            # cria a dialog de altitude
            self.__dlg_altitude = dlgalt.CDlgAltitude(self.__strip_cur, ldct_prf, self)
            assert self.__dlg_altitude

            # exibe a dialog de altitude
            if self.__dlg_altitude.exec_():
                # coloca o comando no label
                self.lbl_comando.setText("{}: {}".format(self.__strip_cur.s_callsign, self.__dlg_altitude.get_data()))

                # habilita o envio
                self.btn_send.setEnabled(True)

            # senão, <cancel>
            else: pass

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_cmd_direcao(self):
        """
        callback do botão direção da botoeira
        """
        # existe strip selecionada ?
        if self.__get_current_strip() is not None:
            # cria a dialog de direção
            self.__dlg_direcao = dlgdir.CDlgDirecao(self.__strip_cur.f_rumo_mag, self)
            assert self.__dlg_direcao

            # exibe a dialog de direção
            if self.__dlg_direcao.exec_():
                # coloca o comando no label
                self.lbl_comando.setText("{}: {}".format(self.__strip_cur.s_callsign, self.__dlg_direcao.get_data()))

                # habilita o envio
                self.btn_send.setEnabled(True)

            # senão, <cancel>
            else: pass

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_cmd_velocidade(self):
        """
        callback do botão velocidade da botoeira
        """
        # existe strip selecionada ?
        if self.__get_current_strip() is not None:
            # obtém os dados de performance
            ldat_prf = self.__dct_prf.get(self.__strip_cur.s_prf, None)

            # cria a dialog de velocidade
            self.__dlg_velocidade = dlgvel.CDlgVelocidade(self.__strip_cur, ldat_prf, self)
            assert self.__dlg_velocidade

            # exibe a dialog de velocidade
            if self.__dlg_velocidade.exec_():
                # coloca o comando no label
                self.lbl_comando.setText("{}: {}".format(self.__strip_cur.s_callsign, self.__dlg_velocidade.get_data()))

                # habilita o envio
                self.btn_send.setEnabled(True)

            # senão, <cancel>
            else: pass

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_prc_apx(self):
        """
        callback do botão procedimento de aproximação da botoeira
        """
        # existe strip selecionada ?
        if self.__get_current_strip() is not None:
            # cria a dialog de aproximação
            ldlg_aproximacao = dlgapx.CDlgAproximacao(self.__sck_http, self.__dct_config, self.__strip_cur, self.__dct_apx, self)
            assert ldlg_aproximacao

            # exibe a dialog de aproximação
            if ldlg_aproximacao.exec_():
                # coloca o comando no label
                self.lbl_comando.setText("{}: {}".format(self.__strip_cur.s_callsign, ldlg_aproximacao.get_data()))

                # habilita o envio
                self.btn_send.setEnabled(True)

            # senão, <cancel>
            else: pass

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_prc_arr(self):
        """
        callback do botão procedimento de pouso da botoeira
        """
        # existe strip selecionada ?
        if self.__get_current_strip() is not None:
            # cria a dialog de pouso
            ldlg_pouso = dlgarr.CDlgPouso(self.__sck_http, self.__dct_config, self.__strip_cur, self.__lst_arr, self)
            assert ldlg_pouso

            # exibe a dialog de pouso
            if ldlg_pouso.exec_():
                # coloca o comando no label
                self.lbl_comando.setText("{}: {}".format(self.__strip_cur.s_callsign, ldlg_pouso.get_data()))

                # habilita o envio
                self.btn_send.setEnabled(True)

            # senão, <cancel>
            else: pass

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_prc_dep(self):
        """
        callback do botão procedimento de decolagem da botoeira
        """
        # existe strip selecionada ?
        if self.__get_current_strip() is not None:
            # cria a dialog de decolagem
            ldlg_decolagem = dlgdep.CDlgDecolagem(self.__sck_http, self.__dct_config, self.__strip_cur, self.__lst_dep, self)
            assert ldlg_decolagem

            # exibe a dialog de pouso
            if ldlg_decolagem.exec_():
                # coloca o comando no label
                self.lbl_comando.setText("{}: {}".format(self.__strip_cur.s_callsign, ldlg_decolagem.get_data()))

                # habilita o envio
                self.btn_send.setEnabled(True)

            # senão, <cancel>
            else: pass

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_prc_dir_fixo(self):
        """
        callback do botão procedimento de direcionamento a fixo da botoeira
        """
        # existe strip selecionada ?
        if self.__get_current_strip() is not None:
            # cria a dialog de direcionamento a fixo
            ldlg_dir_fixo = dlgfix.CDlgDirFixo(self.__sck_http, self.__dct_config, self.__strip_cur, self.__dct_fix, self)
            assert ldlg_dir_fixo

            # exibe a dialog de direcionamento a fixo
            if ldlg_dir_fixo.exec_():
                # coloca o comando no label
                self.lbl_comando.setText("{}: {}".format(self.__strip_cur.s_callsign, ldlg_dir_fixo.get_data()))

                # habilita o envio
                self.btn_send.setEnabled(True)

            # senão, <cancel>
            else: pass

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_prc_esp(self):
        """
        callback do botão procedimento de espera da botoeira
        """
        # existe strip selecionada ?
        if self.__get_current_strip() is not None:
            # cria a dialog de espera
            ldlg_espera = dlgesp.CDlgEspera(self.__sck_http, self.__dct_config, self.__strip_cur, self.__dct_esp, self)
            assert ldlg_espera

            # exibe a dialog de espera
            if ldlg_espera.exec_():
                # coloca o comando no label
                self.lbl_comando.setText("{}: {}".format(self.__strip_cur.s_callsign, ldlg_espera.get_data()))

                # habilita o envio
                self.btn_send.setEnabled(True)

            # senão, <cancel>
            else: pass

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_prc_sub(self):
        """
        callback do botão procedimento de subida da botoeira
        """
        # existe strip selecionada ?
        if self.__get_current_strip() is not None:
            # cria a dialog de subida
            ldlg_subida = dlgsub.CDlgSubida(self.__sck_http, self.__dct_config, self.__strip_cur, self.__dct_sub, self)
            assert ldlg_subida

            # exibe a dialog de subida
            if ldlg_subida.exec_():
                # coloca o comando no label
                self.lbl_comando.setText("{}: {}".format(self.__strip_cur.s_callsign, ldlg_subida.get_data()))

                # habilita o envio
                self.btn_send.setEnabled(True)

            # senão, <cancel>
            else: pass

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_prc_trj(self):
        """
        callback do botão procedimento de trajetória da botoeira
        """
        # existe strip selecionada ?
        if self.__get_current_strip() is not None:
            # cria a dialog de trajetória
            ldlg_trajetoria = dlgtrj.CDlgTrajetoria(self.__sck_http, self.__dct_config, self.__strip_cur, self.__dct_trj, self)
            assert ldlg_trajetoria

            # exibe a dialog de trajetória
            if ldlg_trajetoria.exec_():
                # coloca o comando no label
                self.lbl_comando.setText("{}: {}".format(self.__strip_cur.s_callsign, ldlg_trajetoria.get_data()))

                # habilita o envio
                self.btn_send.setEnabled(True)

            # senão, <cancel>
            else: pass

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_send(self):
        """
        callback do botão send
        """
        # obtém o comando do label
        ls_cmd = self.lbl_comando.text()

        # monta o buffer de envio
        ls_buff = str(gdefs.D_MSG_VRS) + gdefs.D_MSG_SEP + \
                  str(gdefs.D_MSG_PIL) + gdefs.D_MSG_SEP + \
                  str(ls_cmd)

        # envia o comando
        self.__sck_snd_cpil.send_data(ls_buff)

        # coloca o comando no history
        self.qlw_history.insertItem(0, ls_cmd)

        # desabilita o envio
        self.btn_send.setEnabled(False)

        # reset command
        if self.__strip_cur is not None:
            # limpa o comando
            self.lbl_comando.setText("{}: ".format(self.__strip_cur.s_callsign))

        # senão,...
        else:
            # limpa o comando
            self.lbl_comando.setText("")

    # ---------------------------------------------------------------------------------------------
    '''
    # @QtCore.pyqtSlot()
    def __on_strip_add(self):
        """
        DOCUMENT ME!
        """
        # check exec conditions
        assert self.__scene
        assert self.__stp_model

        assert self.qtv_stp
        assert self.btn_stp_ins
        assert self.btn_stp_del

        # get row count
        l_row = self.__stp_model.rowCount()

        # insert row at end
        self.__stp_model.insertRows(l_row)

        # get row index
        l_index = self.__stp_model.index(l_row, 0)

        # get model
        l_strip = self.__stp_model.lst_strips[l_row]
        assert l_strip

        # insert strip on view
        self.__scene.strip_inserted(l_strip)

        # emit signal
        self.C_SIG_STRIP_INS.emit(l_strip)

        # resets the model to its original state in any attached views
        self.__stp_model.reset()

        # ajusta as colunas da view
        self.qtv_stp.resizeColumnsToContents()
        self.qtv_stp.setColumnHidden(ldefs.D_STP_0, True)

        # config ins/del buttons
        self.btn_stp_ins.setEnabled(True)
        self.btn_stp_del.setEnabled(self.__stp_model.rowCount() > 0)

        # get tableview
        self.qtv_stp.setFocus()
        self.qtv_stp.setCurrentIndex(l_index)
        self.qtv_stp.edit(l_index)
    '''
    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(QtCore.QModelIndex, QtCore.QModelIndex)
    def __on_strip_row_changed(self, f_index_new, f_index_old):
        """
        DOCUMENT ME!
        """
        # is index valid ?
        if f_index_old.isValid():
            # get old strip
            l_strip_old = self.__stp_model.lst_strips[f_index_old.row()]
            assert l_strip_old

        # is index valid ?
        if f_index_new.isValid():
            # get new strip
            self.__strip_cur = self.__stp_model.lst_strips[f_index_new.row()]
            assert self.__strip_cur

            # obtém o status da aeronave
            self.__get_status(self.__strip_cur)

            # habilita botoeira
            self.gbx_comandos.setEnabled(True)

            # inicia o comando
            self.lbl_comando.setText("{}: ".format(self.__strip_cur.s_callsign))

            # desabilita o envio
            self.btn_send.setEnabled(False)

            # emit signal
            self.C_SIG_STRIP_SEL.emit(self.__strip_cur)

        # reconfig buttons
        self.__config_buttons()

    # ---------------------------------------------------------------------------------------------
    '''
    @QtCore.pyqtSlot(QtCore.QModelIndex, QtCore.QModelIndex)
    def __on_strip_data_changed(self, f_index_tl, f_index_br):
        """
        @param f_index_tl: topLeft index
        @param f_index_br: bottomRight index
        """
        # check input
        assert f_index_tl

        # check exec conditions
        assert self.__stp_model
        # assert self.__scene

        # is index valid ?
        if f_index_tl.isValid():
            # get strip
            l_strip = self.__stp_model.lst_strips[f_index_tl.row()]
            assert l_strip

            # change strip on scene
            # self.__scene.strip_changed(l_strip)
    '''
    # ---------------------------------------------------------------------------------------------
    '''
    # @QtCore.pyqtSlot()
    def __on_strip_remove(self):
        """
        DOCUMENT ME!
        """
        # check exec conditions
        assert self.__scene
        assert self.__stp_model

        assert self.qtv_stp
        assert self.btn_stp_ins
        assert self.btn_stp_del

        # get current index
        l_index = self.qtv_stp.currentIndex()

        if not l_index.isValid():
            return

        # get current row
        l_row = l_index.row()

        # get strip
        l_strip = self.__stp_model.lst_strips[l_row]
        assert l_strip

        # get strip info
        l_info = self.__stp_model.data(self.__stp_model.index(l_row, ldefs.D_FIX_INFO)).toString()

        # ask user if it's ok
        if QtGui.QMessageBox.No == QtGui.QMessageBox.question(self, "Remove Strip",
                                       "Remove strip {} ?".format(l_info),
                                       QtGui.QMessageBox.Yes|QtGui.QMessageBox.No):
            # return
            return

        # remove a linha do modelo
        self.__stp_model.removeRows(l_row)

        # ajusta as colunas da view
        self.qtv_stp.resizeColumnsToContents()
        self.qtv_stp.setColumnHidden(ldefs.D_STP_0, True)

        # config ins/del buttons
        self.btn_stp_ins.setEnabled(True)
        self.btn_stp_del.setEnabled(self.__stp_model.rowCount() > 0)

        # select strip
        # self.__on_strip_row_changed(self.qtv_stp.currentIndex(), self.qtv_stp.currentIndex())

        # remove strip from scene
        self.__scene.remove_item(l_strip)
    '''
    # ---------------------------------------------------------------------------------------------
    def __read_settings(self):
        """
        DOCUMENT ME!
        """
        l_settings = QtCore.QSettings("sophosoft", "piloto")

        l_pos = l_settings.value("pos", QtCore.QPoint(200, 200)).toPoint()
        l_size = l_settings.value("size", QtCore.QSize(400, 400)).toSize()

        self.resize(l_size)
        self.move(l_pos)

    # ---------------------------------------------------------------------------------------------
    def __really_quit(self):
        """
        DOCUMENT ME!
        """
        l_ret = QtGui.QMessageBox.warning(self,
                    self.tr("Piloto"),
                    self.tr("Do you want to quit Piloto ?"),
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.Default, QtGui.QMessageBox.No)

        # yes ?
        if QtGui.QMessageBox.Yes == l_ret:
            # retorna
            return True

        # retorna
        return False

    # ---------------------------------------------------------------------------------------------
    def __set_status(self, fs_callsign, fdct_status):
        """
        DOCUMENT ME!
        """
        # função operacional atual
        ls_fnc_ope = fdct_status.get("fnc_ope", None)

        # número do procedimento
        ls_prc_id = fdct_status.get("prc_id", None)

        # get anv
        l_anv = self.__dct_flight.get(fs_callsign, None)

        if l_anv is not None:
            # set status
            l_anv.s_status = "{}/{}".format(ls_fnc_ope, ls_prc_id)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(QtCore.QTimerEvent)
    def timerEvent(self, f_evt):
        """
        DOCUMENT ME!
        """
        # acionado timer de fetch de dados de aeronave ?
        if f_evt.timerId() == self.__i_timer_fetch:
            # for all flights...
            for l_callsign, l_flight in self.__dct_flight.iteritems():
                # new flight ?
                if l_flight not in self.__stp_model.lst_strips:
                    # insert flight on model
                    self.__stp_model.lst_strips.append(l_flight)

                    # reset flag de modificações
                    self.__stp_model.v_dirty = False

                    # emit signal
                    self.C_SIG_STRIP_INS.emit(l_flight)

                # senão, update data...
                # else:
                    # select strip
                    # self.__on_strip_data_changed(self.qtv_stp.currentIndex(), self.qtv_stp.currentIndex())

                    # reset flag de modificações
                    # self.__stp_model.v_dirty = True

                    # emit signal
                    # self.C_SIG_STRIP_CHG.emit(l_flight)

            # update view
            # self.__stp_model.dataChanged.emit(self.qtv_stp.currentIndex(), self.qtv_stp.currentIndex())
            self.__stp_model.layoutChanged.emit()

            # ajusta as colunas da view
            self.qtv_stp.resizeColumnsToContents()

        # acionado timer de status de aeronave ?
        elif f_evt.timerId() == self.__i_timer_status:
            # obtém o status da aeronave selecionada
            self.__get_status(self.__strip_cur)

    # ---------------------------------------------------------------------------------------------
    def __write_settings(self):
        """
        DOCUMENT ME!
        """
        l_settings = QtCore.QSettings("sophosoft", "piloto")

        l_settings.setValue("pos", self.pos())
        l_settings.setValue("size", self.size())
    '''
    # ---------------------------------------------------------------------------------------------
    def e_strips(self):
        """
        DOCUMENT ME!
        """
        ###
        # strips

        # build the list widgets
        for i in xrange(10):
            listItem = QtGui.QListWidgetItem(self.qlw_strips)
            listItem.setSizeHint(QtCore.QSize(300, 63))  # or else the widget items will overlap(irritating bug)

            self.qlw_strips.setItemWidget(listItem, strips.CWidStrip(self.__control, i, self))
    '''
    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_visual(self):
        """
        get visual dictionary
        """
        return self.dck_procedures.dct_visual

# < the end >--------------------------------------------------------------------------------------
