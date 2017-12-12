#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
newton

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
import multiprocessing
import sys

import sip
sip.setapi('QString', 2)

# control
import control.newton.control_newton as CControlNewton

# -------------------------------------------------------------------------------------------------
def main():

    # instancia o controller
    l_control = CControlNewton.CControlNewton()
    assert l_control

    try:
        # ativa o controle
        l_control.run()

    # trata interrupções
    except KeyboardInterrupt as SystemExit:

        # termina a aplicação
        l_control.cbk_termina()

    # termina a aplicação
    sys.exit()

# -------------------------------------------------------------------------------------------------
# this is the bootstrap process

if "__main__" == __name__:

    # logger
    logging.basicConfig()

    # disable logging
    # logging.disable(sys.maxint)

    # multiprocessing logger
    multiprocessing.log_to_stderr()

    # run application
    main()

# < the end >--------------------------------------------------------------------------------------
