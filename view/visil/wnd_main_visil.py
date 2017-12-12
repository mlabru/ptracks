#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wnd_main_visil

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/12"

# < imports >--------------------------------------------------------------------------------------

# Python library
import logging
import sys
import time

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

# model
import model.common.glb_data as gdata
import model.common.defs_strips as ldefs
import model.common.strip_model as mstp
import model.common.strip_table_model as stm

import model.newton.defs_newton as ndefs
import model.visil.aircraft_visil as anv

# view
import view.common.dock_procedures as dckprc
import view.common.slate_radar as sltrdr
# import view.common.strip_basic as strp

import view.visil.statusbar_visil as stbar
import view.visil.wnd_main_visil_ui as wndmain_ui

# control
import control.control_debug as cdbg

import control.events.events_basic as evtbas
import control.events.events_config as evtcfg
import control.events.events_flight as evtfly

# resources
import view.resources.resources_rc

# < class CWndMainVisil >--------------------------------------------------------------------------

class CWndMainVisil(QtGui.QMainWindow, wndmain_ui.Ui_wndMainVisil):
    """
    class CWndMainVisil
    """
    # ---------------------------------------------------------------------------------------------
    # signals
    C_SIG_STRIP_DEL = QtCore.pyqtSignal(anv.CAircraftVisil)
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
        super(CWndMainVisil, self).__init__()

        # save control manager
        self.__control = f_control
        # save event manager
        self.__event = f_control.event

        # dicionário de configuração
        self.__dct_config = f_control.config.dct_config
        assert self.__dct_config
                        
        # socket de recebimento
        self.__sck_http = f_control.sck_http
        assert self.__sck_http
                        
        # register as event listener
        self.__event.register_listener(self)

        # init color dictionary
        gdata.G_DCT_COLORS = {}
                
        # load color dictionary
        for l_key, l_val in f_control.view.colors.c_dct_color.iteritems():
            gdata.G_DCT_COLORS[l_key] = QtGui.QColor(l_val[1][0], l_val[1][1], l_val[1][2])

        # flights dictionary
        self.__dct_flight = f_control.model.emula.dct_flight  
        assert self.__dct_flight is not None
                        
        # current strip
        self.__strip_cur = None
                
        # create main Ui
        self.setupUi(self)

        # window title
        self.setWindowTitle(self.tr(u"ViSIL 0.1 [Visualização]", None,))

        # the slate radar is the main widget
        self.__slate_radar = sltrdr.CSlateRadar(f_control, self)
        assert self.__slate_radar

        # the radar screen goes to central widget
        self.setCentralWidget(self.__slate_radar)

        # create status bar
        self.status_bar = stbar.CStatusBarVisil(self)
        assert self.status_bar

        # config statusBar
        self.setStatusBar(self.status_bar)

        # config flight strips
        self.__config_strips()

        # create windows elements
        self.__create_actions()
        self.__create_toolbars()
        self.__config_toolboxes()

        # make SIGNAL-SLOT connections
        self.__make_connections()

        # get initial values from weather()
        # self.__weather.initSignals()

        # read saved settings
        self.__read_settings()

        # strips
        # self.e_strip()

        # fetch aircrafts data timer (1s cycle)
        self.__i_timer_fetch = self.startTimer(1000)
                
        # clock timer (1s cycle)
        self.__i_timer_status = self.startTimer(1000)

        # config tableview
        self.qtv_stp.setFocus()
        self.qtv_stp.setCurrentIndex(self.__stp_model.index(0, 0))

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def about(self):
        """
        about
        """
        # show about box
        QtGui.QMessageBox.about(self, self.tr("About ViSIL", None),
                                      self.tr("Lorem ipsum dolor sit amet, no vim quas animal intellegam.\n"
                                              "Click pro ad impetus tractatos deterruisset. Atqui tritani ut.\n"
                                              "Per postea conclusionemque ad, discere scripserit referrentur.\n"
                                              "Eos esse commune atomorum et, ex mei appareat platonem.\n"
                                              "Use the middle mouse button to center your radar screen.\n"
                                              "\n", None))

    # ---------------------------------------------------------------------------------------------
    # @QtCore.pyqtSlot()
    def closeEvent(self, f_evt):
        """
        close event callback
        """
        # really quit ?
        if self.__really_quit():
            # save actual config
            self.__write_settings()

            # accept
            f_evt.accept()

            # create CQuit event
            l_evt = evtbas.CQuit()
            assert l_evt

            # dispatch event
            self.__event.post(l_evt)

        # otherwise, continua...
        else:
            # ignore
            f_evt.ignore()

    # ---------------------------------------------------------------------------------------------
    def __config_strips(self):
        """
        config strips
        """
        ###
        # strips

        # strips table model
        self.__stp_model = stm.CStripTableModel()
        assert self.__stp_model

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

    # ---------------------------------------------------------------------------------------------
    def __config_toolboxes(self):
        """
        config toolboxes
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
        create actions
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
        self.__act_about.setStatusTip(self.tr("About ViSIL"))

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
        create toolbars
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
        get current strip
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

        # return current strip
        return self.__strip_cur
        
    # ---------------------------------------------------------------------------------------------
    def __get_status(self, f_strip):
        """
        get status

        @param f_strip: strip selecionada
        """
        # nenhuma strip selecionada ?
        if f_strip is None:
            # nenhuma strip selecionada. cai fora...
            return

        # monta o request de status
        ls_req = "data/status.json?{}".format(f_strip.s_callsign)

        # get server address
        l_srv = self.__dct_config.get("srv.addr", None)

        if l_srv is not None:
            # obtém os dados de status da aneronave
            l_status = self.__sck_http.get_data(l_srv, ls_req)

            if (l_status is not None) and (l_status != ""):
                # obtém os dados de status
                ldct_status = json.loads(l_status)

                # salva os dados nos widgets
                self.__set_status(f_strip.s_callsign, ldct_status)

            # senão, não achou no servidor...
            else:
                # logger
                l_log = logging.getLogger("CWndMainVisil::__get_status")
                l_log.setLevel(logging.ERROR)
                l_log.error(u"<E01: aeronave({}) não existe no servidor.".format(f_strip.s_callsign))

        # senão, não achou endereço do servidor
        else:
            # logger
            l_log = logging.getLogger("CWndMainVisil::__get_status")
            l_log.setLevel(logging.WARNING)
            l_log.warning(u"<E02: srv.addr não existe na configuração.")

    # ---------------------------------------------------------------------------------------------
    def __make_connections(self):
        """
        make connections
        """
        # clear to go
        assert self.__slate_radar is not None

        assert self.__act_pause is not None
        assert self.__act_zoom_in is not None
        assert self.__act_zoom_out is not None
        assert self.__act_invert is not None

        self.__act_pause.toggled.connect(self.__slate_radar.pause)
        self.__act_invert.toggled.connect(self.__slate_radar.invert)

    # ---------------------------------------------------------------------------------------------
    # @QtCore.pyqtSlot()
    def notify(self, f_evt):
        """
        notify
        """
        # check input
        assert f_evt
                
        # recebeu um aviso de término da aplicação ?
        if isinstance(f_evt, evtbas.CQuit):
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

        # recebeu um aviso de eliminação de aeronave
        elif isinstance(f_evt, evtfly.CFlightKill):
            # get flight
            l_flight = self.__dct_flight.get(f_evt.s_callsign, None)
            #cdbg.M_DBG.debug("CWndMainVisil::notify::l_flight: {}".format(l_flight))

            if l_flight is None:
                # return
                return

            # emit signal
            self.C_SIG_STRIP_DEL.emit(l_flight)

            # trava a lista de vôos
            gdata.G_LCK_FLIGHT.acquire()

            try:
                # remove flight from dicionário de voos
                del self.__dct_flight[f_evt.s_callsign]

            finally:
                # libera a lista de vôos
                gdata.G_LCK_FLIGHT.release()

            # remove flight from model
            del self.__stp_model.lst_strips[self.__stp_model.lst_strips.index(l_flight)]

            # row change
            self.__strip_cur = None
            self.qtv_stp.setCurrentIndex(self.__stp_model.index(0, 0))

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(QtCore.QModelIndex,QtCore.QModelIndex)
    def __on_strip_row_changed(self, f_index_new, f_index_old):
        """
        on strip row changed
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
                        
            # emit signal
            self.C_SIG_STRIP_SEL.emit(self.__strip_cur)

    # ---------------------------------------------------------------------------------------------
    def __read_settings(self):
        """
        read settings
        """
        l_settings = QtCore.QSettings("sophosoft", "visil")

        l_pos = l_settings.value("pos", QtCore.QPoint(200, 200)).toPoint()
        l_size = l_settings.value("size", QtCore.QSize(400, 400)).toSize()

        self.resize(l_size)
        self.move(l_pos)

    # ---------------------------------------------------------------------------------------------
    def __really_quit(self):
        """
        really quit
        """
        l_ret = QtGui.QMessageBox.warning(self,
                    self.tr("ViSIL"),
                    self.tr("Do you want to quit ViSIL ?"),
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.Default, QtGui.QMessageBox.No)

        # yes ?
        if QtGui.QMessageBox.Yes == l_ret:
            # return
            return True

        # return
        return False

    # ---------------------------------------------------------------------------------------------
    def __recursive_checks(self, fo_parent):
        """
        recursive checks
        """
        # obtém o checkState
        l_checkState = fo_parent.checkState(0)

        # o nó é uma folha ? (i.e. sem filhos)
        if 0 == fo_parent.childCount():
            # o nó tem dados associados ?
            if fo_parent.data(0, QtCore.Qt.WhatsThisRole).toPyObject() is not None:
                # obtém o nome do mapa
                ls_name = fo_parent.data(0, QtCore.Qt.WhatsThisRole).toPyObject()[0]

                # nome válido ?
                if ls_name is not None:
                    # obtém o mapa
                    l_map = self.__slate_radar.findMap(ls_name)

                    # achou o mapa ?
                    if l_map is not None:
                        # muda o status de exibição
                        l_map.showMap(QtCore.Qt.Checked == l_checkState)

        # para todos os filhos...
        for l_i in xrange(fo_parent.childCount()):
            # muda o checkState
            fo_parent.child(l_i).setCheckState(0, l_checkState)
            fo_parent.child(l_i).setDisabled(QtCore.Qt.Unchecked == l_checkState)

            # o nó tem dados associados ?
            if fo_parent.data(0, QtCore.Qt.WhatsThisRole).toPyObject() is not None:
                # obtém o nome do mapa
                ls_name = fo_parent.child(l_i).data(0, QtCore.Qt.WhatsThisRole).toPyObject()[0]
                # cdbg.M_DBG.debug("ls_name: " + ls_name)

                # nome válido ?
                if ls_name is not None:
                    # obtém o mapa
                    l_map = self.__slate_radar.findMap(ls_name)

                    # achou o mapa ?
                    if l_map is not None:
                        # muda o status de exibição
                        l_map.showMap(QtCore.Qt.Checked == l_checkState)

            # propaga aos filhos
            self.__recursive_checks(fo_parent.child(l_i))

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(int)
    def showCoords(self, f_coords):
        """
        show coords
        """
        self.status_bar.lblCoords.setText(u"99ᵒ 99' 99\" N 999ᵒ 99' 99\" E" % int(f_coords))

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(int)
    def showQNH(self, f_qnh):
        """
        show QNH
        """
        self.status_bar.lblQNH.setText("Q%d" % int(f_qnh))

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(int)
    def showTL(self, f_qnh):
        """
        show TL
        """
        # TODO: airport specific
        if f_qnh >= 1013.:
            l_tl = 60.

        else:
            l_tl = 70.

        self.status_bar.lblTL.setText("TL%d" % int(l_tl))

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(int, int)
    def showWind(self, f_dir, f_v):
        """
        show Wind
        """
        if f_v == 0.:
            l_windstring = "CALM"

        else:
            l_windstring = "%d%c/%dkt" % (int(f_dir), u'°'.encode("utf-8")[1:], int(f_v))

        self.status_bar.lblWind.setText(l_windstring)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(QtCore.QTimerEvent)
    def timerEvent(self, f_evt):
        """
        timer event callback
        """
        # flight data fetch timer event ?
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

            # update view
            # self.__stp_model.dataChanged.emit(self.qtv_stp.currentIndex(), self.qtv_stp.currentIndex())
            self.__stp_model.layoutChanged.emit()

            # ajusta as colunas da view
            self.qtv_stp.resizeColumnsToContents()

        # clock timer event ?
        elif f_evt.timerId() == self.__i_timer_status:
            # display simulation time
            self.lbl_hora.setText(self.__control.sim_time.get_hora_format())

            # obtém o status da aeronave selecionada  
            self.__get_status(self.__strip_cur)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot("QTreeWidgetItem", int)
    def __update_checks(self, f_item, f_iColumn):
        """
        update checks
        """
        # checkState is stored on column 0
        if 0 != f_iColumn:
            # return
            return

        # propaga
        self.__recursive_checks(f_item)

    # ---------------------------------------------------------------------------------------------
    def __write_settings(self):
        """
        write settings
        """
        l_settings = QtCore.QSettings("sophosoft", "visil")

        l_settings.setValue("pos", self.pos())
        l_settings.setValue("size", self.size())
    '''
    # ---------------------------------------------------------------------------------------------
    def e_strip(self):
        """
        e_strip
        """
        ###
        # strips

        # cdbg.M_DBG.debug("e_strips:dct_flight: " + str(self.__dct_flight))
                        
        # build the list widgets
        for i in xrange(8):
            listItem = QtGui.QListWidgetItem(self.qlw_strips)
            listItem.setSizeHint(QtCore.QSize(300, 63))  # or else the widget items will overlap (irritating bug)

            self.qlw_strips.setItemWidget(listItem, strp.CWidStripBasic(self.__control, i, self))
    '''
    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_visual(self):
        return self.dck_procedures.dct_visual

# < the end >--------------------------------------------------------------------------------------
