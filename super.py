#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
super

dynamic configuration tool

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

revision 0.2  2017/jan  mlabru
pep8 style conventions

revision 0.1  2016/dez  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/01"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging

import sip
sip.setapi('QString', 2)

# control
import control.super.control_super as control

# -------------------------------------------------------------------------------------------------
def main():
    """
    initalize and kick off the main loop
    """
    # instancia o controller
    l_control = control.CControlSuper()
    assert l_control

    # executa em modo interativo ?
    if l_control.dct_config["spr.gui"]:

        # ativa o controller
        l_control.start()

        # obtém a view
        l_view = l_control.view
        assert l_view

        # ativa a viewer
        l_view.run()

    # senão,...
    else:
        # envia o comando
        l_control.send()

# -------------------------------------------------------------------------------------------------
# this is the bootstrap process

if "__main__" == __name__:

    # logger
    logging.basicConfig()

    # run application
    main()

# < the end >--------------------------------------------------------------------------------------
