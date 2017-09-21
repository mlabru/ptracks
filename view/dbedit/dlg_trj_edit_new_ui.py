# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './dlg_trj_edit_new.ui'
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

class Ui_CDlgTrjEditNEW(object):
    def setupUi(self, CDlgTrjEditNEW):
        CDlgTrjEditNEW.setObjectName(_fromUtf8("CDlgTrjEditNEW"))
        CDlgTrjEditNEW.resize(597, 135)
        self.verticalLayout = QtGui.QVBoxLayout(CDlgTrjEditNEW)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frmPrcID = QtGui.QFrame(CDlgTrjEditNEW)
        self.frmPrcID.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frmPrcID.setFrameShadow(QtGui.QFrame.Raised)
        self.frmPrcID.setObjectName(_fromUtf8("frmPrcID"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frmPrcID)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lblPrcID = QtGui.QLabel(self.frmPrcID)
        self.lblPrcID.setObjectName(_fromUtf8("lblPrcID"))
        self.gridLayout_2.addWidget(self.lblPrcID, 1, 0, 1, 1)
        self.qlePrcDesc = QtGui.QLineEdit(self.frmPrcID)
        self.qlePrcDesc.setReadOnly(False)
        self.qlePrcDesc.setObjectName(_fromUtf8("qlePrcDesc"))
        self.gridLayout_2.addWidget(self.qlePrcDesc, 2, 1, 1, 1)
        self.lblPrcDesc = QtGui.QLabel(self.frmPrcID)
        self.lblPrcDesc.setObjectName(_fromUtf8("lblPrcDesc"))
        self.gridLayout_2.addWidget(self.lblPrcDesc, 2, 0, 1, 1)
        self.qlePrcID = QtGui.QLineEdit(self.frmPrcID)
        self.qlePrcID.setObjectName(_fromUtf8("qlePrcID"))
        self.gridLayout_2.addWidget(self.qlePrcID, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.frmPrcID)
        self.bbxTrj = QtGui.QDialogButtonBox(CDlgTrjEditNEW)
        self.bbxTrj.setOrientation(QtCore.Qt.Horizontal)
        self.bbxTrj.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bbxTrj.setObjectName(_fromUtf8("bbxTrj"))
        self.verticalLayout.addWidget(self.bbxTrj)

        self.retranslateUi(CDlgTrjEditNEW)
        QtCore.QObject.connect(self.bbxTrj, QtCore.SIGNAL(_fromUtf8("accepted()")), CDlgTrjEditNEW.accept)
        QtCore.QObject.connect(self.bbxTrj, QtCore.SIGNAL(_fromUtf8("rejected()")), CDlgTrjEditNEW.reject)
        QtCore.QMetaObject.connectSlotsByName(CDlgTrjEditNEW)
        CDlgTrjEditNEW.setTabOrder(self.qlePrcID, self.qlePrcDesc)
        CDlgTrjEditNEW.setTabOrder(self.qlePrcDesc, self.bbxTrj)

    def retranslateUi(self, CDlgTrjEditNEW):
        CDlgTrjEditNEW.setWindowTitle(_translate("CDlgTrjEditNEW", "Dialog", None))
        self.lblPrcID.setText(_translate("CDlgTrjEditNEW", "Indicativo:", None))
        self.lblPrcDesc.setText(_translate("CDlgTrjEditNEW", "Descrição:", None))

