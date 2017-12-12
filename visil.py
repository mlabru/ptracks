#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
visil

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

# python library
import logging
import multiprocessing
import sys
import threading

import sip
sip.setapi('QString', 2)

# control
import control.visil.control_visil as control

# -------------------------------------------------------------------------------------------------
# void (void)
def main():

    # instancia o control
    l_control = control.CControlVisil()
    assert l_control

    try:
        # ativa o control
        l_control.start()
                    
        # obtém a view
        l_view = l_control.view
        assert l_view
                                                          
        # ativa a viewer
        l_view.run()
                                                                          
    # trata interrupções
    except KeyboardInterrupt as SystemExit:

        # termina a aplicação
        l_control.cbk_termina()
    '''
    print "threadings:", threading.enumerate()

    import traceback

    for thread_id, frame in sys._current_frames().iteritems():
        name = thread_id
        for thread in threading.enumerate():
            if thread.ident == thread_id:
                name = thread.name

        traceback.print_stack(frame)
    '''
    # termina
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
