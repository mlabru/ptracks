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

revision 0.1  2017/jul  matias
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Ivan Matias"
__date__ = "2017/07"

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
import model.items.brk_new as brkTrj

# view
import view.dbedit.dlg_brk_trj_edit_new_ui as dlg

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CDlgBrkTrjEditNEW >-------------------------------------------------------------------------

class CDlgBrkTrjEditNEW(QtGui.QDialog, dlg.Ui_CDlgBrkTrjEditNEW):
    """
    mantém as informações sobre a dialog de edição de pontos de uma trajetória
    """
    # -------------------------------------------------------------------------------------------
    def __init__(self, f_control, f_oBrkTrj=None, f_parent=None):
        """
        constructor
        cria uma dialog de edição de pontos de uma trajetória

        @param f_control : control manager do editor da base de dados
        @param f_lstBrkTrj : lista como os pontos da trajetória a editar
        @param f_parent : janela vinculada
        """
        # verifica parâmetros de entrada
        assert (f_control)

        # init super class
        super(CDlgBrkTrjEditNEW, self).__init__(f_parent)

        # salva o control manager localmente
        self._control = f_control

        # salve o model manager localmente
        self._model = f_control.model
        assert (self._model)

        # obtém o gerente de configuração
        self._config = f_control.config
        assert (self._config)

        # obtém o dicionário de configuração
        self._dctConfig = self._config.dct_config
        assert (self._dctConfig)

        # salva a parent window localmente
        self._wndParent = f_parent

        # salva os parâmetros localmente
        self._oBrkTrj = f_oBrkTrj

        # pathnames
        self._sPN = None

        # monta a dialog
        self.setupUi(self)

        # configura título da dialog
        if self._oBrkTrj:
            self.setWindowTitle(self.tr(u"Edição dos pontos da trajetória"))
        else:
            self.setWindowTitle(self.tr(u"Novos pontos da trajetória"))

        # carrega o combobox de fixos e o combobox de procedimentos
        self.fillComboBoxes()

        # configura botões
        self.btnCancel.setText("&Cancela")
        self.btnOk.setFocus()

        # configurações de conexões slot/signal
        self.configConnects()

        # configurações de títulos e mensagens da janela de edição
        self.configTexts()

        # restaura as configurações da janela de edição
        self.restoreSettings()

        # atualiza na tela os dados de pontos da trajetória
        self.updateBrkTrjData()


    # -------------------------------------------------------------------------------------------
    def accept(self):
        """
        DOCUMENT ME!
        """
        # logger
        M_LOG.info("accept:>>")
        M_LOG.debug(" Accept editing data ...")

        # ponto da trajetória existe ?
        if (self._oBrkTrj is not None):
            # salva edição do ponto da trajetória
            l_dctBrkTrj = self.guiDataToDict()
            l_dctBrkTrj["nBrk"] = self._oBrkTrj.i_brk_id
            self._oBrkTrj.load_brk(l_dctBrkTrj)

        # senão, o ponto da trajetória não existe
        else:
            # salva novo ponto da trajetória
            self.acceptNew()

        # logger
        M_LOG.info("accept:<<")

        # faz o "accept"
        QtGui.QDialog.accept(self)

    # -------------------------------------------------------------------------------------------
    def acceptNew(self):
        """
        DOCUMENT ME!
        """
        # cria um novo ponto da trajetória
        self._oBrkTrj = brkTrj.CBrkNEW(self._model, self, self.guiDataToDict())
        assert (self._oBrkTrj)

    # ---------------------------------------------------------------------------------------------
    def configConnects(self):
        """
        configura as conexões slot/signal
        """
        # exercício

        # conecta botão Ok
        self.connect(self.btnOk,
                     QtCore.SIGNAL("clicked()"),
                     self.accept)

        # conecta botão Cancela
        self.connect(self.btnCancel,
                     QtCore.SIGNAL("clicked()"),
                     self.reject)

        # conecta o signal de mudança de tipo de coordenada
        self.cbxTCrd.currentIndexChanged.connect(self.selectionTCrdChange)

        # conecta o signal de mudança de fixo
        self.cbxFixo.currentIndexChanged.connect(self.selectionFixoChange)

    # -------------------------------------------------------------------------------------------
    def configTexts(self):
        """
        DOCUMENT ME!
        """
        # configura títulos e mensagens
        self._txtSettings = "CDlgBrkTrjEditNEW"

    # -------------------------------------------------------------------------------------------
    def fillComboBoxes(self):
        """
        carrega os comboboxes de prcoedimento e de performance de aeronaves
        :return:
        """
        # carrega os fixos definidos no sistema

        llst_fix = []
        for ls_fix in self._model.dct_fix.keys():
            llst_fix.append(ls_fix)

        llst_fix.sort()
        self.cbxFixo.addItems(llst_fix)

        # carrega os procedimentos definidos no sistema
        llst_proc=[]

        # aproximacoes
        for li_id in self._model.dct_apx.keys():
            ls_apx = "APX" + str(li_id).zfill(3)
            llst_proc.append(ls_apx)

        # subidas
        for li_id in self._model.dct_sub.keys():
            ls_sub = "SUB" + str(li_id).zfill(3)
            llst_proc.append(ls_sub)

        # esperas
        for li_id in self._model.dct_esp.keys():
            ls_esp = "ESP" + str(li_id).zfill(3)
            llst_proc.append(ls_esp)

        # esperas
        for li_id in self._model.dct_trj.keys():
            ls_trj = "TRJ" + str(li_id).zfill(3)
            llst_proc.append(ls_trj)

        llst_proc.sort()
        llst_proc.insert(0, "None")
        self.cbxTrjPrc.addItems(llst_proc)

    # -------------------------------------------------------------------------------------------
    def getData(self):
        """
        DOCUMENT ME!
        """
        # return
        return (self._oBrkTrj)

    # -------------------------------------------------------------------------------------------
    def guiDataToDict(self):
        """

        :return:
        """
        # logger
        M_LOG.info("guiDataToDict:>>")
        l_dctBrk = {}

        # número do breakpoint da trajetória
        l_dctBrk["nBrk"] = 0

        # tipo de coordenada
        l_dctTCoord = {}
        if 0 == self.cbxTCrd.currentIndex():
            l_dctTCoord["tipo"] = 'L'
            ls_cpoA = str(self.dsbGeoLat.text()).strip()
            ls_cpoA = ls_cpoA.replace(",", ".")
            l_dctTCoord["cpoA"] = ls_cpoA
            ls_cpoB = str(self.dsbGeoLng.text()).strip()
            ls_cpoB = ls_cpoB.replace(",", ".")
            l_dctTCoord["cpoB"] = ls_cpoB
            ls_cpoC = str(self.dsbGeoAlt.text()).strip()
            ls_cpoC = ls_cpoC.replace(",", ".")
            lf_AltM = float(ls_cpoC) * cdefs.D_CNV_FT2M
            l_dctTCoord["cpoC"] = str(lf_AltM)
        else:
            l_dctTCoord["tipo"] = 'F'
            l_dctTCoord["cpoA"] = str(self.cbxFixo.currentText()).strip()

        # coordenada
        l_dctBrk["coord"] = l_dctTCoord

        # altitude
        ls_alt = str(self.dsbTrjAlt.text()).strip()
        ls_alt = ls_alt.replace(",", ".", 1)
        l_dctBrk["altitude"] = ls_alt

        # velocidade
        ls_vel = str(self.dsbTrjVel.text()).strip()
        ls_vel = ls_vel.replace(",", ".")
        l_dctBrk["velocidade"] = ls_vel

        # procedimento
        ls_trjPrc = ""
        if "None" != str(self.cbxTrjPrc.currentText()):
            ls_trjPrc = str(self.cbxTrjPrc.currentText()).strip()

        l_dctBrk["procedimento"] = ls_trjPrc

        # logger
        M_LOG.info("guiDataToDict:<<")

        return l_dctBrk

    # -------------------------------------------------------------------------------------------
    def reject(self):
        """
        DOCUMENT ME!
        """
        # logger
        M_LOG.info("reject:>>")
        M_LOG.debug(" Set object brk to None ...")
        self._oBrkTrj = None

        # logger
        M_LOG.info("reject:<<")

        # faz o "reject"
        QtGui.QDialog.reject(self)

    # -------------------------------------------------------------------------------------------
    def restoreSettings(self):
        """
        restaura as configurações salvas para esta janela
        """
        # obtém os settings
        l_set = QtCore.QSettings()
        assert (l_set)

        # restaura geometria da janela
        self.restoreGeometry(l_set.value("%s/Geometry" % (self._txtSettings)).toByteArray())

        # return
        return True

    # -------------------------------------------------------------------------------------------
    def selectionFixoChange(self, f_iIndex):
        """
        DOCUMENT ME!
        :param f_iIndex:
        :return:
        """
        # logger
        M_LOG.info("selectionFixoChange:>>")

        ls_IndFixo = str(self.cbxFixo.currentText()).strip()
        M_LOG.debug ("Indicativo do fixo selecionado [%s]" % ls_IndFixo)

        if ls_IndFixo in self._model.dct_fix:
            l_oFixo = self._model.dct_fix[ls_IndFixo]
            M_LOG.debug("Lat [%s] - Lng [%s]" % (str(l_oFixo.f_fix_lat), str(l_oFixo.f_fix_lng)))
            self.qleFixoLat.setText(str(l_oFixo.f_fix_lat))
            self.qleFixoLng.setText(str(l_oFixo.f_fix_lng))
        else:
            M_LOG.warning("Fixo inexistente [%s]" % ls_IndFixo)

        # logger
        M_LOG.info("selectionFixoChange:<<")

    # -------------------------------------------------------------------------------------------
    def selectionTCrdChange(self, f_iIndex):
        """
        DOCUMENT ME!
        :param f_iIndex:
        :return:
        """
        self.stkTCrd.setCurrentIndex(f_iIndex)

    # -------------------------------------------------------------------------------------------
    def updateBrkTrjData(self):
        """
        atualiza na tela os a área de dados do ponto da trajetória selecionado
        """
        # logger
        M_LOG.info("updateBrkTrjData:>>")
        M_LOG.debug("Mostrar as informações de um ponto da trajetória")

        # ponto da trajetória existe ?
        if (self._oBrkTrj is not None):
            li_index = 0
            M_LOG.debug("Tipo de coordenada: [%s]" % self._oBrkTrj.s_brk_tipo)
            if "F" == self._oBrkTrj.s_brk_tipo:
                li_index = 1
            M_LOG.debug("Índice: [%d]" % li_index)

            self.cbxTCrd.setCurrentIndex(li_index)
            #self.stkTCrd.setCurrentIndex(li_index)

            if 0 == li_index:
                self.dsbGeoLat.setValue(self._oBrkTrj.f_brk_lat)
                self.dsbGeoLng.setValue(self._oBrkTrj.f_brk_lng)
                self.dsbGeoAlt.setValue(self._oBrkTrj.f_brk_alt * cdefs.D_CNV_M2FT)
            else:
                self.cbxFixo.setCurrentIndex(self.cbxFixo.findText(self._oBrkTrj.s_brk_cpoA))
                self.qleFixoLat.setText(str(self._oBrkTrj.f_brk_lat))
                self.qleFixoLng.setText(str(self._oBrkTrj.f_brk_lng))

            # altitude (QDoubleSpinBox)
            lf_AltFt = self._oBrkTrj.f_brk_alt * cdefs.D_CNV_M2FT
            self.dsbTrjAlt.setValue(lf_AltFt)

            # velocidade (QDoubleSpinBox)
            lf_VelKt = self._oBrkTrj.f_brk_vel * cdefs.D_CNV_MS2KT
            self.dsbTrjVel.setValue(lf_VelKt)

            # procedimento (QComboBox)
            li_cbxIndex = self.cbxTrjPrc.findText(self._oBrkTrj.s_brk_prc)
            if -1 == li_cbxIndex:
                li_cbxIndex = 0
            self.cbxTrjPrc.setCurrentIndex(li_cbxIndex)

        # senão, é um novo tráfego do exercício
        else:
            # posiciona cursor no tipo de coordenada do breakpoint da trajetória
            self.cbxTCrd.setFocus()

        # logger
        M_LOG.info("updateBrkTrjData:<<")

# < the end >--------------------------------------------------------------------------------------
