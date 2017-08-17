#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_brk_trj_edit_new

mantém as informações sobre a dialog de edição dos pontos da trajetória

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

revision 0.1  2017/jul  matias
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
import model.items.brk_new as bptrj
import model.validators.fix_validator as fixval

# view
import view.dbedit.dlg_brk_trj_edit_new_ui as dlg

# control
# import control.control_debug as cdbg

# < class CDlgBrkTrjEditNEW >----------------------------------------------------------------------

class CDlgBrkTrjEditNEW(QtGui.QDialog, dlg.Ui_CDlgBrkTrjEditNEW):
    """
    mantém as informações sobre a dialog de edição de pontos de uma trajetória
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control, flst_brk_trj=None, f_parent=None):
        """
        constructor
        cria uma dialog de edição de pontos de uma trajetória

        @param f_control: control manager do editor da base de dados
        @param flst_brk_trj: lista como os pontos da trajetória a editar
        @param f_parent: janela vinculada
        """
        # check input
        assert f_control

        # init super class
        super(CDlgBrkTrjEditNEW, self).__init__(f_parent)

        # model
        self.__model = f_control.model
        assert self.__model

        # parâmetros
        self.__brk_trj = flst_brk_trj

        # monta a dialog
        self.setupUi(self)

        # configura título da dialog
        if self.__brk_trj:
            self.setWindowTitle(self.tr(u"Edição dos pontos da trajetória"))

        # senão,...
        else:
            self.setWindowTitle(self.tr(u"Novos pontos da trajetória"))

        # carrega o combobox de fixos e o combobox de procedimentos
        self.__fill_comboboxes()

        # configura botões
        self.btnCancel.setText("&Cancela")
        self.btnOk.setFocus()

        # configurações de conexões slot/signal
        self.__config_connects()

        # configurações de títulos e mensagens da janela de edição
        self.__config_texts()

        # restaura as configurações da janela de edição
        self.__restore_settings()

        # atualiza na tela os dados de pontos da trajetória
        self.__update_brk_trj_data()

    # ---------------------------------------------------------------------------------------------
    def accept(self):
        """
        DOCUMENT ME!
        """
        # ponto da trajetória existe ?
        if self.__brk_trj is not None:
            # salva edição do ponto da trajetória
            ldct_brk_trj = self.__gui_data2dict()

            # coloca no dicionário
            ldct_brk_trj["nBrk"] = self.__brk_trj.i_brk_id

            # carrega o dicionário
            self.__brk_trj.load_brk(ldct_brk_trj)

        # senão, o ponto da trajetória não existe
        else:
            # cria um novo ponto da trajetória
            self.__brk_trj = bptrj.CBrkNEW(self.__model, self, self.__gui_data2dict())
            assert self.__brk_trj

        # faz o "accept"
        QtGui.QDialog.accept(self)

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
        # conecta botão Ok
        self.btnOk.clicked.connect(self.accept)

        # conecta botão Cancela
        self.btnCancel.clicked.connect(self.reject)

        # conecta o signal de mudança de tipo de coordenada
        self.cbxTCrd.currentIndexChanged.connect(self.__selection_tcrd_changed)

    # ---------------------------------------------------------------------------------------------
    def __config_texts(self):
        """
        DOCUMENT ME!
        """
        # configura títulos e mensagens
        self.__txt_settings = "CDlgBrkTrjEditNEW"

    # ---------------------------------------------------------------------------------------------
    def __fill_comboboxes(self):
        """
        carrega os comboboxes de prcoedimento e de performance de aeronaves
        """
        # carrega os fixos na combobox
        self.cbxFixo.addItems(sorted(self.__model.dct_fix))

        # config combobox de fixos
        self.cbxFixo.setEditable(True)
        self.cbxFixo.setInsertPolicy(QtGui.QComboBox.NoInsert)

        # completer 
        self.cbxFixo.setCompleter(QtGui.QCompleter(self.cbxFixo))
        self.cbxFixo.completer().setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.cbxFixo.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)
        self.cbxFixo.completer().setModel(self.cbxFixo.model())

        # validator
        self.cbxFixo.setValidator(fixval.CFixValidator(self))

        # connections
        self.cbxFixo.editTextChanged.connect(self.__check_state)
        self.cbxFixo.editTextChanged.emit(self.cbxFixo.currentText())
        self.cbxFixo.currentIndexChanged.connect(self.__selection_fixo_changed)

        # carrega os procedimentos definidos no sistema
        llst_proc = []

        # aproximações
        for li_id in self.__model.dct_apx.keys():
            ls_apx = "APX" + str(li_id).zfill(3)

            # carrega os procedimentos definidos no sistema
            llst_proc.append(ls_apx)

        # subidas
        for li_id in self.__model.dct_sub.keys():
            ls_sub = "SUB" + str(li_id).zfill(3)

            # carrega os procedimentos definidos no sistema
            llst_proc.append(ls_sub)

        # esperas
        for li_id in self.__model.dct_esp.keys():
            ls_esp = "ESP" + str(li_id).zfill(3)

            # carrega os procedimentos definidos no sistema
            llst_proc.append(ls_esp)

        # trajetórias
        for li_id in self.__model.dct_trj.keys():
            ls_trj = "TRJ" + str(li_id).zfill(5)

            # carrega os procedimentos definidos no sistema
            llst_proc.append(ls_trj)

        # ordena a lista de procedimentos
        llst_proc.sort()

        # insere primeiro procedimento
        llst_proc.insert(0, "None")

        # coloca na combobox
        self.cbxTrjPrc.addItems(llst_proc)

    # ---------------------------------------------------------------------------------------------
    def getData(self):
        """
        DOCUMENT ME!
        """
        # return
        return self.__brk_trj

    # ---------------------------------------------------------------------------------------------
    def __gui_data2dict(self):
        """
        DOCUMENT ME!
        """
        # logger
        ldct_brk = {}

        # número do breakpoint da trajetória
        ldct_brk["nBrk"] = 0

        # tipo de coordenada
        ldct_tcrd = {}

        if 0 == self.cbxTCrd.currentIndex():
            ldct_tcrd["tipo"] = 'L'
            ls_cpoA = str(self.dsbGeoLat.text()).strip()
            ls_cpoA = ls_cpoA.replace(",", ".")
            ldct_tcrd["cpoA"] = ls_cpoA

            ls_cpoB = str(self.dsbGeoLng.text()).strip()
            ls_cpoB = ls_cpoB.replace(",", ".")
            ldct_tcrd["cpoB"] = ls_cpoB

            ls_cpoC = str(self.dsbGeoAlt.text()).strip()
            ls_cpoC = ls_cpoC.replace(",", ".")
            ldct_tcrd["cpoC"] = str(float(ls_cpoC) * cdefs.D_CNV_FT2M)

        # senão,...
        else:
            ldct_tcrd["tipo"] = 'F'
            ldct_tcrd["cpoA"] = str(self.cbxFixo.currentText()).strip()

        # coordenada
        ldct_brk["coord"] = ldct_tcrd

        # altitude
        ls_alt = str(self.dsbTrjAlt.text()).strip()
        ls_alt = ls_alt.replace(",", ".", 1)
        ldct_brk["altitude"] = ls_alt

        # velocidade
        ls_vel = str(self.dsbTrjVel.text()).strip()
        ls_vel = ls_vel.replace(",", ".")
        ldct_brk["velocidade"] = ls_vel

        # procedimento
        ls_prc = ""

        if "None" != str(self.cbxTrjPrc.currentText()):
            ls_prc = str(self.cbxTrjPrc.currentText()).strip()

        ldct_brk["procedimento"] = ls_prc

        # return
        return ldct_brk

    # ---------------------------------------------------------------------------------------------
    def reject(self):
        """
        DOCUMENT ME!
        """
        # 
        self.__brk_trj = None

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

    # ---------------------------------------------------------------------------------------------
    def __selection_fixo_changed(self, fi_ndx):
        """
        DOCUMENT ME!

        @param fi_ndx:
        """
        # indicativo do fixo selecionado 
        ls_ind_fixo = str(self.cbxFixo.currentText()).strip().upper()

        # fixo selecionado 
        l_fixo = self.__model.dct_fix.get(ls_ind_fixo, None)
        
        if l_fixo is not None:
            # get fix data
            self.qleFixoLat.setText(str(l_fixo.f_fix_lat))
            self.qleFixoLng.setText(str(l_fixo.f_fix_lng))

        # senão,...
        else:
            # logger
            l_log = logging.getLogger("CDlgBrkTrjEditNEW::__selection_fixo_changed")
            l_log.setLevel(logging.WARNING)
            l_log.warning("<E01: fixo {} inexistente.".format(ls_ind_fixo))

    # ---------------------------------------------------------------------------------------------
    def __selection_tcrd_changed(self, fi_ndx):
        """
        DOCUMENT ME!

        @param fi_ndx:
        """
        # set new stack
        self.stkTCrd.setCurrentIndex(fi_ndx)

    # ---------------------------------------------------------------------------------------------
    def __update_brk_trj_data(self):
        """
        atualiza na tela a área de dados do ponto da trajetória selecionado
        """
        # ponto da trajetória existe ?
        if self.__brk_trj is not None:
            # set default index (lat/lng)
            li_index = 0

            # tipo fixo ?
            if "F" == self.__brk_trj.s_brk_tipo:
                # set index 
                li_index = 1

            # coordinate type
            self.cbxTCrd.setCurrentIndex(li_index)

            # lat/lng ?
            if 0 == li_index:
                self.dsbGeoLat.setValue(self.__brk_trj.f_brk_lat)
                self.dsbGeoLng.setValue(self.__brk_trj.f_brk_lng)
                self.dsbGeoAlt.setValue(self.__brk_trj.f_brk_alt * cdefs.D_CNV_M2FT)

            # senão, fixo
            else:
                self.cbxFixo.setCurrentIndex(self.cbxFixo.findText(self.__brk_trj.s_brk_cpoA))
                self.qleFixoLat.setText(str(self.__brk_trj.f_brk_lat))
                self.qleFixoLng.setText(str(self.__brk_trj.f_brk_lng))

            # altitude (QDoubleSpinBox)
            self.dsbTrjAlt.setValue(self.__brk_trj.f_brk_alt * cdefs.D_CNV_M2FT)

            # velocidade (QDoubleSpinBox)
            self.dsbTrjVel.setValue(self.__brk_trj.f_brk_vel * cdefs.D_CNV_MS2KT)

            # procedimento (QComboBox)
            li_index_prc = self.cbxTrjPrc.findText(self.__brk_trj.s_brk_prc)

            # none selected ?
            if -1 == li_index_prc:
                # set index
                li_index_prc = 0

            # procedure 
            self.cbxTrjPrc.setCurrentIndex(li_index_prc)

        # senão, é um novo tráfego do exercício
        else:
            # posiciona cursor no tipo de coordenada do breakpoint da trajetória
            self.cbxTCrd.setFocus()

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def model(self):
        return self.__model

# < the end >--------------------------------------------------------------------------------------
