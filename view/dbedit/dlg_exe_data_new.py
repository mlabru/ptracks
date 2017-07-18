#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_exe_data_new

mantém as informações sobre a dialog de edição da tabela de exercícios

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

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import os
import logging
import sys

# PyQt library
from PyQt4 import QtCore, QtGui

# libs
import libs.coords.coord_defs as cdefs

# model
import model.items.exe_data as dctExe

# view
import view.dbedit.dlg_exe_edit_new as dlgEdit
import view.dbedit.dlg_exe_data_new_ui as dlgData_ui
import view.dbedit.dlg_anv_edit_new as dlgAnv

# control
import control.events.events_basic as events
import control.events.events_config as evtConfig

# < class CDlgExeDataNEW >---------------------------------------------------------------------------

class CDlgExeDataNEW (QtGui.QDialog, dlgData_ui.Ui_CDlgExeDataNEW):
    """
    mantém as informações sobre a dialog de edição da tabela de exercícios
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control, f_parent=None):
        """
        constructor

        @param f_control: control manager do editor da base de dados
        @param f_parent: janela vinculada
        """
        # verifica parâmetros de entrada
        assert f_control

        # init super class
        super(CDlgExeDataNEW, self).__init__(f_parent)

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

        # pointer para os itens correntes
        self._oExe = None

        # pointer para os dicionários a editar
        self._dctExe = None

        # monta a dialog
        self.setupUi(self)

        # configurações de conexões slot/signal
        self.configConnects()

        # configurações de títulos e mensagens da janela de edição
        self.configTexts()

        # restaura as configurações da janela de edição
        self.restoreSettings()

        # configura título da dialog
        self.setWindowTitle(u"dbEdit [ Edição de Exercícios ]")

        # Não permitir a inclusão e exclusão exercícios e de tráfegos do exercício
        self.btnExeNew.setEnabled(False)
        self.btnExeDel.setEnabled(False)
        self.btnTrfNew.setEnabled(False)
        self.btnTrfDel.setEnabled(False)


        # faz a carrga inicial do diretório de exercícios
        QtCore.QTimer.singleShot(0, self.loadInitial)

    # ---------------------------------------------------------------------------------------------
    def accept(self):
        """
        callback de btnOk da dialog de edição
        faz o accept da dialog
        """
        # ok para continuar ?
        if self.okToContinue():
            # faz o "accept"
            QtGui.QDialog.accept(self)

            # fecha a janela de edição
            self.close()

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
        # exercício

        # conecta click a remoção de exercício
        self.connect(self.btnExeDel,
                     QtCore.SIGNAL("clicked()"),
                     self.exeDel)

        # conecta click a edição de exercício
        self.connect(self.btnExeEdit,
                       QtCore.SIGNAL("clicked()"),
                       self.exeEdit)

        # conecta click a inclusão de exercício
        self.connect(self.btnExeNew,
                     QtCore.SIGNAL("clicked()"),
                     self.exeNew)

        # conecta click a remoção do tráfego do exercício
        self.connect(self.btnTrfDel,
                     QtCore.SIGNAL("clicked()"),
                     self.trfDel)

        # conecta click a edição do tráfego do exercício
        self.connect(self.btnTrfEdit,
                     QtCore.SIGNAL("clicked()"),
                     self.trfEdit)

        # conecta click a inclusão do tráfego do exercício
        self.connect(self.btnTrfNew,
                     QtCore.SIGNAL("clicked()"),
                     self.trfNew)

        # conecta click a seleção da linha
        self.connect(self.qtwExeTab,
                     QtCore.SIGNAL("itemSelectionChanged()"),
                     self.exeSelect)

        # conecta botão Ok
        self.connect(self.bbxExeTab,
                     QtCore.SIGNAL("accepted()"),
                     self.accept)

        # conecta botão Cancela
        self.connect(self.bbxExeTab,
                     QtCore.SIGNAL("rejected()"),
                     self.reject)

        # configura botões
        self.bbxExeTab.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.bbxExeTab.button(QtGui.QDialogButtonBox.Ok).setFocus()

    # ---------------------------------------------------------------------------------------------
    def configTexts(self):
        """
        configura títulos e mensagens
        """
        self._txtSettings = "CDlgExeDataNEW"

        # self._txtContinueTit = u"TrackS - Alterações pendentes"
        # self._txtContinueMsg = u"Salva alterações pendentes ?"

        self._txtDelExeTit = u"TrackS - Apaga exercício"
        self._txtDelExeMsg = u"Apaga exercício {0} ?"

        self._txtDelTrfTit = u"TrackS - Apaga o tráfego do exercício"
        self._txtDelTrfMsg = u"Apaga o tráfego do exercício {0} ?"

    # ---------------------------------------------------------------------------------------------
    def exeDel(self):
        """
        callback de btnDel da dialog de edição
        deleta um exercício da lista
        """
        # verifica condições de execução
        assert self.qtwExeTab is not None
        assert self._dctExe is not None

        # obtém o exercício selecionado
        self._oExe = self.getCurrentSel(self._dctExe, self.qtwExeTab)

        if self._oExe is not None:
            # apaga o exercício atual ?
            if QtGui.QMessageBox.Yes == QtGui.QMessageBox.question(self,
               self._txtDelExeTit,
               self._txtDelExeMsg.format(self._oExe.s_exe_id),
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No):

                # apaga o exercício
                self.exeRemove(self._oExe)

    # ---------------------------------------------------------------------------------------------
    def exeEdit(self):
        """
        callback de btnEdit da dialog de edição
        edita um exercício da QTableWidget
        """
        # verifica condições de execução
        assert self.qtwExeTab is not None
        assert self._dctExe is not None

        # obtém o exercício selecionado
        self._oExe = self.getCurrentSel(self._dctExe, self.qtwExeTab)

        if(self._oExe is not None):
            # cria a dialog de edição de exercícios
            l_Dlg = dlgEdit.CDlgExeEditNEW(self._control, self._oExe, self)
            assert l_Dlg

            # processa a dialog de edição de exercícios (modal)
            if(l_Dlg.exec_ ()):
                # obtém os dados alterados
                self._oExe = l_Dlg.getData()

                # exercício existente ?
                if (self._oExe is not None) and (self._dctExe is not None):
                    # atualiza o exercicio no dicionário de exercícios
                    self._dctExe[self._oExe.s_exe_id] = self._oExe

                    # Cria o evento para salvar no disco o exercício atualizado
                    l_evtUpd2Disk = events.CUpd2Disk(fs_table="EXE", fs_filename=self._oExe.s_exe_id)
                    assert l_evtUpd2Disk

                    # dissemina o evento
                    self._event.post(l_evtUpd2Disk)

                    # se ok, atualiza a QTableWidget de exercícios
                    self.exeUpdateWidget ()

    # ---------------------------------------------------------------------------------------------
    def exeNew(self):
        """
        callback de btnNew da dialog de edição
        cria um novo exercício na lista
        """
        # cria a dialog de edição de exercícios
        l_Dlg = dlgEdit.CDlgExeEditNEW(self._control, None, self)
        assert l_Dlg

        # processa a dialog de edição de exercícios (modal)
        if l_Dlg.exec_():
            # obtém os dados da edição
            self._oExe = l_Dlg.getData()

            # exercício existente ?
            if (self._oExe is not None) and (self._dctExe is not None):
                # insere o exercício na lista
                self._dctExe[self._oExe.s_exe_id] = self._oExe

                # Cria o evento para salvar no disco os exercícios
                l_evtSave2Disk = events.CSave2Disk(fs_table="EXE")
                assert l_evtSave2Disk

                # dissemina o evento
                self._event.post(l_evtSave2Disk)

                # se ok, atualiza a QTableWidget de exercícios
                self.exeUpdateWidget()

    # ---------------------------------------------------------------------------------------------
    def exeRemove(self, f_oExe):
        """
        remove o exercício selecionado

        @param  f_oExe : pointer para o exercício a remover
        """
        # verifica condições de execução
        assert f_oExe is not None

        # remove a linha da widget
        self.qtwExeTab.removeRow(self.qtwExeTab.currentRow())

        # Cria o evento para apagar do disco o exercício
        l_evtDelFromDisk = events.CDelFromDisk(fs_table="EXE", fs_filename=f_oExe.s_exe_id)
        assert l_evtDelFromDisk

        # dissemina o evento
        self._event.post(l_evtDelFromDisk)

    # ---------------------------------------------------------------------------------------------
    def exeSelect(self):
        """
        seleciona um exercício a editar
        """
        # verifica condições de execução
        assert self._dctExe is not None
        assert self.qtwExeTab is not None

        # obtém o exercício selecionado
        self._oExe = self.getCurrentSel(self._dctExe, self.qtwExeTab)
        assert self._oExe

        # Cria o evento para configurar o exercício atual
        l_evtConfigExe = evtConfig.CConfigExe(ls_exe=self._oExe.s_exe_id)
        assert l_evtConfigExe

        # dissemina o evento
        self._event.post(l_evtConfigExe)

        # atualiza a área de dados do exercício selecionado
        self.exeUpdateSel()

    # ---------------------------------------------------------------------------------------------
    def exeUpdateList(self):
        """
        atualiza na tela os dados da lista de exercícios
        """
        # verifica condições de execução
        assert self._dctExe is not None
        assert self.qtwExeTab is not None

        # atualiza a QTableWidget de exercícios
        self.exeUpdateWidget()

        # obtém o exercício selecionado
        self._oExe = self.getCurrentSel(self._dctExe, self.qtwExeTab)
        # assert self._oExe

    # ---------------------------------------------------------------------------------------------
    def exeUpdateSel(self):
        """
        atualiza na tela os dados do exercício selecionado
        """
        # exercício selecionado existe ?
        l_log = logging.getLogger("CDlgExeDataNEW::exeUpdateSel")
        l_log.setLevel(logging.DEBUG)

        if self._oExe is not None:
            # indicativo do exercício
            #l_sExeID = self._oExe.s_exe_id

            # atualiza a visualização do exercício
            # self._oSrv.configExe(l_sExeID, dbus_interface = self.cSRV_Path)

            # identificação
            self.txtExeID.setText(self._oExe.s_exe_id)
            self.qleExeDesc.setText(self._oExe.s_exe_desc)
            l_exe_hor_ini = str(self._oExe.t_exe_hor_ini[0]) + ":" + str(self._oExe.t_exe_hor_ini[1])
            self.tedHorIni.setTime(QtCore.QTime.fromString(l_exe_hor_ini,"h:m"))
            l_log.debug(" Exercicio [%s] Descricao [%s] Hora Inicial [%s]" %
                        (self._oExe.s_exe_id, self._oExe.s_exe_desc, l_exe_hor_ini))

            # atualiza a lista de tráfegos do exercício
            self.trfUpdateWidget()

        # senão, o exercício não existe
        else:
            # posiciona cursor no início do formulário
            self.txtExeID.setFocus()

    # ---------------------------------------------------------------------------------------------
    def exeUpdateWidget(self):
        """
        atualiza na tela os dados da QTableWidget de exercícios
        """
        l_log = logging.getLogger("CDlgExeDataNEW::exeUpdateWidget")
        l_log.setLevel(logging.DEBUG)
        l_log.debug(" load exes on the table ...")

        # verifica condições de execução
        assert self.qtwExeTab is not None
        assert self._dctExe is not None

        # limpa a QTableWidget
        self.qtwExeTab.clear()

        # seta o número de linhas da QTableWidget para o tamanho da lista
        self.qtwExeTab.setRowCount(len(self._dctExe))

        # seta número de colunas e cabeçalho das colunas
        self.qtwExeTab.setColumnCount(2)
        self.qtwExeTab.setHorizontalHeaderLabels([u"Indicativo", u"Descrição"])

        # seta QTableWidget
        self.qtwExeTab.setAlternatingRowColors(True)
        self.qtwExeTab.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.qtwExeTab.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
        self.qtwExeTab.setSelectionMode(QtGui.QTableWidget.SingleSelection)
        self.qtwExeTab.setSortingEnabled(False)

        # linha 0 (objeto exercício)
        l_oA0 = None

        # linha selecionada (objeto exercício)
        l_oSItem = None

        # para cada exercício no dicionário..
        for l_iNdx, l_sExeID in enumerate(sorted(self._dctExe.keys())):
            # indicativo do exercício
            l_twiExeID = QtGui.QTableWidgetItem(l_sExeID)
            l_twiExeID.setData(QtCore.Qt.UserRole, QtCore.QVariant(l_sExeID))

            self.qtwExeTab.setItem(l_iNdx, 0, l_twiExeID)

            # é o exercício selecionado ?
            if (self._oExe is not None) and (self._oExe.s_exe_id == l_sExeID):
                # salva pointer para o item selecionado
                l_oSItem = l_twiExeID

            # obtém o exercício
            l_oExe = self._dctExe[l_sExeID]
            assert l_oExe

            # descrição
            l_twiExeDesc = QtGui.QTableWidgetItem(l_oExe.s_exe_desc)
            l_log.debug(" Exe ID [%s] Descricao [%s]" % (l_oExe.s_exe_id, l_twiExeDesc.text()))
            l_log.debug(" Quantidade de tráfegos [%d]" % l_oExe.i_exe_qtd_trf)

            self.qtwExeTab.setItem(l_iNdx, 1, l_twiExeDesc)

        # existe um exercício selecionado ?
        if self._oExe is not None:
            # seleciona o item
            self.qtwExeTab.setCurrentItem(l_oSItem)

            # posiciona no item selecionado
            self.qtwExeTab.scrollToItem(l_oSItem)

            # marca que existe seleção
            l_oSItem.setSelected(True)

        # senão, não existe um exercício selecionado
        else:
            # seleciona a primeira linha
            self.qtwExeTab.selectRow(0)

            # obtém o exercício atual
            self._oExe = self.getCurrentSel(self._dctExe, self.qtwExeTab)
            # assert self._oExe

        # ajusta o tamanho das colunas pelo conteúdo
        self.qtwExeTab.resizeColumnsToContents()

        # habilita a ordenação
        self.qtwExeTab.setSortingEnabled(True)

    # ---------------------------------------------------------------------------------------------
    def getCurrentData(self, f_qtwTab, f_iCol):
        """
        retorna os dados associados a linha selecionada
        """
        l_log = logging.getLogger("CDlgExeDataNEW::getCurrentData")
        l_log.setLevel(logging.DEBUG)
        l_log.debug("Obter os dados elemento selecionado")

        # verifica condições de execução
        assert f_qtwTab is not None

        # o dado da linha selecionada
        l_sData = ""

        # obtém o item da linha selecionada
        l_oItem = self.getCurrentItem(f_qtwTab, f_iCol)
        l_log.debug(" Dados do Item [%s]" % str(l_oItem.text()))

        # existe uma linha selecionada ?
        if l_oItem is not None:
            # obtém o dado associado a linha
            #l_sData = l_oItem.data(QtCore.Qt.UserRole).toString()
            l_sData = l_oItem.text()

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
        # verifica condições de execução
        assert f_dct is not None
        assert f_qtw is not None

        # obtém o index da linha selecionada
        l_sID = self.getCurrentData(f_qtw, 0)

        # indice válido ?
        if str(l_sID) in f_dct:
            # obtém o elemento selecionado se existir uma linha selecionada
            l_oSel = f_dct[str(l_sID)]
            assert l_oSel

        # senão, índice inválido
        else:
            # não há elemento selecionado
            l_oSel = None

        # retorna o elemento da linha selecionada na lista
        return l_oSel

    # ---------------------------------------------------------------------------------------------
    def getCurrentTrfSel(self, f_dct, f_qtw):
        """
        retorna o tráfego do exercício associado a linha selecionada na lista
        """
        l_log = logging.getLogger("CDlgExeDataNEW::getCurrentTrfSel")
        l_log.setLevel(logging.DEBUG)
        l_log.debug("Obter o elemento selecionado")

        # verifica condições de execução
        assert f_dct is not None
        assert f_qtw is not None

        # obtém o index da linha selecionada
        l_sID = self.getCurrentData(f_qtw, 0)
        l_log.debug ("ID [%s]" % l_sID)
        l_iID = int(l_sID)

        # indice válido ?
        if l_iID in f_dct:
            # obtém o elemento selecionado se existir uma linha selecionada
            l_oSel = f_dct[l_iID]
            assert l_oSel

        # senão, índice inválido
        else:
            # não há elemento selecionado
            l_oSel = None

        # retorna o elemento da linha selecionada na lista
        return l_oSel

    # ---------------------------------------------------------------------------------------------
    def loadInitial(self):
        """
        faz a carga inicial da tabela de exercícios
        """
        l_log = logging.getLogger("CDlgExeDataNEW::loadInitial")
        l_log.setLevel(logging.DEBUG)
        l_log.debug(" load exes ...")

        # obtém o dicionário de exercícios
        self._dctExe = self._model.dct_exe

        # o dicionário de exercícios não existe ?
        if self._dctExe is None:
            # logger
            l_log.critical(u"<E01: Tabela de exercícios não carregada !")

            # cria um evento de quit
            l_evtQuit = events.CQuit()
            assert l_evtQuit

            # dissemina o evento
            self._event.post(l_evtQuit)

            # cai fora..
            sys.exit(1)

        # atualiza na tela os dados da tabela de exercícios
        self.exeUpdateList()

    # ---------------------------------------------------------------------------------------------
    def okToContinue(self):
        """
        cria uma messageBox

        @return True se tratou a resposta, senão False
        """
        # resposta
        l_bAns = True
        '''
        # flag de alterações setado ?
        if(self._bChanged):
            # questiona sobre alterações pendentes
            l_Resp = QtGui.QMessageBox.question(self, self._txtContinueTit,
                                                        self._txtContinueMsg,
                                                        QtGui.QMessageBox.Yes |
                                                        QtGui.QMessageBox.No |
                                                        QtGui.QMessageBox.Cancel)

            # cancela ?
            if(QtGui.QMessageBox.Cancel == l_Resp):
                # não sai
                l_bAns = False

            # salva ?
            elif(QtGui.QMessageBox.Yes == l_Resp):
                # salva as pendências e sai
                l_bAns = True

            # não salva ?
           else:
               # reseta o flag de alterações..
               self._bChanged = False

               # ...e sai
               l_bAns = True
        '''
        # return
        return l_bAns

    # ---------------------------------------------------------------------------------------------
    def reject(self):
        """
        DOCUMENT ME!
        """
        self._oExe = None

        # faz o "reject"
        QtGui.QDialog.reject(self)

        # close dialog
        self.close()

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
    def trfDel(self):
        """

        :return:
        """
        # verifica condições de execução
        assert self.qtw_anv is not None
        assert self._oExe is not None
        assert self._oExe.dct_exe_trf is not None

        # obtém o tráfego do exercício selecionado
        l_oTrf = self.getCurrentTrfSel(self._oExe.dct_exe_trf, self.qtw_anv)

        if l_oTrf is not None:
            # apaga o tráfego do exercício atual ?
            if QtGui.QMessageBox.Yes == QtGui.QMessageBox.question(self,
               self._txtDelTrfTit,
               self._txtDelTrfMsg.format(l_oTrf.s_trf_ind),
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No):
                # apaga o tráfego do exercício
                self.trfRemove(l_oTrf)

    # ---------------------------------------------------------------------------------------------
    def trfEdit(self):
        """
        callback de btnTrfNew da dialog de edição de tráfegos do exercício
        atualiza o tráfego do exercício na lista

        :return:
        """
        l_log = logging.getLogger("CDlgExeDataNEW::trfEdit")
        l_log.setLevel(logging.DEBUG)
        l_log.debug("Editar um tráfego do exercício")

        # verifica condições de execução
        assert self.qtw_anv is not None
        assert self._oExe is not None
        assert self._oExe.dct_exe_trf is not None

        # obtém o tráfego do exercício selecionado
        l_oTrf = self.getCurrentTrfSel(self._oExe.dct_exe_trf, self.qtw_anv)
        l_log.debug("Tráfego : [%s] - Id [%s]" % (l_oTrf, l_oTrf.i_trf_id))

        if (l_oTrf is not None):
            # cria a dialog de edição do tráfego do exercício
            l_Dlg = dlgAnv.CDlgAnvEditNEW(self._control, l_oTrf, self)
            assert l_Dlg

            # processa a dialog de edição de exercícios (modal)
            if(l_Dlg.exec_ ()):
                # obtém os dados alterados
                l_oTrf = l_Dlg.getData()
                l_log.debug("Tráfego Id [%s]" % str(l_oTrf.i_trf_id))

                # tráfego do exercício existente ?
                if (l_oTrf is not None) and (self._oExe is not None):
                    # atualiza o tráfego do exercício na lista
                    self._oExe.dct_exe_trf[l_oTrf.i_trf_id] = l_oTrf

                    # atualiza o exercicio no dicionário de exercícios
                    self._dctExe[self._oExe.s_exe_id] = self._oExe

                    # Cria o evento para salvar no disco o exercício atualizado
                    l_evtUpd2Disk = events.CUpd2Disk(fs_table="ANV", fs_filename=self._oExe.s_exe_id)
                    assert l_evtUpd2Disk

                    # dissemina o evento
                    self._event.post(l_evtUpd2Disk)

                    # se ok, atualiza a QTableWidget de exercícios
                    self.trfUpdateWidget ()

    # ---------------------------------------------------------------------------------------------
    def trfNew(self):
        """
        callback de btnTrfNew da dialog de edição de tráfegos do exercício
        cria um novo tráfego do exercício na lista
        """
        l_log = logging.getLogger("CDlgExeDataNEW::trfNew")
        l_log.setLevel(logging.DEBUG)
        l_log.debug("Um novo tráfego do exercício [%s]" % self._oExe.s_exe_id)

        # cria a dialog de edição de tráfegos do exercício
        l_Dlg = dlgAnv.CDlgAnvEditNEW(self._control, None, self)
        assert l_Dlg

        # processa a dialog de edição de tráfegos do exercícios (modal)
        if l_Dlg.exec_():
            # obtém os dados da edição
            l_oTrf = l_Dlg.getData()
            li_node = 1

            # Obtém o número do nó que não está sendo usado
            if self._oExe.dct_exe_trf is not None:
                ll_node_hosts = self._oExe.dct_exe_trf.keys()
                l_log.debug("Dicionario de tráfegos do exercício [%s]" % self._oExe.dct_exe_trf)
                l_log.debug("Lista de node hosts [%s]" % ll_node_hosts)
                ll_node_hosts.sort()
                li_index = 0
                li_node = 1
                while li_index < len(ll_node_hosts):
                    if (li_index > 0):
                        if ll_node_hosts[li_index] != ll_node_hosts[li_index - 1] + 1:
                            li_node = ll_node_hosts[li_index - 1] + 1
                            break

                    li_index = li_index + 1

                if li_index != 0 and li_index == len(ll_node_hosts):
                    li_node = ll_node_hosts[li_index -1] + 1

            # tráfego do exercício existente ?
            if (l_oTrf is not None) and (self._oExe is not None):
                # insere o tráfego do exercício na lista
                l_oTrf.i_trf_id = li_node
                self._oExe.dct_exe_trf[li_node] = l_oTrf

                # atualiza o exercicio no dicionário de exercícios
                self._dctExe[self._oExe.s_exe_id] = self._oExe

                # Cria o evento para salvar no disco os exercícios
                l_evtSave2Disk = events.CSave2Disk(fs_table="ANV")
                assert l_evtSave2Disk

                # dissemina o evento
                self._event.post(l_evtSave2Disk)

                # se ok, atualiza a QTableWidget de exercícios
                self.trfUpdateWidget()

    # ---------------------------------------------------------------------------------------------
    def trfRemove(self, f_oTrf):
        """
        remove o tráfego selecionado do exercício atual

        @param  f_oTrf : pointer para o tráfego selecionado
        """
        # verifica condições de execução
        assert f_oTrf is not None

        # remove a linha da widget
        self.qtw_anv.removeRow(self.qtw_anv.currentRow())

        # atualiza a tabela de tráfegos do exercício
        l_dctTrf = self._oExe.dct_exe_trf
        del l_dctTrf[f_oTrf.i_trf_id]
        self._oExe.dct_exe_trf = l_dctTrf

        # atualiza o exercicio no dicionário de exercícios
        self._dctExe[self._oExe.s_exe_id] = self._oExe

        l_evt = None
        if len(self._oExe.dct_exe_trf):
            # Cria o evento para atualizar a tabela de trafegos no disco
            l_evt = events.CSave2Disk(fs_table="ANV")
            assert l_evt
        else:
            # Cria o evento para apagar do disco o exercício
            l_evt = events.CDelFromDisk(fs_table="ANV", fs_filename=self._oExe.s_exe_id)
            assert l_evt

        # dissemina o evento
        if l_evt is not None:
            self._event.post(l_evt)

    # ---------------------------------------------------------------------------------------------
    def trfUpdateWidget(self):
        """
        atualiza na tela os dados da QtableWidget de tráfegos do exercício

        :return:
        """
        # verifica condições de execução
        # assert self.qtw_anv is not None
        # assert self._oExe is not None
        l_log = logging.getLogger("CDlgExeDataNEW::trfUpdateWidget")
        l_log.setLevel(logging.DEBUG)
        l_log.debug("Atualizando a tabela de tráfegos")

        for li_row in range(self.qtw_anv.rowCount()):
            self.qtw_anv.removeRow(li_row)

        self.qtw_anv.setRowCount(0)

        self.qtw_anv.setColumnCount(14)
        self.qtw_anv.setHorizontalHeaderLabels(
            ["Node", "Latitude", "Longitude", "Tipo da Anv", "SSR", "Indicativo", "Origem", "Destino", "Proa", "Velocidade (Kt)",
             "Altitude (Ft)", "Procedimento", "Tempo (min)", "ID"])

        self.qtw_anv.setColumnHidden(13, True)
        self.qtw_anv.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.qtw_anv.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.qtw_anv.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
        self.qtw_anv.setSelectionMode(QtGui.QTableWidget.SingleSelection)

        li_row = 0

        # para todas as linhas da tabela...
        l_log.debug(" Número de tráfegos [%s]" % len(self._oExe.dct_exe_trf))
        for li_key, l_oTrf in self._oExe.dct_exe_trf.iteritems():
            # cria nova linha na tabela
            self.qtw_anv.insertRow(li_row)

            # node name
            lqtwi_item = QtGui.QTableWidgetItem(str(li_key))
            lqtwi_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.qtw_anv.setItem(li_row, 0, lqtwi_item)

            # latitude
            lqtwi_item = QtGui.QTableWidgetItem(str(l_oTrf.f_trf_lat))
            lqtwi_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.qtw_anv.setItem(li_row, 1, lqtwi_item)

            # longitude
            lqtwi_item = QtGui.QTableWidgetItem(str(l_oTrf.f_trf_lng))
            lqtwi_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.qtw_anv.setItem(li_row, 2, lqtwi_item)

            # designador
            lqtwi_item = QtGui.QTableWidgetItem(l_oTrf.ptr_trf_prf.s_prf_id)
            lqtwi_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.qtw_anv.setItem(li_row, 3, lqtwi_item)

            # ssr
            lqtwi_item = QtGui.QTableWidgetItem(str(l_oTrf.i_trf_ssr).zfill(4))
            lqtwi_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.qtw_anv.setItem(li_row, 4, lqtwi_item)

            # indicativo
            lqtwi_item = QtGui.QTableWidgetItem(l_oTrf.s_trf_ind)
            lqtwi_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.qtw_anv.setItem(li_row, 5, lqtwi_item)

            # origem
            lqtwi_item = QtGui.QTableWidgetItem(l_oTrf.ptr_trf_aer_ori.s_aer_indc)
            lqtwi_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.qtw_anv.setItem(li_row, 6, lqtwi_item)

            # destino
            lqtwi_item = QtGui.QTableWidgetItem(l_oTrf.ptr_trf_aer_dst.s_aer_indc)
            lqtwi_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.qtw_anv.setItem(li_row, 7, lqtwi_item)

            # proa
            lqtwi_item = QtGui.QTableWidgetItem(str(l_oTrf.f_trf_pro_atu))
            lqtwi_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.qtw_anv.setItem(li_row, 8, lqtwi_item)

            # velocidade
            lf_VelKt = l_oTrf.f_trf_vel_atu * cdefs.D_CNV_MS2KT
            lqtwi_item = QtGui.QTableWidgetItem(str(lf_VelKt))
            lqtwi_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.qtw_anv.setItem(li_row, 9, lqtwi_item)

            # altitude
            lf_AltFt = l_oTrf.f_trf_alt_atu * cdefs.D_CNV_M2FT
            lqtwi_item = QtGui.QTableWidgetItem(str(lf_AltFt))
            lqtwi_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.qtw_anv.setItem(li_row, 10, lqtwi_item)

            # procedimento
            lqtwi_item = QtGui.QTableWidgetItem(l_oTrf.s_trf_prc)
            lqtwi_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.qtw_anv.setItem(li_row, 11, lqtwi_item)

            # tempo de apresentação do tráfego
            li_HorIni, li_MinIni, li_SegIni = self._oExe.t_exe_hor_ini
            li_MinIni = li_MinIni + (li_HorIni * 60) + (li_SegIni / 60)

            li_Hor, li_Min, li_Seg = l_oTrf.t_trf_hor_atv
            li_Min = li_Min + (li_Hor * 60) + (li_Seg / 60)

            lqtwi_item = QtGui.QTableWidgetItem(str(li_Min - li_MinIni))
            lqtwi_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.qtw_anv.setItem(li_row, 12, lqtwi_item)

            li_row = li_row + 1

        # redefine o tamanho da QTableWidget
        self.qtw_anv.resizeRowsToContents()
        self.qtw_anv.resizeColumnsToContents()

# < the end >--------------------------------------------------------------------------------------
