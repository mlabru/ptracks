#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------------------------
dlg_trj_edit_new

mantém as informações sobre a dialog de edição de trajetória

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
-------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Ivan Matias"
__date__ = "2017/07"

# < imports >------------------------------------------------------------------------------------

# python library
import logging
import os

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

# model
import model.items.trj_new as clsTrj

# view
import view.dbedit.dlg_trj_edit_new_ui as CDlgTrjEditNEW_ui

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CDlgExeEditNEW >------------------------------------------------------------------------

class CDlgTrjEditNEW (QtGui.QDialog, CDlgTrjEditNEW_ui.Ui_CDlgTrjEditNEW):
    """
    mantém as informações sobre a dialog de trajetória
    """
    # -------------------------------------------------------------------------------------------
    def __init__(self, f_control, f_oTrj=None, f_parent=None):
        """
        constructor
        cria uma dialog de edição de trajetória

        @param f_control : control manager do editor da base de dados
        @param f_oTrj : trajetória a editar
        @param f_parent : janela vinculada
        """
        # verifica parâmetros de entrada
        assert (f_control)

        # init super class
        super(CDlgTrjEditNEW, self).__init__(f_parent)

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
        self._oTrj = f_oTrj

        # pathnames
        self._sPN = None

        # monta a dialog
        self.setupUi(self)

        # configura título da dialog
        if self._oTrj:
            self.setWindowTitle(self.tr(u"Edição de Trajetória"))
            self.qlePrcID.setReadOnly(True)

        else:
            self.setWindowTitle(self.tr(u"Nova Trajetória"))
            self.qlePrcID.setReadOnly(False)

        # atualiza na tela os dados da trajetória
        self.updateTrjData()

        # configura botões
        self.bbxTrj.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.bbxTrj.button(QtGui.QDialogButtonBox.Ok).setFocus()

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
        # logger
        M_LOG.info("accept:>>")
        M_LOG.debug(" Accept editing data ...")

        # trajetória existe ?
        if (self._oTrj is not None):
            # salva edição da trajetória
            self.acceptEdit()

        # senão, trajetória não existe
        else:
            # salva a nova trajetória
            self.acceptNew()

        # logger
        M_LOG.info("accept:<<")

        # faz o "accept"
        QtGui.QDialog.accept(self)

    # -------------------------------------------------------------------------------------------
    def acceptEdit(self):
        """
        DOCUMENT ME!
        """
        # dicionário de modificações
        l_dctAlt = {}

        # identificação

        # descrição
        l_sDsc = str(self.qlePrcDesc.text()).strip()

        if (self._oTrj.s_prc_desc != l_sDsc):
            l_dctAlt["descricao"] = l_sDsc

        # atualiza a trajetória
        self._oTrj.load_trj(l_dctAlt)

    # -------------------------------------------------------------------------------------------
    def acceptNew(self):
        """
        DOCUMENT ME!
        """
        # cria uma nova trajetória
        self._oTrj = clsTrj.CTrjNEW(self._model)
        assert (self._oTrj)

        # dicionário da nova trajetória
        l_dctNew = {}

        # indicativo
        l_dctNew["nTrj"] = int(str(self.qlePrcID.text()).strip()[3:])

        # descrição
        l_dctNew["descricao"] = str(unicode(self.qlePrcDesc.text())).strip()

        # cria a nova trajetória
        self._oTrj.make_trj(l_dctNew)

    # -------------------------------------------------------------------------------------------
    def configConnects(self):
        """
        configura as conexões slot/signal
        """
        # conecta botão Ok
        self.connect(self.bbxTrj,
                     QtCore.SIGNAL("accepted()"),
                     self.accept)

        # conecta botão Cancela
        self.connect(self.bbxTrj,
                     QtCore.SIGNAL("rejected()"),
                     self.reject)

        # conect fim de edição da chave
        if self.qlePrcID.isReadOnly() is False:
            self.connect(self.qlePrcID,
                         QtCore.SIGNAL("editingFinished()"),
                         self.editingFinished)

    # -------------------------------------------------------------------------------------------
    def configTexts(self):
        """
        DOCUMENT ME!
        """
        # configura títulos e mensagens
        self._txtSettings = "CDlgTrjEditNEW"

    # -------------------------------------------------------------------------------------------
    def editingFinished(self):
        """
        Verifica se o indicativo da trajetória já existe e se é válido.
        """
        # logger
        M_LOG.info("editingFinished:>>")

        # obtém a chave digitada
        l_sPrcID = str (self.qlePrcID.text()).strip()
        M_LOG.debug(" Data retrieve [%s]" % l_sPrcID)

        l_sInd = l_sPrcID[0:3].strip().upper()

        # Verifica se o indicativo da trajetória começa com TRJ
        if l_sInd != "TRJ":
            M_LOG.debug("Key invalid [%s]" % l_sPrcID)
            QtGui.QMessageBox.warning(self, self.tr("Erro"),
                                      self.tr(u"Indicativo da trajetória inválido!"))
            self.qlePrcID.setFocus()

        l_sID = str(self.qlePrcID.text()).strip()[3:]

        # Verifica se o restante do indicativo da trajetória contém somente números.
        if l_sID.isdigit() is False:
            M_LOG.debug("Key invalid [%s]" % l_sPrcID)
            QtGui.QMessageBox.warning(self, self.tr("Erro"),
                                      self.tr(u"Indicativo da trajetória inválido!"))
            self.qlePrcID.setFocus()

        l_iPrcID = int(l_sID)

        if l_iPrcID in self._model.dct_trj:
            M_LOG.debug("Key already exists [%s]" % l_sPrcID)
            QtGui.QMessageBox.warning(self, self.tr("Erro"),
                                      self.tr(u"Indicativo da trajetória já existe!"))
            self.qlePrcID.setFocus()

    # -------------------------------------------------------------------------------------------
    def getData(self):
        """
        DOCUMENT ME!
        """
        # return
        return (self._oTrj)

    # -------------------------------------------------------------------------------------------
    def reject(self):
        """
        DOCUMENT ME!
        """
        # logger
        M_LOG.info("reject:>>")
        M_LOG.debug(" Set object trj to None ...")
        self._oTrj = None

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
    def updateTrjData(self):
        """
        atualiza na tela os a área de dados da trajetória selecionado
        """
        # trajetória existe ?
        if (self._oTrj is not None):
            # identificação
            ls_IndTrj = "TRJ" + str(self._oTrj.i_prc_id).zfill(3)
            self.qlePrcID.setText(ls_IndTrj)
            self.qlePrcDesc.setText(self._oTrj.s_prc_desc)

        # senão, é uma nova trajetória
        else:
            # posiciona cursor no início do formulário
            self.qlePrcID.setFocus()

# < the end >--------------------------------------------------------------------------------------
