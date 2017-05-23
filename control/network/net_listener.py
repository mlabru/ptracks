#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
net_listener

net listener

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
desmembramento do netManager
inclusão do config_manager e event_manager

revision 0.1  2014/nov  mlabru
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.3$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import errno
import logging
import multiprocessing
import socket
import struct
import time

# model 
import model.common.glb_data as gdata

# control
import control.common.glb_defs as gdefs
import control.control_debug as cdbg

# < class CNetListener >---------------------------------------------------------------------------

class CNetListener(multiprocessing.Process):
    """
    net listener
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, ft_ifce, fs_addr, fi_port, f_queue):
        """
        initializes network listener

        @param ft_ifce: tupla in/out de interfaces. ('eth0', 'eth0')
        @param fs_addr: endereço multicast. ('225.12.2')
        @param fi_port: porta. (1970)
        @param f_queue: queue de dados
        """
        # check input
        assert fs_addr
        assert fi_port
        assert f_queue

        # init super class
        super(CNetListener, self).__init__()

        # queue de dados
        self.__q_queue = f_queue

        # cria o socket de recebimento
        self.__fd_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        assert self.__fd_recv

        # especificou uma interface ?
        if ft_ifce[0] is not None:
            # seleciona a interface (from socket.h, SO_BINDTODEVICE 25)
            self.__fd_recv.setsockopt(socket.SOL_SOCKET, 25, ft_ifce[0])

        # set some options to make it multicast-friendly
        self.__fd_recv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            # set some options to make it multicast-friendly
            self.__fd_recv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        # em caso de erro...
        except AttributeError as ls_err:
            # logger
            l_log = logging.getLogger("CNetListener::__init__")
            l_log.setLevel(logging.WARNING)
            l_log.warning("<E01: some systems don't support SO_REUSEPORT:[{}]".format(ls_err))

        # set some options to make it multicast-friendly
        # self.__fd_recv.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_TTL, 20)
        self.__fd_recv.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1)

        # bind udp port. Better use:
        self.__fd_recv.bind((fs_addr, fi_port))

        # instead of: self.__fd_recv.bind(('', fi_port))
        # ... because if you want to listen to multiple mcast groups on the same port, you'll get
        # all messages on all listeners

        # set mcast group
        l_mreq = struct.pack("4sl", socket.inet_aton(fs_addr), socket.INADDR_ANY)
        assert l_mreq

        # set some more multicast options
        self.__fd_recv.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, l_mreq)

    # ---------------------------------------------------------------------------------------------
    def run(self):
        """
        drive application
        """
        # clear to go
        assert self.__fd_recv

        # enquanto não inicia...
        while not gdata.G_KEEP_RUN:
            # aguarda 1 seg
            time.sleep(1)

        # non-blocking socket
        self.__fd_recv.settimeout(0.0)
        self.__fd_recv.setblocking(0)

        # application loop
        while gdata.G_KEEP_RUN:
            try:
                # recebe uma mensagem (de até 512 bytes)
                l_data, l_addr = self.__fd_recv.recvfrom(512)
                # cdbg.M_DBG.debug("data: {} received from: {}".format(l_data, l_addr))

                # divide a mensagem em seus componentes
                llst_data = l_data.split(gdefs.D_MSG_SEP)
                # cdbg.M_DBG.debug("llst_data: {}".format(llst_data))

                # versão da mensagem não reconhecida ?
                if gdefs.D_MSG_VRS != int(llst_data[0]):
                    # próxima mensagem
                    continue

                # mensagem válida ?
                if int(llst_data[1]) in gdefs.SET_MSG_VALIDAS:
                    # coloca a mensagem na queue
                    self.__q_queue.put(llst_data[1:])

                # mensagem não reconhecida ou inválida
                else:
                    # logger
                    l_log = logging.getLogger("CNetListener::run")
                    l_log.setLevel(logging.WARNING)
                    l_log.warning("<E01: unknow:[{}].".format(llst_data[2:]))

            # em caso de erro...
            except socket.timeout, l_err:
                pass

            # em caso de erro...    
            except socket.error, l_err:
                # get error code
                li_err = l_err.args[0]

                # data unavailable ?
                if (errno.EAGAIN == li_err) or (errno.EWOULDBLOCK == li_err):
                    continue

                # senão, a "real" error occurred
                else:
                    # logger
                    l_log = logging.getLogger("CNetListener::run")
                    l_log.setLevel(logging.WARNING)
                    l_log.warning("<E02: socket receive error: {}.".format(l_err))

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    def get_data(self):
        """
        DOCUMENT ME!
        """
        # return list
        llst_data = []

        # fila tem dados ?
        if self.__q_queue:
            # primeiro item da fila
            llst_data = self.__q_queue.pop(0)

        # dado recebido
        return llst_data

    # ---------------------------------------------------------------------------------------------
    @property
    def queue(self):
        """
        get queue
        """
        return self.__q_queue

# < the end >--------------------------------------------------------------------------------------
