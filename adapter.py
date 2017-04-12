#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
adapter

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

revision 0.1  2017/abr  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/04"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import multiprocessing
import sys

# control
import control.control_adapter as control

# -------------------------------------------------------------------------------------------------
def main():

    # instancia o control
    l_control = control.CControlAdapter()
    assert l_control

    try:
        # ativa o control
        l_control.start()
                    
    # trata interrupções
    except KeyboardInterrupt as SystemExit:

        # termina a aplicação
        l_control.cbk_termina()

    # termina
    sys.exit()

# -------------------------------------------------------------------------------------------------
# this is the bootstrap process
#
if "__main__" == __name__:

    # logger
    logging.basicConfig()

    # multiprocessing logger
    multiprocessing.log_to_stderr()
        
    # run application
    main()

# < the end >--------------------------------------------------------------------------------------
