#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
prf_validator

validador de performances

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

# < class CPrfValidator >--------------------------------------------------------------------------

class CPrfValidator(QtGui.QValidator):
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
        super(CPrfValidator, self).__init__(f_parent)

        # model
        self.__model = f_parent.model
        assert self.__model

    # ---------------------------------------------------------------------------------------------
    def fixup(self, fs_prf):
        """
        fixup
        """
        return fs_prf

    # ---------------------------------------------------------------------------------------------
    def validate(self, fs_prf, fi_pos):
        """
        validate
        """
        # clear to go
        assert self.__model

        # convert
        ls_prf = str(fs_prf).strip().upper()

        # string vazia ?
        if len(fs_prf) < 0:
            # return tuple
            return (QtGui.QValidator.Invalid, ls_prf, fi_pos)

        # performance válida ?
        if ls_prf in self.__model.dct_prf:
            # return tuple
            return (QtGui.QValidator.Acceptable, ls_prf, fi_pos)

        # para todos as performances...
        for l_key in self.__model.dct_prf.keys():
            # match início da string ?
            if l_key.startswith(ls_prf):
                # return tuple
                return (QtGui.QValidator.Intermediate, ls_prf, fi_pos)

        # return tuple
        return (QtGui.QValidator.Invalid, ls_prf, fi_pos)

# < the end >--------------------------------------------------------------------------------------
