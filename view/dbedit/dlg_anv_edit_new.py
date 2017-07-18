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

revision 0.1  2017/jun  matias
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Ivan Matias"
__date__ = "2017/06"

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

# view
import view.dbedit.dlg_anv_edit_new_ui as dlg

# < class CDlgAnvEditNEW >-------------------------------------------------------------------------

class CDlgAnvEditNEW(QtGui.QDialog, dlg.Ui_CDlgAnvEditNEW):
    """
    mantém as informações sobre a dialog de edição de tráfego de um exercício
    """
    # -------------------------------------------------------------------------------------------
    def __init__(self, f_control, f_oTrf=None, f_parent=None):
        """
        constructor
        cria uma dialog de edição de tráfego de um exercícios

        @param f_control : control manager do editor da base de dados
        @param f_oExe : tráfego do exercício a editar
        @param f_parent : janela vinculada
        """
        # verifica parâmetros de entrada
        assert (f_control)

        # init super class
        super(CDlgAnvEditNEW, self).__init__(f_parent)

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
        self._oTrf = f_oTrf

        # pathnames
        self._sPN = None

        # monta a dialog
        self.setupUi(self)

        # SSR only allowed octal digits
        l_oRegExp = QtCore.QRegExp("[0-7]*$")
        l_oRegExpVal = QtGui.QRegExpValidator(l_oRegExp)
        self.qleSSR.setValidator(l_oRegExpVal)

        # configura título da dialog
        if self._oTrf:
            self.setWindowTitle(self.tr(u"Edição do Tráfego do Exercício"))
        else:
            self.setWindowTitle(self.tr(u"Novo Tráfego do Exercício"))

        # carrega o combobox de performance e o combobox de procedimentos
        self.fillComboBoxes()

        # atualiza na tela os dados do exercício
        self.updateTrfData()

        # configura botões
        self.btnCancel.setText("&Cancela")
        self.btnOk.setFocus()

        # configurações de conexões slot/signal
        self.configConnects()

        # configurações de títulos e mensagens da janela de edição
        self.configTexts()

        # restaura as configurações da janela de edição
        self.restoreSettings()

    # -------------------------------------------------------------------------------------------
    def accept(self):
        """
        DOCUMENT ME!
        """
        l_log = logging.getLogger("CDlgAnvEditNEW::accept")
        l_log.setLevel(logging.DEBUG)
        l_log.debug(" Accept editing data ...")

        # tráfego do exercício existe ?
        if (self._oTrf is not None):
            # salva edição do tráfego do exercício
            l_dctTrf = self.guiDataToDict()
            l_dctTrf["nTrf"] = self._oTrf.i_trf_id
            self._oTrf.load_trf(l_dctTrf)

        # senão, exercício não existe
        else:
            # salva novo tráfego do exercício
            self.acceptNew()

        # faz o "accept"
        QtGui.QDialog.accept(self)

    # -------------------------------------------------------------------------------------------
    def acceptNew(self):
        """
        DOCUMENT ME!
        """
        # cria um novo tráfego do exercício
        self._oTrf = clsTrf.CTrfNEW(self._model)
        assert (self._oTrf)

        # cria o novo tráfego do exercício
        self._oTrf.make_trf(self.guiDataToDict())

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

    # -------------------------------------------------------------------------------------------
    def configTexts(self):
        """
        DOCUMENT ME!
        """
        # configura títulos e mensagens
        self._txtSettings = "CDlgAnvEditNEW"

    # -------------------------------------------------------------------------------------------
    def fillComboBoxes(self):
        """
        carrega os comboboxes de prcoedimento e de performance de aeronaves
        :return:
        """
        # carrega as aeronaves definidas na tabela de performances
        llst_prf = []
        for ls_prf in self._model.dct_prf.keys():
            llst_prf.append(ls_prf)

        llst_prf.sort()
        self.cbxPrf.addItems(llst_prf)

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
        self.cbxProc.addItems(llst_proc)

    # -------------------------------------------------------------------------------------------
    def getData(self):
        """
        DOCUMENT ME!
        """
        # return
        return (self._oTrf)

    # -------------------------------------------------------------------------------------------
    def guiDataToDict(self):
        """

        :return:
        """
        l_log = logging.getLogger("CDlgAnvEditNEW::guiDataToDict")
        l_log.setLevel(logging.DEBUG)
        l_dctTrf = {}

        # identificação do tráfego
        l_dctTrf["nTrf"] = 0

        # indicativo do tráfego
        l_dctTrf["indicativo"] = str(self.qleInd.text()).strip()

        # performance
        l_dctTrf["designador"] = str(self.cbxPrf.currentText()).strip()

        # código transponder
        l_dctTrf["ssr"] = int(str(self.qleSSR.text()).strip())

        # aeródromo de origem
        l_dctTrf["origem"] = str(self.qleAdOri.text()).strip()

        # aeródromo de origem
        l_dctTrf["destino"] = str(self.qleAdDst.text()).strip()

        # procedimento
        l_dctTrf["procedimento"] = str(self.cbxProc.currentText()).strip()

        # tempo de ativação do tráfego
        l_dctTrf["temptrafego"] = int(str(self.qsbAtvPndMin.text()).strip())

        # posição da aeronave latitude e longitude da aeronave
        l_dctPos = {}
        l_dctPos["tipo"] = 'L'
        ls_cpoA = str(self.qsbPosX.text()).strip()
        ls_cpoA = ls_cpoA.replace(",", ".")
        l_dctPos["cpoA"] = ls_cpoA
        ls_cpoB = str(self.qsbPosY.text()).strip()
        ls_cpoB = ls_cpoB.replace(",", ".")
        l_dctPos["cpoB"] = ls_cpoB
        l_dctTrf["coord"] = l_dctPos

        # proa
        ls_proa = str(self.qsbNavPro.text()).strip()
        ls_proa = ls_proa.replace(",", ".")
        l_dctTrf["proa"] = ls_proa
        l_log.debug(" Proa [%s]" % ls_proa)

        # velocidade
        ls_vel = str(self.qsbNavVel.text()).strip()
        ls_vel = ls_vel.replace(",", ".")
        l_dctTrf["velocidade"] = ls_vel

        # altitude
        ls_alt = str(self.qsbNavAlt.text()).strip()
        ls_alt = ls_alt.replace(",", ".", 1)
        l_dctTrf["altitude"] = ls_alt

        return l_dctTrf

    # -------------------------------------------------------------------------------------------
    def reject(self):
        """
        DOCUMENT ME!
        """
        l_log = logging.getLogger("CDlgAnvEditNEW::reject")
        l_log.setLevel(logging.DEBUG)
        l_log.debug(" Set object trf to None ...")
        self._oTrf = None

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
    def updateTrfData(self):
        """
        atualiza na tela os a área de dados do tráfego do exercício selecionado
        """
        l_log = logging.getLogger("CDlgExeDataNEW::trfEdit")
        l_log.setLevel(logging.DEBUG)
        l_log.debug("Mostrar as informações de um tráfego do exercício")

        # tráfego exercício existe ?
        if (self._oTrf is not None):
            # identificação
            self.qleInd.setText(self._oTrf.s_trf_ind)

            # tipo da aeronave (QComboBox)
            self.cbxPrf.setCurrentIndex(self.cbxPrf.findText(self._oTrf.ptr_trf_prf.s_prf_id))

            # SSR
            self.qleSSR.setText(str(self._oTrf.i_trf_ssr))

            # aeródromo de origem
            self.qleAdOri.setText(self._oTrf.ptr_trf_aer_ori.s_aer_indc)

            # aeródromo de destino
            self.qleAdDst.setText(self._oTrf.ptr_trf_aer_dst.s_aer_indc)

            # procedimento (QComboBox)
            self.cbxProc.setCurrentIndex(self.cbxProc.findText(self._oTrf.s_trf_prc))

            # tempo de ativação (QSpinBox)
            li_HorIni, li_MinIni, li_SegIni = self._model.exe.t_exe_hor_ini
            li_MinIni = li_MinIni + (li_HorIni * 60) + (li_SegIni / 60)

            li_Hor, li_Min, li_Seg = self._oTrf.t_trf_hor_atv
            li_Min = li_Min + (li_Hor * 60) + (li_Seg / 60)
            self.qsbAtvPndMin.setValue(li_Min - li_MinIni)

            # latitude (QDoubleSpinBox)
            self.qsbPosX.setValue(self._oTrf.f_trf_lat)

            # longitude (QDoubleSpinBox)
            self.qsbPosY.setValue(self._oTrf.f_trf_lng)

            # proa (QDoubleSpinBox)
            self.qsbNavPro.setValue(self._oTrf.f_trf_pro_atu)

            # altitude (QDoubleSpinBox)
            lf_AltFt = self._oTrf.f_trf_alt_atu * cdefs.D_CNV_M2FT
            self.qsbNavAlt.setValue(lf_AltFt)

            # velocidade (QDoubleSpinBox)
            lf_VelKt = self._oTrf.f_trf_vel_atu * cdefs.D_CNV_MS2KT
            self.qsbNavVel.setValue(lf_VelKt)

        # senão, é um novo tráfego do exercício
        else:
            # posiciona cursor no início do formulário
            self.qleInd.setFocus()

# < the end >--------------------------------------------------------------------------------------
