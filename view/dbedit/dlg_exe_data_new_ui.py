# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './dlg_exe_data_new.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_CDlgExeDataNEW(object):
    def setupUi(self, CDlgExeDataNEW):
        CDlgExeDataNEW.setObjectName(_fromUtf8("CDlgExeDataNEW"))
        CDlgExeDataNEW.setWindowModality(QtCore.Qt.WindowModal)
        CDlgExeDataNEW.resize(763, 580)
        CDlgExeDataNEW.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        CDlgExeDataNEW.setSizeGripEnabled(True)
        CDlgExeDataNEW.setModal(True)
        self.verticalLayout_4 = QtGui.QVBoxLayout(CDlgExeDataNEW)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.splitter = QtGui.QSplitter(CDlgExeDataNEW)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.wid_qwt = QtGui.QWidget(self.splitter)
        self.wid_qwt.setObjectName(_fromUtf8("wid_qwt"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.wid_qwt)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.qtwExeTab = QtGui.QTableWidget(self.wid_qwt)
        self.qtwExeTab.setObjectName(_fromUtf8("qtwExeTab"))
        self.qtwExeTab.setColumnCount(0)
        self.qtwExeTab.setRowCount(0)
        self.verticalLayout_2.addWidget(self.qtwExeTab)
        self.frm_btn_exe = QtGui.QFrame(self.wid_qwt)
        self.frm_btn_exe.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frm_btn_exe.setFrameShadow(QtGui.QFrame.Raised)
        self.frm_btn_exe.setObjectName(_fromUtf8("frm_btn_exe"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frm_btn_exe)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnExeNew = QtGui.QPushButton(self.frm_btn_exe)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/dbedit/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnExeNew.setIcon(icon)
        self.btnExeNew.setObjectName(_fromUtf8("btnExeNew"))
        self.horizontalLayout.addWidget(self.btnExeNew)
        self.btnExeEdit = QtGui.QPushButton(self.frm_btn_exe)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/dbedit/open.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnExeEdit.setIcon(icon1)
        self.btnExeEdit.setObjectName(_fromUtf8("btnExeEdit"))
        self.horizontalLayout.addWidget(self.btnExeEdit)
        self.btnExeDel = QtGui.QPushButton(self.frm_btn_exe)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/dbedit/delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnExeDel.setIcon(icon2)
        self.btnExeDel.setObjectName(_fromUtf8("btnExeDel"))
        self.horizontalLayout.addWidget(self.btnExeDel)
        self.btnExeNew.raise_()
        self.btnExeDel.raise_()
        self.btnExeEdit.raise_()
        self.verticalLayout_2.addWidget(self.frm_btn_exe)
        self.wid_data = QtGui.QWidget(self.splitter)
        self.wid_data.setObjectName(_fromUtf8("wid_data"))
        self.verticalLayout = QtGui.QVBoxLayout(self.wid_data)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frm_id = QtGui.QFrame(self.wid_data)
        self.frm_id.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frm_id.setFrameShadow(QtGui.QFrame.Raised)
        self.frm_id.setLineWidth(1)
        self.frm_id.setObjectName(_fromUtf8("frm_id"))
        self.gridLayout = QtGui.QGridLayout(self.frm_id)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lbl_indc = QtGui.QLabel(self.frm_id)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_indc.sizePolicy().hasHeightForWidth())
        self.lbl_indc.setSizePolicy(sizePolicy)
        self.lbl_indc.setObjectName(_fromUtf8("lbl_indc"))
        self.gridLayout.addWidget(self.lbl_indc, 0, 0, 1, 1)
        self.qleExeDesc = QtGui.QLineEdit(self.frm_id)
        self.qleExeDesc.setReadOnly(True)
        self.qleExeDesc.setObjectName(_fromUtf8("qleExeDesc"))
        self.gridLayout.addWidget(self.qleExeDesc, 1, 2, 1, 4)
        self.lbl_desc = QtGui.QLabel(self.frm_id)
        self.lbl_desc.setObjectName(_fromUtf8("lbl_desc"))
        self.gridLayout.addWidget(self.lbl_desc, 1, 0, 1, 1)
        self.txtExeID = QtGui.QLabel(self.frm_id)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtExeID.sizePolicy().hasHeightForWidth())
        self.txtExeID.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.txtExeID.setFont(font)
        self.txtExeID.setObjectName(_fromUtf8("txtExeID"))
        self.gridLayout.addWidget(self.txtExeID, 0, 2, 1, 1)
        self.lbl_hor_ini = QtGui.QLabel(self.frm_id)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_hor_ini.sizePolicy().hasHeightForWidth())
        self.lbl_hor_ini.setSizePolicy(sizePolicy)
        self.lbl_hor_ini.setObjectName(_fromUtf8("lbl_hor_ini"))
        self.gridLayout.addWidget(self.lbl_hor_ini, 2, 0, 1, 1)
        self.tedHorIni = QtGui.QTimeEdit(self.frm_id)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tedHorIni.sizePolicy().hasHeightForWidth())
        self.tedHorIni.setSizePolicy(sizePolicy)
        self.tedHorIni.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tedHorIni.setReadOnly(True)
        self.tedHorIni.setTime(QtCore.QTime(0, 0, 0))
        self.tedHorIni.setTimeSpec(QtCore.Qt.LocalTime)
        self.tedHorIni.setObjectName(_fromUtf8("tedHorIni"))
        self.gridLayout.addWidget(self.tedHorIni, 2, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 3, 1, 2)
        self.verticalLayout.addWidget(self.frm_id)
        self.tab_exe = QtGui.QTabWidget(self.wid_data)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_exe.sizePolicy().hasHeightForWidth())
        self.tab_exe.setSizePolicy(sizePolicy)
        self.tab_exe.setObjectName(_fromUtf8("tab_exe"))
        self.pag_anv = QtGui.QWidget()
        self.pag_anv.setObjectName(_fromUtf8("pag_anv"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.pag_anv)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.gbx_anv = QtGui.QGroupBox(self.pag_anv)
        self.gbx_anv.setObjectName(_fromUtf8("gbx_anv"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.gbx_anv)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.qtw_anv = QtGui.QTableWidget(self.gbx_anv)
        self.qtw_anv.setObjectName(_fromUtf8("qtw_anv"))
        self.qtw_anv.setColumnCount(0)
        self.qtw_anv.setRowCount(0)
        self.verticalLayout_3.addWidget(self.qtw_anv)
        self.verticalLayout_5.addWidget(self.gbx_anv)
        self.frame = QtGui.QFrame(self.pag_anv)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.btnTrfNew = QtGui.QPushButton(self.frame)
        self.btnTrfNew.setIcon(icon)
        self.btnTrfNew.setObjectName(_fromUtf8("btnTrfNew"))
        self.horizontalLayout_2.addWidget(self.btnTrfNew)
        self.btnTrfEdit = QtGui.QPushButton(self.frame)
        self.btnTrfEdit.setIcon(icon1)
        self.btnTrfEdit.setObjectName(_fromUtf8("btnTrfEdit"))
        self.horizontalLayout_2.addWidget(self.btnTrfEdit)
        self.btnTrfDel = QtGui.QPushButton(self.frame)
        self.btnTrfDel.setIcon(icon2)
        self.btnTrfDel.setObjectName(_fromUtf8("btnTrfDel"))
        self.horizontalLayout_2.addWidget(self.btnTrfDel)
        self.verticalLayout_5.addWidget(self.frame)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/dbedit/view.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tab_exe.addTab(self.pag_anv, icon3, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tab_exe)
        self.verticalLayout_4.addWidget(self.splitter)
        self.frm_dbb = QtGui.QFrame(CDlgExeDataNEW)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frm_dbb.sizePolicy().hasHeightForWidth())
        self.frm_dbb.setSizePolicy(sizePolicy)
        self.frm_dbb.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frm_dbb.setFrameShadow(QtGui.QFrame.Raised)
        self.frm_dbb.setObjectName(_fromUtf8("frm_dbb"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frm_dbb)
        self.horizontalLayout_3.setContentsMargins(-1, 9, -1, 9)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.bbxExeTab = QtGui.QDialogButtonBox(self.frm_dbb)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bbxExeTab.sizePolicy().hasHeightForWidth())
        self.bbxExeTab.setSizePolicy(sizePolicy)
        self.bbxExeTab.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bbxExeTab.setObjectName(_fromUtf8("bbxExeTab"))
        self.horizontalLayout_3.addWidget(self.bbxExeTab)
        self.verticalLayout_4.addWidget(self.frm_dbb)

        self.retranslateUi(CDlgExeDataNEW)
        self.tab_exe.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(CDlgExeDataNEW)

    def retranslateUi(self, CDlgExeDataNEW):
        CDlgExeDataNEW.setWindowTitle(_translate("CDlgExeDataNEW", "Edição de Exercícios", None))
        self.btnExeNew.setText(_translate("CDlgExeDataNEW", "Novo", None))
        self.btnExeEdit.setText(_translate("CDlgExeDataNEW", "Edita", None))
        self.btnExeDel.setText(_translate("CDlgExeDataNEW", "Remove", None))
        self.lbl_indc.setText(_translate("CDlgExeDataNEW", "Indicativo:", None))
        self.lbl_desc.setText(_translate("CDlgExeDataNEW", "Descrição:", None))
        self.txtExeID.setText(_translate("CDlgExeDataNEW", "TEST001", None))
        self.lbl_hor_ini.setText(_translate("CDlgExeDataNEW", "Hora inicial:", None))
        self.tedHorIni.setDisplayFormat(_translate("CDlgExeDataNEW", "h:mm", None))
        self.gbx_anv.setTitle(_translate("CDlgExeDataNEW", "Tráfegos", None))
        self.qtw_anv.setSortingEnabled(True)
        self.btnTrfNew.setText(_translate("CDlgExeDataNEW", "Novo", None))
        self.btnTrfEdit.setText(_translate("CDlgExeDataNEW", "Edita", None))
        self.btnTrfDel.setText(_translate("CDlgExeDataNEW", "Remove", None))
        self.tab_exe.setTabText(self.tab_exe.indexOf(self.pag_anv), _translate("CDlgExeDataNEW", "Tráfegos", None))

import resources_rc
