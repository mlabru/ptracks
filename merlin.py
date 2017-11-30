#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
merlin

configurador de simulação

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

revision 0.2  2015/dez  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2016/01"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import sys
sys.path.insert(0, ".")

import sip
sip.setapi('QString', 2)

# control
import control.wizard.control_wizard as control

# -------------------------------------------------------------------------------------------------
def main():
    """
    initalize and kick off the main loop
    """
    # instancia o controller
    l_control = control.CControlWizard()
    assert l_control

    # ativa o controller
    l_control.start()

    # obtém o view manager
    l_view = l_control.view
    assert l_view

    # ativa a viewer
    sys.exit(l_view.run())

# -------------------------------------------------------------------------------------------------
# this is the bootstrap process

if "__main__" == __name__:

    # logger
    logging.basicConfig()

    # disable logging
    #logging.disable(sys.maxint)

    # run application
    main()

# < the end >--------------------------------------------------------------------------------------
