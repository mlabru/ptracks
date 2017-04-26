#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
strip_basic

DOCUMENT ME!

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

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/12"

# < imports >--------------------------------------------------------------------------------------

# Python library
import logging

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

# < variáveis globais >----------------------------------------------------------------------------

# callsign
g_Callsign = ["AAL9717", "AZU8112", "BGR6707", "FWK6313", "GOL7883", "JAL3922", "QNT9974", "TAM9261", ]

# origem
g_Orig = ["SBSP", "SBGL", "SBCW", "SBBR", "SBPA", "SBCT", "SBGR", "SBGL", "SBUT", "SBBR"]

# destino
g_Dest = ["JFK", "CDG", "HTW", "KVV", "CDG", "FRX", "JFK", "MMO", "PRG", "STT"]

# runway
g_Rwy = ["W18", "W12", "R31", "R47", "H52", "H64", "H73", "L89", "L95", "L10"]

# altitude
g_Alt = [100, 200, 300, 400, 500, 600, 700, 800, 900, 105]

# proa
g_Proa = [254, 211, 35, 47, 59, 64, 73, 89, 93, 105]

# velocidade
g_Vel = [650, 200, 250, 300, 350, 400, 450, 500, 550, 600]

# designador
g_Dsgn = ["B747-800", "B747-800", "B747-800", "B747-800", "B747", "B747", "B747", "B747", "B747", "B747"]

# cor do fundo
g_SH = ["background-color: rgb(255, 200,  20);",
        "background-color: rgb(255, 180,  40);",
        "background-color: rgb(255, 160,  60);",
        "background-color: rgb(255, 140,  80);",
        "background-color: rgb(255, 120, 100);",
        "background-color: rgb(255, 100, 120);",
        "background-color: rgb(255,  80, 140);",
        "background-color: rgb(255,  60, 160);",
        "background-color: rgb(255,  40, 180);",
        "background-color: rgb(255,  20, 200);"]

# < class CWidStripBasic >-------------------------------------------------------------------------

