#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
fix_validator

validador de fixos

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

revision 0.1  2017/ago  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/08"

# < imports >--------------------------------------------------------------------------------------

# python library

# PyQt4
from PyQt4 import QtCore
from PyQt4 import QtGui

# control
# import control.control_debug as cdbg

# < class CFixValidator >--------------------------------------------------------------------------

class CFixValidator(QtGui.QValidator):
    """
    validator model
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_parent):
        """
        constructor
        """
        # check input
        assert f_parent

        # init super class
        super(CFixValidator, self).__init__(f_parent)

        # model
        self.__model = f_parent.model
        assert self.__model

    # ---------------------------------------------------------------------------------------------
    def fixup(self, fs_fixo):
        """
        fixup
        """
        return fs_fixo

    # ---------------------------------------------------------------------------------------------
    def validate(self, fs_fixo, fi_pos):
        """
        validate
        """
        # clear to go
        assert self.__model

        # convert
        ls_fixo = str(fs_fixo).strip().upper()

        # string vazia ?
        if len(fs_fixo) < 0:
            # return
            return (QtGui.QValidator.Invalid, ls_fixo, fi_pos)

        # fixo válido ?
        if ls_fixo in self.__model.dct_fix:
            # return
            return (QtGui.QValidator.Acceptable, ls_fixo, fi_pos)

        # para todos os fixos...
        for l_key in self.__model.dct_fix.keys():
            # match início da string ?
            if l_key.startswith(ls_fixo):
                # return
                return (QtGui.QValidator.Intermediate, ls_fixo, fi_pos)

        # return
        return (QtGui.QValidator.Invalid, ls_fixo, fi_pos)

# < the end >--------------------------------------------------------------------------------------
