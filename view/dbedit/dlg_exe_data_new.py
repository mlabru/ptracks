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

revision 0.2  2017/jun  mlabru
pep-8

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
import sys

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

# model
import model.items.exe_data as dctExe

# view
import view.dbedit.dlg_exe_edit_new as dlgEdit
import view.dbedit.dlg_exe_data_new_ui as dlgData_ui

# control
import control.control_debug as dbg
import control.events.events_basic as events

# < class CDlgExeDataNEW >-------------------------------------------------------------------------

class CDlgExeDataNEW (QtGui.QDialog, dlgData_ui.Ui_CDlgExeDataNEW):
    """
    mantém as informações sobre a dialog de edição da tabela de exercícios
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control, f_parent=None):
        """
        constructor

        @param f_control: control
        @param f_parent: janela vinculada
        """
        # check input
        assert f_control

        # init super class
        super(CDlgExeDataNEW, self).__init__(f_parent)

        # control
        self.__control = f_control

        # event
        self.__event = f_control.event
        assert self.__event

        # gerente de configuração
        # self.__config = f_control.config
        # assert self.__config

        # dicionário de configuração
        # self.__dct_config = self.__config.dct_config
        # assert self.__dct_config

        # model
        self.__model = f_control.model
        assert self.__model

        # parent window
        self.__parent = f_parent

        # existe uma parent window ?
        if self.__parent is not None:
            # esconde a parent window
            self.__parent.setVisible(False)

        # pointer para os itens correntes
        self.__exe = None

        # pointer para os dicionários a editar
        self.__dct_exe = None

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

        # faz a carrga inicial do diretório de exercícios
        QtCore.QTimer.singleShot(0, self.__load_initial)

    # ---------------------------------------------------------------------------------------------
    def accept(self):
        """
        callback de btn_ok da dialog de edição
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
            l_set.setValue("%s/Geometry" % (self.__txtSettings),
                           QtCore.QVariant(self.saveGeometry()))

            # existe a parent window ?
            if self.__parent is not None:
                # exibe a parent window
                self.__parent.setVisible(True)

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
        self.connect(self.btn_del,
                     QtCore.SIGNAL("clicked()"),
                     self.exeDel)
        '''
        # conecta click a edição de exercício
        self.connect(self.btn_edit,
                       QtCore.SIGNAL("clicked()"),
                       self.exeEdit)
        '''
        # conecta click a inclusão de exercício
        self.connect(self.btn_new,
                     QtCore.SIGNAL("clicked()"),
                     self.exeNew)

        # conecta click a seleção da linha
        self.connect(self.qtw_exe,
                     QtCore.SIGNAL("itemSelectionChanged()"),
                     self.exeSelect)

        # conecta botão Ok
        self.connect(self.dbb_exe,
                     QtCore.SIGNAL("accepted()"),
                     self.accept)

        # conecta botão Cancela
        self.connect(self.dbb_exe,
                     QtCore.SIGNAL("rejected()"),
                     self.reject)

        # configura botões
        self.dbb_exe.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.dbb_exe.button(QtGui.QDialogButtonBox.Ok).setFocus()

    # ---------------------------------------------------------------------------------------------
    def configTexts(self):
        """
        configura títulos e mensagens
        """
        self.__txtSettings = "CDlgExeDataNEW"

        # self.__txtContinueTit = u"TrackS - Alterações pendentes"
        # self.__txtContinueMsg = u"Salva alterações pendentes ?"

        self.__txtDelExeTit = u"Apaga exercício"
        self.__txtDelExeMsg = u"Apaga exercício {0} ?"

    # ---------------------------------------------------------------------------------------------
    def exeDel(self):
        """
        callback de btn_del da dialog de edição
        deleta um exercício da lista
        """
        # clear to go
        assert self.qtw_exe is not None
        assert self.__dct_exe is not None

        # exercício selecionado
        self.__exe = self.getCurrentSel(self.__dct_exe, self.qtw_exe)

        if self.__exe is not None:
            # apaga o exercício atual ?
            if QtGui.QMessageBox.Yes == QtGui.QMessageBox.question(self,
               self.__txtDelExeTit,
               self.__txtDelExeMsg.format(self.__exe._sExeID),
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No):

                # apaga o exercício
                self.exeRemove(self.__exe)
    '''
    # ---------------------------------------------------------------------------------------------
    def exeEdit(self):
        """
        callback de btn_edit da dialog de edição
        edita um exercício da QTableWidget
        """
        # clear to go
        assert self.qtw_exe is not None
        assert self.__dct_exe is not None

        # exercício selecionado
        self.__exe = self.getCurrentSel(self.__dct_exe, self.qtw_exe)

        if(self.__exe is not None):
            # cria a dialog de edição de exercícios
            l_Dlg = dlgEdit.dlgExeEditNEW(self.__control, self.__exe, self)
            assert l_Dlg

            # processa a dialog de edição de exercícios (modal)
            if(l_Dlg.exec_ ()):
                # salva em disco as alterações no exercício
                # self.__exe.save2Disk(self.__exe._sPN)

                # se ok, atualiza a QTableWidget de exercícios
                self.exeUpdateWidget ()
    '''
    # ---------------------------------------------------------------------------------------------
    def exeNew(self):
        """
        callback de btn_new da dialog de edição
        cria um novo exercício na lista
        """
        # cria a dialog de edição de exercícios
        l_Dlg = dlgEdit.dlgExeEditNEW(self.__control, None, self)
        assert l_Dlg

        # processa a dialog de edição de exercícios (modal)
        if l_Dlg.exec_():
            # obtém os dados da edição
            self.__exe = l_Dlg.getData()

            # exercício existente ?
            if (self.__exe is not None) and (self.__dct_exe is not None):
                # insere o exercício na lista
                self.__dct_exe.append(self.__exe)

                # salva o arquivo no disco
                # self.__exe.save2Disk(l_sPath)

                # se ok, atualiza a QTableWidget de exercícios
                self.exeUpdateWidget()

    # ---------------------------------------------------------------------------------------------
    def exeRemove(self, f_oExe):
        """
        remove o exercício selecionado

        @param  f_oExe : pointer para o exercício a remover
        """
        # clear to go
        assert f_oExe is not None

        # remove a linha da widget
        self.qtw_exe.removeRow(self.qtw_exe.currentRow())

        # remove o exercício da lista
        self.__dct_exe.remove(f_oExe)

    # ---------------------------------------------------------------------------------------------
    def exeSelect(self):
        """
        seleciona um exercício a editar
        """
        # clear to go
        assert self.__dct_exe is not None
        assert self.qtw_exe is not None

        # exercício selecionado
        self.__exe = self.getCurrentSel(self.__dct_exe, self.qtw_exe)
        assert self.__exe

        # atualiza a área de dados do exercício selecionado
        self.exeUpdateSel()

    # ---------------------------------------------------------------------------------------------
    def exeUpdateList(self):
        """
        atualiza na tela os dados da lista de exercícios
        """
        # clear to go
        assert self.__dct_exe is not None
        assert self.qtw_exe is not None

        # atualiza a QTableWidget de exercícios
        self.exeUpdateWidget()

        # exercício selecionado
        self.__exe = self.getCurrentSel(self.__dct_exe, self.qtw_exe)
        # assert self.__exe

    # ---------------------------------------------------------------------------------------------
    def exeUpdateSel(self):
        """
        atualiza na tela os dados do exercício selecionado
        """
        # exercício selecionado existe ?
        if self.__exe is not None:
            # indicativo do exercício
            l_sExeID = self.__exe.sExeID

            # atualiza a visualização do exercício
            # self.__oSrv.configExe(l_sExeID, dbus_interface = self.cSRV_Path)

            # identificação
            self.txtExeID.setText(self.__exe.sExeID)
            self.qleExeDesc.setText(self.__exe.sExeDesc)

            # freqüência
            # self.__exe._fExeFrequencia = 0

            # posição

            # posição
            # self.__exe._oExePosicao = None

            # l_iX, l_iY = self.__exe._oCentro.getPto ()

            # self.txtCntrX.setText(str(l_iX))
            # self.txtCntrY.setText(str(l_iY))

        # senão, o exercício não existe
        else:
            # posiciona cursor no início do formulário
            self.txtExeID.setFocus()

    # ---------------------------------------------------------------------------------------------
    def exeUpdateWidget(self):
        """
        atualiza na tela os dados da QTableWidget de exercícios
        """
        # clear to go
        assert self.qtw_exe is not None
        assert self.__dct_exe is not None

        # limpa a QTableWidget
        self.qtw_exe.clear()

        # seta o número de linhas da QTableWidget para o tamanho da lista
        self.qtw_exe.setRowCount(len(self.__dct_exe))

        # seta número de colunas e cabeçalho das colunas
        self.qtw_exe.setColumnCount(2)
        self.qtw_exe.setHorizontalHeaderLabels([u"Indicativo", u"Descrição"])

        # seta QTableWidget
        self.qtw_exe.setAlternatingRowColors(True)
        self.qtw_exe.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.qtw_exe.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
        self.qtw_exe.setSelectionMode(QtGui.QTableWidget.SingleSelection)
        self.qtw_exe.setSortingEnabled(False)

        # linha 0 (objeto exercício)
        l_oA0 = None

        # linha selecionada (objeto exercício)
        l_oSItem = None

        # para cada exercício no dicionário..
        for l_iNdx, l_sExeID in enumerate(sorted(self.__dct_exe.keys())):
            # indicativo do exercício
            l_twiExeID = QtGui.QTableWidgetItem(l_sExeID)
            l_twiExeID.setData(QtCore.Qt.UserRole, QtCore.QVariant(l_sExeID))

            self.qtw_exe.setItem(l_iNdx, 0, l_twiExeID)

            # é o exercício selecionado ?
            if (self.__exe is not None) and (self.__exe._sExeID == l_sExeID):
                # salva pointer para o item selecionado
                l_oSItem = l_twiExeID

            # exercício
            l_oExe = self.__dct_exe[l_sExeID]
            assert l_oExe

            # descrição
            l_twiExeDesc = QtGui.QTableWidgetItem(l_oExe._sExeDesc)

            self.qtw_exe.setItem(l_iNdx, 1, l_twiExeDesc)

        # existe um exercício selecionado ?
        if self.__exe is not None:
            # seleciona o item
            self.qtw_exe.setCurrentItem(l_oSItem)

            # posiciona no item selecionado
            self.qtw_exe.scrollToItem(l_oSItem)

            # marca que existe seleção
            l_oSItem.setSelected(True)

        # senão, não existe um exercício selecionado
        else:
            # seleciona a primeira linha
            self.qtw_exe.selectRow(0)

            # exercício atual
            self.__exe = self.getCurrentSel(self.__dct_exe, self.qtw_exe)
            # assert self.__exe

        # ajusta o tamanho das colunas pelo conteúdo
        self.qtw_exe.resizeColumnsToContents()

        # habilita a ordenação
        self.qtw_exe.setSortingEnabled(True)

    # ---------------------------------------------------------------------------------------------
    def getCurrentData(self, f_qtwTab, f_iCol):
        """
        retorna os dados associados a linha selecionada
        """
        # clear to go
        assert f_qtwTab is not None

        # o dado da linha selecionada
        l_sData = ""

        # item da linha selecionada
        l_oItem = self.getCurrentItem(f_qtwTab, f_iCol)

        # existe uma linha selecionada ?
        if l_oItem is not None:
            # dado associado a linha
            l_sData = l_oItem.data(QtCore.Qt.UserRole).toString()

        # retorna o dado associado a linha selecionada
        return l_sData

    # ---------------------------------------------------------------------------------------------
    def getCurrentItem(self, f_qtwTab, f_iCol):
        """
        retorna o item associado a linha selecionada
        """
        # o item selecionado
        l_oItem = None

        # clear to go
        assert f_qtwTab is not None

        # número da linha selecionada
        l_iRow = f_qtwTab.currentRow()

        # existe uma linha selecionada ?
        if l_iRow > -1:
            # item associado
            l_oItem = f_qtwTab.item(l_iRow, f_iCol)
            assert l_oItem

        # retorna o item selecionado na lista
        return l_oItem

    # ---------------------------------------------------------------------------------------------
    def getCurrentSel(self, f_dct, f_qtw):
        """
        retorna o elemento associado a linha selecionada na lista
        """
        # clear to go
        assert f_dct is not None
        assert f_qtw is not None

        # index da linha selecionada
        l_sID = self.getCurrentData(f_qtw, 0)

        # indice válido ?
        if str(l_sID) in f_dct:
            # elemento selecionado se existir uma linha selecionada
            l_oSel = f_dct[str(l_sID)]
            assert l_oSel

        # senão, índice inválido
        else:
            # não há elemento selecionado
            l_oSel = None

        # retorna o elemento da linha selecionada na lista
        return l_oSel

    # ---------------------------------------------------------------------------------------------
    def __load_initial(self):
        """
        faz a carga inicial da tabela de exercícios
        """
        # dicionário de exercícios
        self.__dct_exe = self.__model.dct_exe

        # dicionário de exercícios não existe ?
        if self.__dct_exe is None:
            # logger
            l_log.critical(u"<E01: tabela de exercícios não existe.")

            # cria um evento de quit
            l_evtQuit = events.CQuit()
            assert l_evtQuit

            # dissemina o evento
            self.__event.post(l_evtQuit)

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
        if(self.__bChanged):
            # questiona sobre alterações pendentes
            l_Resp = QtGui.QMessageBox.question(self, self.__txtContinueTit,
                                                        self.__txtContinueMsg,
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
               self.__bChanged = False

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
        self.__exe = None

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
        self.restoreGeometry(l_set.value("%s/Geometry" % (self.__txtSettings)).toByteArray())

        # return
        return True

# < the end >--------------------------------------------------------------------------------------
