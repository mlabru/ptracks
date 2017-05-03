#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
net_sender

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

revision 0.3  2015/nov  mlabru
pep8 style conventions

revision 0.2  2014/nov  mlabru
desmembramento do NetManager
inclusão do config_manager e event_manager

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.3$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import multiprocessing
import socket

# control
# import control.control_debug as cdbg

# < class CNetSender >-----------------------------------------------------------------------------

class CNetSender(multiprocessing.Process):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, ft_ifce, fs_addr, fi_port, f_queue):
        """
        initializes network sender

        @param ft_ifce: tupla in/out de interfaces. ('eth0', 'eth0')
        @param fs_addr: endereço ('224.1.2.3')
        @param fi_port: porta (1970)
        @param f_queue: queue de mensagens
        """
        # check input
        assert fs_addr
        assert fi_port
        assert f_queue

        # init super class
        super(CNetSender, self).__init__()

        # data queue
        self.__queue = f_queue

        # tupla endereço e porta
        self.__t_addr = (fs_addr, fi_port)

        # cria o socket de envio
        self.__fd_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        assert self.__fd_send

        # especificou uma interface ?
        if ft_ifce[1] is not None:
            # seleciona a interface (from socket.h, SO_BINDTODEVICE 25)
            self.__fd_send.setsockopt(socket.SOL_SOCKET, 25, ft_ifce[1])

        # config sender socket
        self.__fd_send.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

        # non-blocking socket
        self.__fd_send.settimeout(0.0)
        self.__fd_send.setblocking(0)

    # ---------------------------------------------------------------------------------------------
    def send_data(self, fs_msg):
        """
        send message

        @param fs_msg: DOCUMENT ME!
        """
        # clear to go
        assert self.__fd_send

        try:
            # send message
            self.__fd_send.sendto(fs_msg, self.__t_addr)
            # cdbg.M_DBG.debug("fs_msg: {} to: {}".format(fs_msg, self.__t_addr))
        
        # em caso de não enviar a mensagen...
        except Exception, l_err:
            # logger
            l_log = logging.getLogger("CNetSender::send_data")
            l_log.setLevel(logging.WARNING)
            l_log.warning("<E01: socket send error: {}.".format(l_err))

# < the end >--------------------------------------------------------------------------------------
