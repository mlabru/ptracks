#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
prc_validator

validador de procedimentos

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

# < class CPrcValidator >--------------------------------------------------------------------------

class CPrcValidator(QtGui.QValidator):
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
        super(CPrcValidator, self).__init__(f_parent)

        # model
        self.__model = f_parent.model
        assert self.__model

    # ---------------------------------------------------------------------------------------------
    def fixup(self, fs_proc):
        """
        fixup
        """
        return fs_proc

    # ---------------------------------------------------------------------------------------------
    def validate(self, fs_proc, fi_pos):
        """
        validate
        """
        # clear to go
        assert self.__model

        # convert
        ls_proc = str(fs_proc).strip().upper()

        # string vazia ?
        if len(ls_proc) < 0:
            # return tuple
            return (QtGui.QValidator.Invalid, ls_proc, fi_pos)

        # none ?
        if "NONE" == ls_proc:
            # return tuple
            return (QtGui.QValidator.Acceptable, ls_proc, fi_pos)

        # letras do procedimento ?
        if fi_pos <= 3:
            # letras do procedimento válidas ?
            if ("APX".startswith(ls_proc) or "ESP".startswith(ls_proc) or 
                "SUB".startswith(ls_proc) or "TRJ".startswith(ls_proc) or
                "NON".startswith(ls_proc)): 
                # return tuple
                return (QtGui.QValidator.Intermediate, ls_proc, fi_pos)

            # return tuple
            return (QtGui.QValidator.Invalid, ls_proc, fi_pos)

        # 3 letras do procedimento (trigrama)
        ls_tri = ls_proc[:3]

        # número do procedimento
        ls_num = ls_proc[3:]

        # número do procedimento inválido ?
        if not ls_num.isdigit():
            # return tuple
            return (QtGui.QValidator.Invalid, ls_proc, fi_pos)

        # número do procedimento
        li_prc = int(ls_num)

        # aproximação ?
        if "APX" == ls_tri:
            if li_prc in self.__model.dct_apx:
                # return tuple
                return (QtGui.QValidator.Acceptable, ls_proc, fi_pos)

            # senão,...
            else:
                # para todas as aproximações...
                for l_key in self.__model.dct_apx.keys():
                    # match início da string ?
                    if str(l_key).startswith(ls_num):
                        # return tuple
                        return (QtGui.QValidator.Intermediate, ls_proc, fi_pos)

        # espera ?
        elif "ESP" == ls_tri:
            if li_prc in self.__model.dct_esp:
                # return tuple
                return (QtGui.QValidator.Acceptable, ls_proc, fi_pos)

            # senão,...
            else:
                # para todas as esperas...
                for l_key in self.__model.dct_esp.keys():
                    # match início da string ?
                    if str(l_key).startswith(ls_num):
                        # return tuple
                        return (QtGui.QValidator.Intermediate, ls_proc, fi_pos)

        # subida ?
        elif "SUB" == ls_tri:
            if li_prc in self.__model.dct_sub:
                # return tuple
                return (QtGui.QValidator.Acceptable, ls_proc, fi_pos)

            # senão,...
            else:
                # para todas as subidas...
                for l_key in self.__model.dct_sub.keys():
                    # match início da string ?
                    if str(l_key).startswith(ls_num):
                        # return tuple
                        return (QtGui.QValidator.Intermediate, ls_proc, fi_pos)

        # trajetória ?
        elif "TRJ" == ls_tri:
            if li_prc in self.__model.dct_trj:
                # return tuple
                return (QtGui.QValidator.Acceptable, ls_proc, fi_pos)

            # senão,...
            else:
                # para todas as trajetórias...
                for l_key in self.__model.dct_trj.keys():
                    # match início da string ?
                    if str(l_key).startswith(ls_num):
                        # return tuple
                        return (QtGui.QValidator.Intermediate, ls_proc, fi_pos)

        # return tuple
        return (QtGui.QValidator.Invalid, ls_proc, fi_pos)

# < the end >--------------------------------------------------------------------------------------
