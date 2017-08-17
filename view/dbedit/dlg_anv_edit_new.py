#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_anv_edit_new

mantém as informações sobre a dialog de edição de tráfego do exercício

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

revision 0.2  2017/aug  mlabru
pep8 style conventions

revision 0.1  2017/jun  matias
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Ivan Matias"
__date__ = "2017/08"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import os

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

# libs
import libs.coords.coord_defs as cdefs

# model
import model.items.trf_new as clsTrf
import model.validators.prf_validator as prfval
import model.validators.prc_validator as prcval

# view
import view.dbedit.dlg_anv_edit_new_ui as dlg

# control
# import control.control_debug as cdbg

# < class CDlgAnvEditNEW >-------------------------------------------------------------------------

class CDlgAnvEditNEW(QtGui.QDialog, dlg.Ui_CDlgAnvEditNEW):
    """
    mantém as informações sobre a dialog de edição de tráfego de um exercício
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control, f_trf=None, f_parent=None):
        """
        constructor
        cria uma dialog de edição de tráfego de um exercícios

        @param f_control : control manager do editor da base de dados
        @param f_trf : tráfego do exercício a editar
        @param f_parent : janela vinculada
        """
        # check input
        assert f_control

        # init super class
        super(CDlgAnvEditNEW, self).__init__(f_parent)

        # model
        self.__model = f_control.model
        assert self.__model

        # parâmetros
        self.__trf = f_trf

        # monta a dialog
        self.setupUi(self)

        # SSR only allowed octal digits
        l_reg_exp = QtCore.QRegExp("[0-7]*$")
        l_reg_expVal = QtGui.QRegExpValidator(l_reg_exp)

        self.qleSSR.setValidator(l_reg_expVal)

        # configura título da dialog
        if self.__trf:
            self.setWindowTitle(self.tr(u"Edição do Tráfego do Exercício"))

        else:
            self.setWindowTitle(self.tr(u"Novo Tráfego do Exercício"))

        # carrega o combobox de performance e o combobox de procedimentos
        self.__fill_comboboxes()

        # atualiza na tela os dados do exercício
        self.__update_trf_data()

        # configura botões
        self.btnCancel.setText("&Cancela")
        self.btnOk.setFocus()

        # configurações de conexões slot/signal
        self.__config_connects()

        # configurações de títulos e mensagens da janela de edição
        self.__config_texts()

        # restaura as configurações da janela de edição
        self.__restore_settings()

    # ---------------------------------------------------------------------------------------------
    def accept(self):
        """
        DOCUMENT ME!
        """
        # tráfego do exercício existe ?
        if self.__trf is not None:
            # salva edição do tráfego do exercício
            l_dctTrf = self.__gui_data2dict()
            l_dctTrf["nTrf"] = self.__trf.i_trf_id

            self.__trf.load_trf(l_dctTrf)

        # senão, exercício não existe
        else:
            # salva novo tráfego do exercício
            self.__accept_new()

        # faz o "accept"
        QtGui.QDialog.accept(self)

    # ---------------------------------------------------------------------------------------------
    def __accept_new(self):
        """
        DOCUMENT ME!
        """
        # cria um novo tráfego do exercício
        self.__trf = clsTrf.CTrfNEW(self.__model)
        assert self.__trf

        # inicia tráfego do exercício
        self.__trf.make_trf(self.__gui_data2dict())

    # ---------------------------------------------------------------------------------------------
    def __check_state(self, *args, **kwargs):
        """
        identifies the sender of the signal that called it, and validates it's content using the
        assigned validator. The background colour of the widget is then set using the
        setStyleSheet method
        """
        # get sender
        l_sender = self.sender()

        if l_sender is None:
            # return
            return

        # get validator
        l_validator = l_sender.validator()
        assert l_validator

        if l_validator is None:
            # return
            return

        # sender is a combobox ?
        if isinstance(l_sender, QtGui.QComboBox):
           # get QLineEdit of that combobox
           l_sender = l_sender.lineEdit()
           assert l_sender

        # validate
        l_tuple = l_validator.validate(str(l_sender.text()), l_sender.cursorPosition())

        # get state
        l_state = l_tuple[0]

        # acceptable ?
        if QtGui.QValidator.Acceptable == l_state:
            # green
            l_color = "#c4df9b"

        # intermediate ?
        elif QtGui.QValidator.Intermediate == l_state:
            # yellow
            l_color = "#fff79a"

        # senão, invalid...
        else:
            # red
            l_color = "#f6989d"

        # set background color
        l_sender.setStyleSheet("QLineEdit { background-color: %s }" % l_color)

    # ---------------------------------------------------------------------------------------------
    def __config_connects(self):
        """
        configura as conexões slot/signal
        """
        # exercício

        # conecta botão Ok
        self.btnOk.clicked.connect(self.accept)

        # conecta botão Cancela
        self.btnCancel.clicked.connect(self.reject)

    # ---------------------------------------------------------------------------------------------
    def __config_texts(self):
        """
        DOCUMENT ME!
        """
        # configura títulos e mensagens
        self.__txt_settings = "CDlgAnvEditNEW"

    # ---------------------------------------------------------------------------------------------
    def __fill_comboboxes(self):
        """
        carrega os comboboxes de prcoedimento e de performance de aeronaves
        """
        # carrega as performances
        self.cbxPrf.addItems(sorted(self.__model.dct_prf))

        # config combobox de fixos
        self.cbxPrf.setEditable(True)
        self.cbxPrf.setInsertPolicy(QtGui.QComboBox.NoInsert)

        # completer
        self.cbxPrf.setCompleter(QtGui.QCompleter(self.cbxPrf))
        self.cbxPrf.completer().setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.cbxPrf.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)
        self.cbxPrf.completer().setModel(self.cbxPrf.model())

        # validator
        self.cbxPrf.setValidator(prfval.CPrfValidator(self))

        # connections
        self.cbxPrf.editTextChanged.connect(self.__check_state)
        self.cbxPrf.editTextChanged.emit(self.cbxPrf.currentText())
        self.cbxPrf.currentIndexChanged.connect(self.__selection_prf_changed)

        # carrega os procedimentos definidos no sistema
        llst_proc = []

        # aproximações
        for li_id in self.__model.dct_apx.keys():
            ls_apx = "APX{}".format(li_id)
            llst_proc.append(ls_apx)

        # subidas
        for li_id in self.__model.dct_sub.keys():
            ls_sub = "SUB{}".format(li_id)
            llst_proc.append(ls_sub)

        # esperas
        for li_id in self.__model.dct_esp.keys():
            ls_esp = "ESP{}".format(li_id)
            llst_proc.append(ls_esp)

        # trajetórias
        for li_id in self.__model.dct_trj.keys():
            ls_trj = "TRJ{}".format(li_id)
            llst_proc.append(ls_trj)

        # ordena
        llst_proc.sort()

        # insere primeiro procedimento
        llst_proc.insert(0, "NONE")

        # coloca na combobox
        self.cbxProc.addItems(llst_proc)

        # config combobox de procedimentos
        self.cbxProc.setEditable(True)
        self.cbxProc.setInsertPolicy(QtGui.QComboBox.NoInsert)

        # completer 
        self.cbxProc.setCompleter(QtGui.QCompleter(self.cbxProc))
        self.cbxProc.completer().setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.cbxProc.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)
        self.cbxProc.completer().setModel(self.cbxProc.model())

        # validator
        self.cbxProc.setValidator(prcval.CPrcValidator(self))

        # connections
        self.cbxProc.editTextChanged.connect(self.__check_state)
        self.cbxProc.editTextChanged.emit(self.cbxProc.currentText())
        self.cbxProc.currentIndexChanged.connect(self.__selection_proc_changed)

    # ---------------------------------------------------------------------------------------------
    def getData(self):
        """
        DOCUMENT ME!
        """
        # return
        return self.__trf

    # ---------------------------------------------------------------------------------------------
    def __gui_data2dict(self):
        """
        DOCUMENT ME!
        """
        # init dictionary
        ldct_trf = {}

        # identificação do tráfego
        ldct_trf["nTrf"] = 0

        # indicativo do tráfego
        ldct_trf["indicativo"] = str(self.qleInd.text()).strip()

        # performance
        ldct_trf["designador"] = str(self.cbxPrf.currentText()).strip()

        # código transponder
        ldct_trf["ssr"] = int(str(self.qleSSR.text()).strip())

        # aeródromo de origem
        ldct_trf["origem"] = str(self.qleAdOri.text()).strip()

        # aeródromo de origem
        ldct_trf["destino"] = str(self.qleAdDst.text()).strip()

        # procedimento
        ldct_trf["procedimento"] = str(self.cbxProc.currentText()).strip()

        # tempo de ativação do tráfego
        ldct_trf["temptrafego"] = int(str(self.qsbAtvPndMin.text()).strip())

        # posição da aeronave latitude e longitude da aeronave
        ldct_pos = {}
        ldct_pos["tipo"] = 'L'

        ls_cpoA = str(self.qsbPosX.text()).strip()
        ls_cpoA = ls_cpoA.replace(",", ".")
        ldct_pos["cpoA"] = ls_cpoA

        ls_cpoB = str(self.qsbPosY.text()).strip()
        ls_cpoB = ls_cpoB.replace(",", ".")
        ldct_pos["cpoB"] = ls_cpoB

        ldct_trf["coord"] = ldct_pos

        # proa
        ls_proa = str(self.qsbNavPro.text()).strip()
        ls_proa = ls_proa.replace(",", ".")
        ldct_trf["proa"] = ls_proa
        l_log.debug(" Proa [%s]" % ls_proa)

        # velocidade
        ls_vel = str(self.qsbNavVel.text()).strip()
        ls_vel = ls_vel.replace(",", ".")
        ldct_trf["velocidade"] = ls_vel

        # altitude
        ls_alt = str(self.qsbNavAlt.text()).strip()
        ls_alt = ls_alt.replace(",", ".", 1)
        ldct_trf["altitude"] = ls_alt

        # return
        return ldct_trf

    # ---------------------------------------------------------------------------------------------
    def reject(self):
        """
        DOCUMENT ME!
        """
        l_log = logging.getLogger("CDlgAnvEditNEW::reject")
        l_log.setLevel(logging.DEBUG)
        l_log.debug(" Set object trf to None ...")
        self.__trf = None

        # faz o "reject"
        QtGui.QDialog.reject(self)

    # ---------------------------------------------------------------------------------------------
    def __restore_settings(self):
        """
        restaura as configurações salvas para esta janela
        """
        # obtém os settings
        l_set = QtCore.QSettings()
        assert l_set

        # restaura geometria da janela
        self.restoreGeometry(l_set.value("%s/Geometry" % (self.__txt_settings)).toByteArray())

        # return
        return True

    # ---------------------------------------------------------------------------------------------
    def __selection_prf_changed(self, fi_ndx):
        """
        DOCUMENT ME!

        @param fi_ndx:
        """
        # indicativo da performance selecionada
        ls_ind_prf = str(self.cbxPrf.currentText()).strip().upper()

        # performance selecionada
        l_prf = self.__model.dct_prf.get(ls_ind_prf, None)

        if l_prf is not None:
            # get fix data
            #self.qleFixoLat.setText(str(l_prf.f_fix_lat))
            #self.qleFixoLng.setText(str(l_prf.f_fix_lng))
            pass

        # senão,...
        else:
            # logger
            l_log = logging.getLogger("CDlgAnvEditNEW::__selection_prf_changed")
            l_log.setLevel(logging.WARNING)
            l_log.warning("<E01: performance {} inexistente.".format(ls_ind_prf))

    # ---------------------------------------------------------------------------------------------
    def __selection_proc_changed(self, fi_ndx):
        """
        DOCUMENT ME!

        @param fi_ndx:
        """
        # procedimento selecionado 
        ls_ind_proc = str(self.cbxPorc.currentText()).strip().upper()

    # ---------------------------------------------------------------------------------------------
    def __update_trf_data(self):
        """
        atualiza na tela os a área de dados do tráfego do exercício selecionado
        """
        # tráfego exercício existe ?
        if self.__trf is not None:
            # identificação
            self.qleInd.setText(self.__trf.s_trf_ind)

            # tipo da aeronave (QComboBox)
            self.cbxPrf.setCurrentIndex(self.cbxPrf.findText(self.__trf.ptr_trf_prf.s_prf_id))

            # SSR
            self.qleSSR.setText(str(self.__trf.i_trf_ssr))

            # aeródromo de origem
            self.qleAdOri.setText(self.__trf.ptr_trf_aer_ori.s_aer_indc)

            # aeródromo de destino
            self.qleAdDst.setText(self.__trf.ptr_trf_aer_dst.s_aer_indc)

            # procedimento (QComboBox)
            self.cbxProc.setCurrentIndex(self.cbxProc.findText(self.__trf.s_trf_prc))

            # tempo de ativação (QSpinBox)
            li_hor_ini, li_min_ini, li_seg_ini = self.__model.exe.t_exe_hor_ini
            li_min_ini = li_min_ini + (li_hor_ini * 60) + (li_seg_ini / 60)

            li_hor, li_min, li_seg = self.__trf.t_trf_hor_atv
            li_min += (li_hor * 60) + (li_seg / 60)

            self.qsbAtvPndMin.setValue(li_min - li_min_ini)

            # latitude (QDoubleSpinBox)
            self.qsbPosX.setValue(self.__trf.f_trf_lat)

            # longitude (QDoubleSpinBox)
            self.qsbPosY.setValue(self.__trf.f_trf_lng)

            # proa (QDoubleSpinBox)
            self.qsbNavPro.setValue(self.__trf.f_trf_pro_atu)

            # altitude (QDoubleSpinBox)
            self.qsbNavAlt.setValue(self.__trf.f_trf_alt_atu * cdefs.D_CNV_M2FT)

            # velocidade (QDoubleSpinBox)
            self.qsbNavVel.setValue(self.__trf.f_trf_vel_atu * cdefs.D_CNV_MS2KT)

        # senão, é um novo tráfego do exercício
        else:
            # posiciona cursor no início do formulário
            self.qleInd.setFocus()

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def model(self):
        return self.__model

# < the end >--------------------------------------------------------------------------------------