class CWidStripBasic(QtGui.QWidget):
    """
    widget de uma strip
    """
    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __init__(self, f_control, f_iI, f_parent=None):
        """
        constructor
        widget de uma strip

        @param f_control: control manager
        @param f_parent: janela vinculada ou None
        """
        # init super class
        super(CWidStripBasic, self).__init__()

        # verifica parâmetros de entrada
        assert f_control

        # salva o control manager localmente
        self._control = f_control

        # salva o event manager localmente
        self._event = f_control.event
        assert self._event

        # salva o model manager localmente
        self._model = f_control.model
        assert self._model

        # create main Ui
        self.setupUi(f_iI % len(g_Callsign))

    # ---------------------------------------------------------------------------------------------
    def setupUi(self, f_iI):
        # cria a fonte
        l_font = QtGui.QFont()
        assert l_font

        # cria linhas verticais...
        l_lineV = QtGui.QFrame()
        l_lineV.setFrameShadow(QtGui.QFrame.Plain)
        l_lineV.setLineWidth(1)
        l_lineV.setFrameShape(QtGui.QFrame.VLine)
        l_lineV.setFrameShadow(QtGui.QFrame.Sunken)

        l_lineV0 = QtGui.QFrame()
        l_lineV0.setFrameShadow(QtGui.QFrame.Plain)
        l_lineV0.setLineWidth(1)
        l_lineV0.setFrameShape(QtGui.QFrame.VLine)
        l_lineV0.setFrameShadow(QtGui.QFrame.Sunken)

        l_lineV1 = QtGui.QFrame()
        l_lineV1.setFrameShadow(QtGui.QFrame.Plain)
        l_lineV1.setLineWidth(1)
        l_lineV1.setFrameShape(QtGui.QFrame.VLine)
        l_lineV1.setFrameShadow(QtGui.QFrame.Sunken)

        l_lineV2 = QtGui.QFrame()
        l_lineV2.setFrameShadow(QtGui.QFrame.Plain)
        l_lineV2.setLineWidth(1)
        l_lineV2.setFrameShape(QtGui.QFrame.VLine)
        l_lineV2.setFrameShadow(QtGui.QFrame.Sunken)

        l_lineV3 = QtGui.QFrame()
        l_lineV3.setFrameShadow(QtGui.QFrame.Plain)
        l_lineV3.setLineWidth(1)
        l_lineV3.setFrameShape(QtGui.QFrame.VLine)
        l_lineV3.setFrameShadow(QtGui.QFrame.Sunken)

        # e horizontais
        l_lineH = QtGui.QFrame()
        l_lineH.setFrameShadow(QtGui.QFrame.Plain)
        l_lineH.setLineWidth(1)
        l_lineH.setFrameShape(QtGui.QFrame.HLine)
        l_lineH.setFrameShadow(QtGui.QFrame.Sunken)

        # spacers
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

        # style sheet
        # l_sStyleSheet10 = "color: rgb(0, 0, 0);\nfont: 10pt \"Ubuntu Condensed\";"
        # l_sStyleSheet14 = "color: rgb(0, 0, 0);\nfont: 14pt \"Ubuntu Condensed\";"

        l_sStyleSheet10 = "color: rgb(0, 0, 0);\nfont: 10pt \"Monospace\";"
        l_sStyleSheet14 = "color: rgb(0, 0, 0);\nfont: 14pt \"Monospace\";"

        # ajusta o tamanho
        self.resize(300, 63)
        self.setStyleSheet(g_SH[f_iI])
        self.setContentsMargins(1, 1, 1, 1)

        # callsign
        self._lblCallsign = QtGui.QLabel()
        assert self._lblCallsign

        self._lblCallsign.setStyleSheet(l_sStyleSheet14)
        self._lblCallsign.setText(g_Callsign[f_iI])

        # origem
        self._lblOrig = QtGui.QLabel()
        assert self._lblOrig

        self._lblOrig.setStyleSheet(l_sStyleSheet10)
        self._lblOrig.setText(g_Orig[f_iI])

        # _/_
        l_label = QtGui.QLabel()
        l_label.setStyleSheet(l_sStyleSheet10)
        l_label.setText(" / ")

        # destino
        self._lblDest = QtGui.QLabel()
        assert self._lblDest

        self._lblDest.setStyleSheet(l_sStyleSheet10)
        self._lblDest.setText(g_Dest[f_iI])

        # runway
        self._lblRwy = QtGui.QLabel()
        assert self._lblRwy

        self._lblRwy.setStyleSheet(l_sStyleSheet10)
        self._lblRwy.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self._lblRwy.setText(g_Rwy[f_iI])

        # altitude
        self._lblAlt = QtGui.QLabel()
        assert self._lblAlt

        self._lblAlt.setStyleSheet(l_sStyleSheet10)
        self._lblAlt.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self._lblAlt.setText(str(g_Alt[f_iI]))

        # proa
        self._lblProa = QtGui.QLabel()
        assert self._lblProa

        self._lblProa.setStyleSheet(l_sStyleSheet10)
        self._lblProa.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self._lblProa.setText(str(g_Proa[f_iI]))

        # velocidade
        self._lblVel = QtGui.QLabel()
        assert self._lblVel

        self._lblVel.setStyleSheet(l_sStyleSheet10)
        self._lblVel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self._lblVel.setText(str(g_Vel[f_iI]))

        # designador
        self._lblDsgn = QtGui.QLabel()
        assert self._lblDsgn

        self._lblDsgn.setStyleSheet(l_sStyleSheet10)
        self._lblDsgn.setText(g_Dsgn[f_iI])

        #
        # monta a linha 1 da strip

        l_widLin1 = QtGui.QWidget()

        l_hloLin1 = QtGui.QHBoxLayout(l_widLin1)
        l_hloLin1.setSpacing(5)
        l_hloLin1.setMargin(1)
        l_hloLin1.setMargin(0)

        l_hloLin1.addWidget(self._lblOrig)
        l_hloLin1.addWidget(l_label)
        l_hloLin1.addWidget(self._lblDest)
        l_hloLin1.addWidget(l_lineV0)
        l_hloLin1.addWidget(self._lblRwy)
        l_hloLin1.addWidget(l_lineV1)
        l_hloLin1.addWidget(self._lblAlt)
        l_hloLin1.addWidget(l_lineV2)
        l_hloLin1.addWidget(self._lblProa)
        l_hloLin1.addWidget(l_lineV3)
        l_hloLin1.addWidget(self._lblVel)
        l_hloLin1.addItem(spacerItem)

        #
        # monta a linha 2 da strip

        l_widLin2 = QtGui.QWidget()

        l_hloLin2 = QtGui.QHBoxLayout(l_widLin2)
        l_hloLin2.setSpacing(5)
        l_hloLin2.setMargin(1)
        l_hloLin2.setMargin(0)

        # monta a linha 2 da strip
        l_hloLin2.addWidget(self._lblDsgn)
        l_hloLin2.addItem(spacerItem1)

        #
        # monta o lado direito da strip

        l_widDir = QtGui.QWidget()

        l_hvoDir = QtGui.QVBoxLayout(l_widDir)
        l_hvoDir.setSpacing(5)
        l_hvoDir.setMargin(1)
        l_hvoDir.setMargin(0)

        l_hvoDir.addWidget(l_widLin1)
        l_hvoDir.addWidget(l_lineH)
        l_hvoDir.addWidget(l_widLin2)

        #
        # monta o corpo da strip

        l_hloStrip = QtGui.QHBoxLayout(self)
        l_hloStrip.setSpacing(5)
        l_hloStrip.setMargin(1)
        l_hloStrip.setMargin(0)

        l_hloStrip.addWidget(self._lblCallsign)
        # l_hloStrip.addWidget ( l_lineV )
        l_hloStrip.addWidget(l_widDir)

# < the end >--------------------------------------------------------------------------------------
