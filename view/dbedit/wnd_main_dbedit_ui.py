# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './wnd_main_dbedit.ui'
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

class Ui_CWndMainDBEdit(object):
    def setupUi(self, CWndMainDBEdit):
        CWndMainDBEdit.setObjectName(_fromUtf8("CWndMainDBEdit"))
        CWndMainDBEdit.resize(510, 497)
        CWndMainDBEdit.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        self.centralwidget = QtGui.QWidget(CWndMainDBEdit)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.frm_title = QtGui.QFrame(self.centralwidget)
        self.frm_title.setGeometry(QtCore.QRect(30, 20, 451, 211))
        self.frm_title.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 255);"))
        self.frm_title.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frm_title.setFrameShadow(QtGui.QFrame.Raised)
        self.frm_title.setObjectName(_fromUtf8("frm_title"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frm_title)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lbl_lin_1 = QtGui.QLabel(self.frm_title)
        self.lbl_lin_1.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 255);"))
        self.lbl_lin_1.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_lin_1.setObjectName(_fromUtf8("lbl_lin_1"))
        self.verticalLayout.addWidget(self.lbl_lin_1)
        self.lbl_lin_3 = QtGui.QLabel(self.frm_title)
        self.lbl_lin_3.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 255);"))
        self.lbl_lin_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_lin_3.setObjectName(_fromUtf8("lbl_lin_3"))
        self.verticalLayout.addWidget(self.lbl_lin_3)
        self.lbl_lin_4 = QtGui.QLabel(self.frm_title)
        self.lbl_lin_4.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 255);"))
        self.lbl_lin_4.setObjectName(_fromUtf8("lbl_lin_4"))
        self.verticalLayout.addWidget(self.lbl_lin_4)
        self.gbx_btn = QtGui.QGroupBox(self.centralwidget)
        self.gbx_btn.setGeometry(QtCore.QRect(20, 240, 471, 241))
        self.gbx_btn.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.gbx_btn.setFlat(False)
        self.gbx_btn.setCheckable(False)
        self.gbx_btn.setObjectName(_fromUtf8("gbx_btn"))
        self.gridLayout = QtGui.QGridLayout(self.gbx_btn)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btn_sub = QtGui.QPushButton(self.gbx_btn)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_sub.sizePolicy().hasHeightForWidth())
        self.btn_sub.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/execute.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_sub.setIcon(icon)
        self.btn_sub.setObjectName(_fromUtf8("btn_sub"))
        self.gridLayout.addWidget(self.btn_sub, 6, 0, 1, 1)
        self.btn_apx = QtGui.QPushButton(self.gbx_btn)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_apx.sizePolicy().hasHeightForWidth())
        self.btn_apx.setSizePolicy(sizePolicy)
        self.btn_apx.setIcon(icon)
        self.btn_apx.setObjectName(_fromUtf8("btn_apx"))
        self.gridLayout.addWidget(self.btn_apx, 5, 0, 1, 1)
        self.btn_prf = QtGui.QPushButton(self.gbx_btn)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_prf.sizePolicy().hasHeightForWidth())
        self.btn_prf.setSizePolicy(sizePolicy)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/compile16.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_prf.setIcon(icon1)
        self.btn_prf.setObjectName(_fromUtf8("btn_prf"))
        self.gridLayout.addWidget(self.btn_prf, 0, 1, 1, 1)
        self.btn_fix = QtGui.QPushButton(self.gbx_btn)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_fix.sizePolicy().hasHeightForWidth())
        self.btn_fix.setSizePolicy(sizePolicy)
        self.btn_fix.setIcon(icon1)
        self.btn_fix.setObjectName(_fromUtf8("btn_fix"))
        self.gridLayout.addWidget(self.btn_fix, 0, 0, 1, 1)
        self.btn_trj = QtGui.QPushButton(self.gbx_btn)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_trj.sizePolicy().hasHeightForWidth())
        self.btn_trj.setSizePolicy(sizePolicy)
        self.btn_trj.setIcon(icon)
        self.btn_trj.setObjectName(_fromUtf8("btn_trj"))
        self.gridLayout.addWidget(self.btn_trj, 6, 1, 1, 1)
        self.btn_esp = QtGui.QPushButton(self.gbx_btn)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_esp.sizePolicy().hasHeightForWidth())
        self.btn_esp.setSizePolicy(sizePolicy)
        self.btn_esp.setIcon(icon)
        self.btn_esp.setObjectName(_fromUtf8("btn_esp"))
        self.gridLayout.addWidget(self.btn_esp, 5, 1, 1, 1)
        self.btn_aer = QtGui.QPushButton(self.gbx_btn)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_aer.sizePolicy().hasHeightForWidth())
        self.btn_aer.setSizePolicy(sizePolicy)
        self.btn_aer.setIcon(icon1)
        self.btn_aer.setObjectName(_fromUtf8("btn_aer"))
        self.gridLayout.addWidget(self.btn_aer, 1, 0, 1, 1)
        self.btn_exe = QtGui.QPushButton(self.gbx_btn)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_exe.sizePolicy().hasHeightForWidth())
        self.btn_exe.setSizePolicy(sizePolicy)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/run16.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_exe.setIcon(icon2)
        self.btn_exe.setObjectName(_fromUtf8("btn_exe"))
        self.gridLayout.addWidget(self.btn_exe, 1, 1, 1, 1)
        self.btn_sai = QtGui.QPushButton(self.gbx_btn)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_sai.sizePolicy().hasHeightForWidth())
        self.btn_sai.setSizePolicy(sizePolicy)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/pixmaps/gamequit.xpm")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_sai.setIcon(icon3)
        self.btn_sai.setObjectName(_fromUtf8("btn_sai"))
        self.gridLayout.addWidget(self.btn_sai, 7, 1, 1, 1)
        CWndMainDBEdit.setCentralWidget(self.centralwidget)

        self.retranslateUi(CWndMainDBEdit)
        QtCore.QMetaObject.connectSlotsByName(CWndMainDBEdit)

    def retranslateUi(self, CWndMainDBEdit):
        CWndMainDBEdit.setWindowTitle(_translate("CWndMainDBEdit", "Edicão da Base de Dados", None))
        self.lbl_lin_1.setText(_translate("CWndMainDBEdit", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans\'; font-size:16pt; font-weight:600; color:#ffff00;\">TrackS</span></p></body></html>", None))
        self.lbl_lin_3.setText(_translate("CWndMainDBEdit", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans\'; font-size:16pt; font-weight:600; color:#ffff00;\">Gerador de Pistas</span></p></body></html>", None))
        self.lbl_lin_4.setText(_translate("CWndMainDBEdit", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Cantarell\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans\'; font-size:16pt; font-weight:600; color:#00007f;\">(C) 2016  ICEA - GMU </span></p></body></html>", None))
        self.btn_sub.setText(_translate("CWndMainDBEdit", "Subidas", None))
        self.btn_apx.setText(_translate("CWndMainDBEdit", "Aproximações", None))
        self.btn_prf.setText(_translate("CWndMainDBEdit", "Performances", None))
        self.btn_fix.setText(_translate("CWndMainDBEdit", "Fixos", None))
        self.btn_trj.setText(_translate("CWndMainDBEdit", "Trajetórias", None))
        self.btn_esp.setText(_translate("CWndMainDBEdit", "Esperas", None))
        self.btn_aer.setText(_translate("CWndMainDBEdit", "Aeródromos", None))
        self.btn_exe.setText(_translate("CWndMainDBEdit", "Exercícios", None))
        self.btn_sai.setText(_translate("CWndMainDBEdit", "Sair", None))

import resources_rc
