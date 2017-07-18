#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_trj_data_new

mantém as informações sobre a dialog de edição da tabela de trajetórias

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
import os
import logging
import sys

# PyQt library
from PyQt4 import QtCore, QtGui

# libs
import libs.coords.coord_defs as cdefs

# view
import view.dbedit.dlg_brk_trj_edit_new as dlgBrk
import view.dbedit.dlg_trj_edit_new as dlgEdit
import view.dbedit.dlg_trj_data_new_ui as dlgData_ui

# control
import control.events.events_basic as events

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CDlgTrjDataNEW >---------------------------------------------------------------------------

class CDlgTrjDataNEW (QtGui.QDialog, dlgData_ui.Ui_CDlgTrjDataNEW):
    """
    mantém as informações sobre a dialog de edição da tabela de trajetórias
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control, f_parent=None):
        """
        constructor

        @param f_control: control manager do editor da base de dados
        @param f_parent: janela vinculada
        """
        # logger
        M_LOG.info("__init__:>>")

        # verifica parâmetros de entrada
        assert f_control

        # init super class
        super(CDlgTrjDataNEW, self).__init__(f_parent)

        # salva o control manager localmente
        self._control = f_control

        # obtém o event manager
        self._event = f_control.event
        assert self._event

        # obtém o gerente de configuração
        self._config = f_control.config
        assert self._config

        # obtém o dicionário de configuração
        self._dctConfig = self._config.dct_config
        assert self._dctConfig

        # obtém o model manager
        self._model = f_control.model
        assert self._model

        # salva a parent window localmente
        self._parent = f_parent

        # existe uma parent window ?
        if self._parent is not None:
            # esconde a parent window
            self._parent.setVisible(False)

        # pointer para a trajetória corrente
        self._oTrj = None

        # pointer para os dicionários a editar
        self._dctTrj = None

        # flag para indicar atualização na trajetória
        self._bChanged = False

        # monta a dialog
        self.setupUi(self)

        # configurações de conexões slot/signal
        self.configConnects()

        # configurações de títulos e mensagens da janela de edição
        self.configTexts()

        # restaura as configurações da janela de edição
        self.restoreSettings()

        # configura título da dialog
        self.setWindowTitle(u"dbEdit [ Edição de Trajetórias ]")

        # faz a carrga inicial do diretório de exercícios
        QtCore.QTimer.singleShot(0, self.loadInitial)

        # logger
        M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def accept(self):
        """
        callback de btnOk da dialog de edição
        faz o accept da dialog
        """
        # logger
        M_LOG.info("accept:>>")

        # ok para continuar ?
        if self.okToContinue():
            # gerar a mensagem de gravação das alterações no disco
            if self._bChanged == True:
                # Cria o evento para salvar no disco as tarjetórias
                l_evtSave2Disk = events.CSave2Disk(fs_table="TRJ")
                assert l_evtSave2Disk

                # dissemina o evento
                self._event.post(l_evtSave2Disk)

                # reseta a flag de alterações
                self._bChanged = False

            else:
                # refazer a leitura das trajetórias
                self._model.airspace.load_dicts()

                self._dctTrj = self._model.dct_trj

                self._oTrj = None

            # faz o "accept"
            QtGui.QDialog.accept(self)

            # fecha a janela de edição
            self.close()

        # logger
        M_LOG.info("accept:<<")

    # ---------------------------------------------------------------------------------------------
    def closeEvent(self, event):
        """
        callback de tratamento do evento Close

        @param  event : ..
        """
        # ok para continuar ?
        if self.okToContinue():
            # obtém os settings
            l_set = QtCore.QSettings()
            assert l_set

            # salva geometria da janela
            l_set.setValue("%s/Geometry" % (self._txtSettings),
                           QtCore.QVariant(self.saveGeometry()))

            # existe a parent window ?
            if self._parent is not None:
                # exibe a parent window
                self._parent.setVisible(True)

        # senão, ignora o request
        else:
            # ignora o evento
            event.ignore()

    # ---------------------------------------------------------------------------------------------
    def configConnects(self):
        """
        configura as conexões slot/signal
        """
        # conecta click a remoção da trajetória
        self.connect(self.btnTrjDel,
                     QtCore.SIGNAL("clicked()"),
                     self.trjDel)

        # conecta click a edição da trajetória
        self.connect(self.btnTrjEdit,
                       QtCore.SIGNAL("clicked()"),
                       self.trjEdit)

        # conecta click a inclusão da trajetória
        self.connect(self.btnTrjNew,
                     QtCore.SIGNAL("clicked()"),
                     self.trjNew)

        # conecta click a remoção do ponto da trajetória
        self.connect(self.btnPtoTrjDel,
                     QtCore.SIGNAL("clicked()"),
                     self.ptoTrjDel)

        # conecta click a edição do ponto da trajetória
        self.connect(self.btnPtoTrjEdit,
                     QtCore.SIGNAL("clicked()"),
                     self.ptoTrjEdit)

        # conecta click a inclusão do ponto da trajetória
        self.connect(self.btnPtoTrjNew,
                     QtCore.SIGNAL("clicked()"),
                     self.ptoTrjNew)

        # conecta click a seleção da linha da trajetória
        self.connect(self.qtwTrjTab,
                     QtCore.SIGNAL("itemSelectionChanged()"),
                     self.trjSelect)

        # conecta botão Ok
        self.connect(self.bbxTrjTab,
                     QtCore.SIGNAL("accepted()"),
                     self.accept)

        # conecta botão Cancela
        self.connect(self.bbxTrjTab,
                     QtCore.SIGNAL("rejected()"),
                     self.reject)

        # configura botões
        self.bbxTrjTab.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.bbxTrjTab.button(QtGui.QDialogButtonBox.Ok).setFocus()

    # ---------------------------------------------------------------------------------------------
    def configTexts(self):
        """
        configura títulos e mensagens
        """
        self._txtSettings = "CDlgTrjDataNEW"

        self._txtCancelMsg = u"As alterações pendentes serão perdidas.\n Deseja Continuar?"

        self._txtContinueTit = u"TrackS - Alterações pendentes"
        self._txtContinueMsg = u"Salva alterações pendentes ?"

        self._txtDelTrjTit = u"TrackS - Apaga a trajetória"
        self._txtDelTrjMsg = u"Apaga trajetória {0} ?"

        self._txtDelPtoTrjTit = u"TrackS - Apaga o ponto da trajetória"
        self._txtDelPtoTrjMsg = u"Apaga o ponto da trajetória {0} ?"

    # ---------------------------------------------------------------------------------------------
    def getCurrentData(self, f_qtwTab, f_iCol):
        """
        retorna os dados associados a linha selecionada
        """
        # logger
        M_LOG.info("getCurrentData:>>")
        M_LOG.debug("Obter os dados elemento selecionado")

        # verifica condições de execução
        assert f_qtwTab is not None

        # o dado da linha selecionada
        l_sData = ""

        # obtém o item da linha selecionada
        l_oItem = self.getCurrentItem(f_qtwTab, f_iCol)
        M_LOG.debug(" Dados do Item [%s]" % str(l_oItem.text()))

        # existe uma linha selecionada ?
        if l_oItem is not None:
            # obtém o dado associado a linha
            #l_sData = l_oItem.data(QtCore.Qt.UserRole).toString()
            l_sData = l_oItem.text()

        # logger
        M_LOG.info("getCurrentData:<<")

        # retorna o dado associado a linha selecionada
        return l_sData

    # ---------------------------------------------------------------------------------------------
    def getCurrentItem(self, f_qtwTab, f_iCol):
        """
        retorna o item associado a linha selecionada
        """
        # o item selecionado
        l_oItem = None

        # verifica condições de execução
        assert f_qtwTab is not None

        # obtém o número da linha selecionada
        l_iRow = f_qtwTab.currentRow()

        # existe uma linha selecionada ?
        if l_iRow > -1:
            # obtém o item associado
            l_oItem = f_qtwTab.item(l_iRow, f_iCol)
            assert l_oItem

        # retorna o item selecionado na lista
        return l_oItem

    # ---------------------------------------------------------------------------------------------
    def getCurrentSel(self, f_dct, f_qtw):
        """
        retorna o elemento associado a linha selecionada na lista
        """
        M_LOG.info("getCurrentSel:>>")
        # verifica condições de execução
        assert f_dct is not None
        assert f_qtw is not None

        # obtém o index da linha selecionada
        l_sID = self.getCurrentData(f_qtw, 0)
        M_LOG.debug("ID [%s]" % l_sID)
        l_iID = int(l_sID[3:])
        M_LOG.debug("ID [%s]" % str(l_iID))

        # indice válido ?
        if l_iID in f_dct:
            # obtém o elemento selecionado se existir uma linha selecionada
            l_oSel = f_dct[l_iID]
            assert l_oSel

        # senão, índice inválido
        else:
            # não há elemento selecionado
            l_oSel = None

        M_LOG.info("getCurrentSel:<<")

        # retorna o elemento da linha selecionada na lista
        return l_oSel

    # ---------------------------------------------------------------------------------------------
    def loadInitial(self):
        """
        faz a carga inicial da tabela de exercícios
        """
        # logger
        M_LOG.info("loadInitial:>>")
        M_LOG.debug("caregando as trajetórias ...")

        # obtém o dicionário de trajetórias
        self._dctTrj = self._model.dct_trj

        # o dicionário de trajetótias não existe ?
        if self._dctTrj is None:
            # logger
            M_LOG.critical(u"<E01: Tabela de trajetórias não carregada !")

            # cria um evento de quit
            l_evtQuit = events.CQuit()
            assert l_evtQuit

            # dissemina o evento
            self._event.post(l_evtQuit)

            # cai fora..
            sys.exit(1)

        # atualiza na tela os dados da tabela de trajetórias
        self.trjUpdateList()
        M_LOG.info("loadInitial:<<")

    # ---------------------------------------------------------------------------------------------
    def okToContinue(self):
        """
        cria uma messageBox

        @return True se tratou a resposta, senão False
        """
        # flag de alterações setado ?
        if(self._bChanged):
            # questiona sobre alterações pendentes
            l_Resp = QtGui.QMessageBox.question(self, self._txtContinueTit,
                                                self._txtContinueMsg,
                                                QtGui.QMessageBox.Yes |
                                                QtGui.QMessageBox.No)

            # não salva as alterações pendentes ?
            if(QtGui.QMessageBox.No == l_Resp):
                # salva as pendências e sai
                self._bChanged = False

        # não houve alterações pendentes ?
        else:
           # reseta o flag de alterações..
           self._bChanged = False

        # return
        return True

    # ---------------------------------------------------------------------------------------------
    def ptoTrjDel(self):
        """

        :return:
        """
        pass
        # verifica condições de execução
        assert self._oTrj is not None
        assert self._oTrj.lst_trj_brk is not None

        # obtém o número da linha selecionada
        l_iRow = self.qtwTabPtoTrj.currentRow()

        if l_iRow >= 0 and l_iRow < len(self._oTrj.lst_trj_brk):
            # apaga o ponto da trajetória atual ?
            if QtGui.QMessageBox.Yes == QtGui.QMessageBox.question(self,
               self._txtDelPtoTrjTit,
               self._txtDelPtoTrjMsg.format(self._oTrj.lst_trj_brk[l_iRow].i_brk_id),
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No):
                # apaga o tráfego do exercício
                self.ptoTrjRemove(l_iRow)

    # ---------------------------------------------------------------------------------------------
    def ptoTrjEdit(self):
        """
        atualiza o ponto da trajetória da lista

        :return:
        """
        # logger
        M_LOG.info("ptoTrjEdit:>>")
        M_LOG.debug("Editar um ponto da trajetória")

        # verifica condições de execução
        assert self.qtwTabPtoTrj is not None
        assert self._oTrj is not None
        assert self._oTrj.lst_trj_brk is not None

        # obtém o número oo ponto da trajetória selecionado
        l_iRow = self.qtwTabPtoTrj.currentRow()
        l_oBrkTrj = self._oTrj.lst_trj_brk[l_iRow]

        if (l_iRow >=0) and (l_iRow < len(self._oTrj.lst_trj_brk)):
            # cria a dialog de edição do ponto da trajetória
            l_Dlg = dlgBrk.CDlgBrkTrjEditNEW(self._control, l_oBrkTrj, self)
            assert l_Dlg

            # processa a dialog de edição do ponto da trajetória (modal)
            if(l_Dlg.exec_ ()):
                # obtém os dados alterados
                l_oBrkTrj = l_Dlg.getData()
                M_LOG.debug("Tráfego Id [%s]" % str(l_oBrkTrj.i_brk_id))

                # ponto da trajetória existente ?
                if (l_oBrkTrj is not None) and (self._oTrj is not None):
                    # atualiza o tráfego do exercício na lista
                    self._oTrj.lst_trj_brk[l_iRow] = l_oBrkTrj

                    # atualiza a trajetória no dicionário de trajetórias
                    self._dctTrj[self._oTrj.i_prc_id] = self._oTrj

                    # se ok, atualiza a QTableWidget de pontos trajetórias
                    self.ptoTrjUpdateWidget()

                    # sinaliza que houve alteração em um ponto da trajetória
                    self._bChanged = True

        M_LOG.info("ptoTrjEdit:>>")

    # ---------------------------------------------------------------------------------------------
    def ptoTrjNew(self):
        """
        cria um novo ponto da trajetória
        """
        # logger
        M_LOG.info("ptoTrjNew:>>")
        ls_TrjId = "TRJ" + str(self._oTrj.i_prc_id).zfill(3)
        M_LOG.debug("Um novo ponto da trajetória [%s]" % ls_TrjId)

        # cria a dialog de edição de pontos da trajetória
        l_Dlg = dlgBrk.CDlgBrkTrjEditNEW(self._control, None, self)
        assert l_Dlg

        # processa a dialog de edição de pontos da trajetória
        if l_Dlg.exec_():
            # obtém os dados da edição
            l_oBrkTrj = l_Dlg.getData()
            # atualiza o número do breakpoint
            l_oBrkTrj.i_brk_id = len(self._oTrj.lst_trj_brk) + 1
            M_LOG.debug("Número do novo breakpoint [%d]" % l_oBrkTrj.i_brk_id)

            for l_oBrk in self._oTrj.lst_trj_brk:
                M_LOG.debug("Número do breakpoint [%d]" % l_oBrk.i_brk_id)

            # trajetória existente ?
            if (l_oBrkTrj is not None) and (self._oTrj is not None):
                # insere o tráfego do exercício na lista
                self._oTrj.lst_trj_brk.append(l_oBrkTrj)

                # atualiza o exercicio no dicionário de exercícios
                self._dctTrj[self._oTrj.i_prc_id] = self._oTrj

                # se ok, atualiza a QTableWidget de pontos da trajetória
                self.ptoTrjUpdateWidget()

                # sinaliza que houve a inclusão de um novo breakpoint na trajetória
                self._bChanged = True

        # logger
        M_LOG.info("ptoTrjNew:<<")

    # ---------------------------------------------------------------------------------------------
    def ptoTrjRemove(self, f_iIndex):
        """
        Deleta um ponto da trajetória
        :param f_index:
        :return:
        """
        # logger
        M_LOG.info("ptoTrjRemove:>>")

        M_LOG.debug(u"Índice a ser removido [%s]" % str(f_iIndex))
        # removendo o elemento da lista
        M_LOG.debug("Lista [%s]" % self._oTrj.lst_trj_brk)
        l_lstBrk = self._oTrj.lst_trj_brk;
        del l_lstBrk[f_iIndex]

        # atualiza a lista
        M_LOG.debug("Atualizando os id dos breakpoints")
        for l_iIndex, l_oBrk in enumerate(l_lstBrk):
            M_LOG.debug ("Anterior [%d] Atual [%d]" % (l_oBrk.i_brk_id, l_iIndex + 1))
            l_oBrk.i_brk_id = l_iIndex + 1

        self._oTrj.lst_trj_brk = l_lstBrk

        # deleta o ponto da lista de pontos da trajetória
        self.qtwTabPtoTrj.removeRow(self.qtwTabPtoTrj.currentRow())

        # sinaliza que houve alteração nos breakpoints da trajetória
        self._bChanged = True

        # logger
        M_LOG.info("ptoTrjRemove:<<")

    # ---------------------------------------------------------------------------------------------
    def ptoTrjUpdateWidget(self):
        """
        atualiza na tela os dados da QtableWidget de pontos da trajetória

        :return:
        """
        # logger
        M_LOG.info("ptoTrjUpdateWidget:>>")
        M_LOG.debug("Atualizando a tabela de pontos da trajetória")

        for li_row in range(self.qtwTabPtoTrj.rowCount()):
            self.qtwTabPtoTrj.removeRow(li_row)

        self.qtwTabPtoTrj.setRowCount(0)
        self.qtwTabPtoTrj.setColumnCount(8)
        self.qtwTabPtoTrj.setHorizontalHeaderLabels(
            ["Tipo", "Campo A", "Campo B", "Campo C", "Campo D", "Altitude (ft)", "Velocidade (kt)", "Procedimento"])
        self.qtwTabPtoTrj.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.qtwTabPtoTrj.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.qtwTabPtoTrj.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
        self.qtwTabPtoTrj.setSelectionMode(QtGui.QTableWidget.SingleSelection)

        li_row = 0

        # para todas as linhas da tabela...
        M_LOG.debug(" Número de pontos da trajetória [%s]" % len(self._oTrj.lst_trj_brk))
        for l_oBrkNew in self._oTrj.lst_trj_brk:
            # cria nova linha na tabela
            self.qtwTabPtoTrj.insertRow(li_row)

            # tipo de coordenada
            lqtwi_item = QtGui.QTableWidgetItem(l_oBrkNew.s_brk_tipo)
            lqtwi_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.qtwTabPtoTrj.setItem(li_row, 0, lqtwi_item)

            # campo A
            lqtwi_item = QtGui.QTableWidgetItem(l_oBrkNew.s_brk_cpoA)
            lqtwi_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.qtwTabPtoTrj.setItem(li_row, 1, lqtwi_item)

            # campo B
            lqtwi_item = QtGui.QTableWidgetItem(l_oBrkNew.s_brk_cpoB)
            lqtwi_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.qtwTabPtoTrj.setItem(li_row, 2, lqtwi_item)

            # campo C
            ls_Value = l_oBrkNew.s_brk_cpoC
            if l_oBrkNew.s_brk_tipo == 'L' or l_oBrkNew.s_brk_tipo == 'G':
                lf_AltFt = float(ls_Value) * cdefs.D_CNV_M2FT
                ls_Value = str(lf_AltFt)
            lqtwi_item = QtGui.QTableWidgetItem(ls_Value)
            lqtwi_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.qtwTabPtoTrj.setItem(li_row, 3, lqtwi_item)

            # campo D
            lqtwi_item = QtGui.QTableWidgetItem(l_oBrkNew.s_brk_cpoD)
            lqtwi_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.qtwTabPtoTrj.setItem(li_row, 4, lqtwi_item)

            # altitude
            lf_AltFt = l_oBrkNew.f_brk_alt * cdefs.D_CNV_M2FT
            lqtwi_item = QtGui.QTableWidgetItem(str(lf_AltFt))
            lqtwi_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.qtwTabPtoTrj.setItem(li_row, 5, lqtwi_item)

            # velocidade
            lf_VelKt = l_oBrkNew.f_brk_vel * cdefs.D_CNV_MS2KT
            lqtwi_item = QtGui.QTableWidgetItem(str(lf_VelKt))
            lqtwi_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.qtwTabPtoTrj.setItem(li_row, 6, lqtwi_item)

            # procedimento
            lqtwi_item = QtGui.QTableWidgetItem(l_oBrkNew.s_brk_prc)
            lqtwi_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.qtwTabPtoTrj.setItem(li_row, 7, lqtwi_item)

            li_row = li_row + 1

        # redefine o tamanho da QTableWidget
        self.qtwTabPtoTrj.resizeRowsToContents()
        self.qtwTabPtoTrj.resizeColumnsToContents()

    # ---------------------------------------------------------------------------------------------
    def reject(self):
        """
        DOCUMENT ME!
        """
        # logger
        M_LOG.info("reject:>>")

        #self._oExe = None

        if self._bChanged:
            # questiona sobre alterações pendentes
            l_Resp = QtGui.QMessageBox.question(self, self._txtContinueTit,
                                                self._txtCancelMsg,
                                                QtGui.QMessageBox.Yes |
                                                QtGui.QMessageBox.No)

            # não cancelar as alterações pendentes ?
            if (QtGui.QMessageBox.No == l_Resp):
                # logger
                M_LOG.info("reject:<< cancelado!")
                return

        # faz o "reject"
        QtGui.QDialog.reject(self)

        # ajusta a flag de alterações
        self._bChanged = False

        # faz a releitura das trajetórias
        self._model.airspace.load_dicts()
        self._dctTrj = self._model.dct_trj
        self._oTrj = None

        # close dialog
        self.close()

        # logger
        M_LOG.info("reject:<<")

    # ---------------------------------------------------------------------------------------------
    def restoreSettings(self):
        """
        restaura as configurações salvas para esta janela
        """
        # obtém os settings
        l_set = QtCore.QSettings("sophosoft", "dbedit")
        assert l_set

        # restaura geometria da janela
        self.restoreGeometry(l_set.value("%s/Geometry" % (self._txtSettings)).toByteArray())

        # return
        return True

    # ---------------------------------------------------------------------------------------------
    def show(self):
        """

        :return:
        """
        # show super class
        super(CDlgTrjDataNEW, self).show()

        # faz a carrga inicial do diretório de trajetórias
        QtCore.QTimer.singleShot(0, self.loadInitial)

    # ---------------------------------------------------------------------------------------------
    def trjDel(self):
        """
        callback de btnDel da dialog de edição
        deleta uma trajetória da lista
        """
        pass
        # verifica condições de execução
        assert self.qtwTrjTab is not None
        assert self._dctTrj is not None

        # obtém a trajetória selecionado
        self._oTrj = self.getCurrentSel(self._dctTrj, self.qtwTrjTab)

        if self._oTrj is not None:
            # apaga a trajetória atual ?
            l_sTrjID = "TRJ" + str(self._oTrj.i_prc_id).zfill(3)
            if QtGui.QMessageBox.Yes == QtGui.QMessageBox.question(self,
               self._txtDelTrjTit,
               self._txtDelTrjMsg.format(l_sTrjID),
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No):

                # apaga a trajetória
                self.trjRemove(self._oTrj)

    # ---------------------------------------------------------------------------------------------
    def trjEdit(self):
        """
        callback de btnEdit da dialog de edição
        edita uma trajetória da QTableWidget
        """
        pass
        # verifica condições de execução
        assert self.qtwTrjTab is not None
        assert self._dctTrj is not None

        # obtém a trajetória selecionada
        self._oTrj = self.getCurrentSel(self._dctTrj, self.qtwTrjTab)

        if(self._oTrj is not None):
            # cria a dialog de edição da trajetória
            l_Dlg = dlgEdit.CDlgTrjEditNEW(self._control, self._oTrj, self)
            assert l_Dlg

            # processa a dialog de edição da trajetória (modal)
            if(l_Dlg.exec_ ()):
                # obtém os dados alterados
                self._oTrj = l_Dlg.getData()

                # trajetória existente ?
                if (self._oTrj is not None) and (self._dctTrj is not None):
                    # atualiza a trajetória no dicionário de trajetórias
                    self._dctTrj[self._oTrj.i_prc_id] = self._oTrj

                    # se ok, atualiza a QTableWidget de trajetórias
                    self.trjUpdateWidget ()

                    # sinaliza que houve alteração na trajetória
                    self._bChanged = True

    # ---------------------------------------------------------------------------------------------
    def trjNew(self):
        """
        callback de btnNew da dialog de edição
        cria uma nova trajetória na lista
        """
        pass
        # cria a dialog de edição da trajetória
        l_Dlg = dlgEdit.CDlgTrjEditNEW(self._control, None, self)
        assert l_Dlg

        # processa a dialog de edição da trajetória (modal)
        if l_Dlg.exec_():
            # obtém os dados da edição
            self._oTrj = l_Dlg.getData()

            # trajetória existente ?
            if (self._oTrj is not None) and (self._dctTrj is not None):
                # insere a trajetória na lista
                self._dctTrj[self._oTrj.i_prc_id] = self._oTrj

                # se ok, atualiza a QTableWidget de trajetórias
                self.trjUpdateWidget()

                # sinaliza que houve a inclusão de uma nova trajetória
                self._bChanged = True

    # ---------------------------------------------------------------------------------------------
    def trjRemove(self, f_oTrj):
        """
        remove o exercício selecionado

        @param  f_oExe : pointer para o exercício a remover
        """
        # verifica condições de execução
        assert f_oTrj is not None

        # remove a linha da widget
        self.qtwTrjTab.removeRow(self.qtwTrjTab.currentRow())

        # atualiza o dicionário de trajetórias
        del self._dctTrj[f_oTrj.i_prc_id]

        # sinaliza que houve alteração nos dados
        self._bChanged = True

    # ---------------------------------------------------------------------------------------------
    def trjSelect(self):
        """
        seleciona uma trajetória
        """
        pass
        # verifica condições de execução
        assert self._dctTrj is not None
        assert self.qtwTrjTab is not None

        # obtém a trajetória selecionado
        self._oTrj = self.getCurrentSel(self._dctTrj, self.qtwTrjTab)

        # atualiza a área de dados da trajetória selecionada
        self.trjUpdateSel()

    # ---------------------------------------------------------------------------------------------
    def trjUpdateList(self):
        """
        atualiza na tela os dados das trajeórias
        """
        # verifica condições de execução
        assert self._dctTrj is not None
        assert self.qtwTrjTab is not None

        # atualiza a QTableWidget de trajetória
        self.trjUpdateWidget()

        # obtém o exercício selecionado
        self._oTrj = self.getCurrentSel(self._dctTrj, self.qtwTrjTab)

    # ---------------------------------------------------------------------------------------------
    def trjUpdateSel(self):
        """
        atualiza na tela os dados da trajetória selecionado
        """
        # logger
        M_LOG.info("trjUpdateSel:>>")

        # trajetória selecionada existe ?
        if self._oTrj is not None:
            # indicativo da trajetória
            l_sTrjID = "TRJ" + str(self._oTrj.i_prc_id).zfill(3)

            # identificação
            self.txtPrcID.setText(l_sTrjID)
            self.qlePrcDesc.setText(self._oTrj.s_prc_desc)

            # atualiza a lista de pontos da trajetória
            self.ptoTrjUpdateWidget()

        # senão, a trajetória não existe
        else:
            # posiciona cursor no início do formulário
            self.txtPrcID.setFocus()

        # logger
        M_LOG.info("trjUpdateSel:<<")

    # ---------------------------------------------------------------------------------------------
    def trjUpdateWidget(self):
        """
        atualiza na tela os dados da QTableWidget de exercícios
        """
        M_LOG.info("trjUpdateWidget:>>")
        M_LOG.debug(" carrega os procedimentos de trajetória na GUI ...")

        # verifica condições de execução
        assert self.qtwTrjTab is not None
        assert self._dctTrj is not None

        # limpa a QTableWidget
        self.qtwTrjTab.clear()

        # seta o número de linhas da QTableWidget para o tamanho da lista
        self.qtwTrjTab.setRowCount(len(self._dctTrj))

        # seta número de colunas e cabeçalho das colunas
        self.qtwTrjTab.setColumnCount(2)
        self.qtwTrjTab.setHorizontalHeaderLabels([u"Indicativo", u"Descrição"])

        # seta QTableWidget
        self.qtwTrjTab.setAlternatingRowColors(True)
        self.qtwTrjTab.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.qtwTrjTab.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
        self.qtwTrjTab.setSelectionMode(QtGui.QTableWidget.SingleSelection)
        self.qtwTrjTab.setSortingEnabled(False)

        # linha selecionada (objeto trajetória)
        l_oSItem = None

        # para cada trajetória no dicionário..
        for l_iNdx, l_iTrjID in enumerate(sorted(self._dctTrj.keys())):
            # indicativo da trajetória
            ls_IndTrj = "TRJ" + str(l_iTrjID).zfill(3)
            l_twiTrjID = QtGui.QTableWidgetItem(ls_IndTrj)
            l_twiTrjID.setData(QtCore.Qt.UserRole, QtCore.QVariant(str(l_iTrjID)))

            self.qtwTrjTab.setItem(l_iNdx, 0, l_twiTrjID)

            # é a trajetória selecionado ?
            if (self._oTrj is not None) and (self._oTrj.i_prc_id == l_iTrjID):
                # salva pointer para o item selecionado
                l_oSItem = l_twiTrjID

            # obtém a trajetória
            l_oTrj = self._dctTrj[l_iTrjID]
            assert l_oTrj

            # descrição
            l_twiExeDesc = QtGui.QTableWidgetItem(l_oTrj.s_prc_desc)
            M_LOG.debug(" Trj ID [%s] Descricao [%s]" % (str(l_oTrj.i_prc_id), l_twiExeDesc.text()))
            M_LOG.debug(" Quantidade de trajetórias [%d]" % len(self._dctTrj))

            self.qtwTrjTab.setItem(l_iNdx, 1, l_twiExeDesc)

        # existe uma trajetória selecionado ?
        if self._oTrj is not None:
            # seleciona o item
            self.qtwTrjTab.setCurrentItem(l_oSItem)

            # posiciona no item selecionado
            self.qtwTrjTab.scrollToItem(l_oSItem)

            # marca que existe seleção
            l_oSItem.setSelected(True)

        # senão, não existe um exercício selecionado
        else:
            # seleciona a primeira linha
            self.qtwTrjTab.selectRow(0)

            # obtém o exercício atual
            self._oTrj = self.getCurrentSel(self._dctTrj, self.qtwTrjTab)
            # assert self._oExe

        # ajusta o tamanho das colunas pelo conteúdo
        self.qtwTrjTab.resizeColumnsToContents()

        # habilita a ordenação
        self.qtwTrjTab.setSortingEnabled(True)

        M_LOG.info("trjUpdateWidget:<<")

# < the end >--------------------------------------------------------------------------------------
