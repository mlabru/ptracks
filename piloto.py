#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
piloto

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

revision 0.2  2016/mar  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2016/03"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import multiprocessing
import sys
import threading

import sip
sip.setapi('QString', 2)

# control
import control.piloto.control_piloto as control

# -------------------------------------------------------------------------------------------------
def main():

    # instancia o controller
    l_control = control.CControlPiloto()
    assert l_control

    # ativa o controller
    l_control.start()

    # obtém a view
    l_view = l_control.view
    assert l_view

    # ativa a viewer
    l_view.run()
    '''
    print "threadings:", threading.enumerate ()

    import traceback

    for thread_id, frame in sys._current_frames ().iteritems ():
        name = thread_id
        for thread in threading.enumerate ():
            if thread.ident == thread_id:
                name = thread.name

        traceback.print_stack ( frame )
    '''
    # termina
    sys.exit()

# -------------------------------------------------------------------------------------------------
# this is the bootstrap process

if "__main__" == __name__:

    # logger
    logging.basicConfig()

    # multiprocessing logger
    multiprocessing.log_to_stderr()

    # run application
    main()

# < the end >--------------------------------------------------------------------------------------
