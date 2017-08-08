#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
get_ctrl_net

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

revision 0.2  2017/aug  mlabru
pep8 style conventions

revision 0.1  2015/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/08"

# < imports >--------------------------------------------------------------------------------------

# python library
import array
import fcntl
import os
import socket
import struct
import sys

# control
import control.network.get_address as gaddr

# < local data >-----------------------------------------------------------------------------------

M_SIOCGIFCONF = 0x8912

# -------------------------------------------------------------------------------------------------
def get_ctrl_net(f_config, fs_addr_key):
    """
    @param f_config: gerente de configuração (config manager)
    @param fs_addr_key: address key
    """
    # check input
    assert f_config
    assert fs_addr_key

    # get address
    (lt_ifce_in, lt_ifce_out), ls_addr, li_port = gaddr.get_address(f_config, fs_addr_key)

    # lista de interfaces disponíveis
    llst_iface = os.listdir("/sys/class/net/")
    assert llst_iface is not None

    # for all interfaces...
    for l_tuple in all_interfaces():
        if "ctrl0net" in l_tuple[0]:
            # interface de saída
            lt_ifce_out = l_tuple

    if lt_ifce_out[0] not in llst_iface:
        # interface de saída (None)
        lt_ifce_out = (None, '')

    # return
    return (lt_ifce_in, lt_ifce_out), ls_addr, li_port

# -------------------------------------------------------------------------------------------------
def all_interfaces():

    # struct size
    li_struct_sz = 40 if sys.maxsize > 2 ** 32 else 32

    # socket
    l_sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # initial value
    li_max_possible = 8

    # for all interfaces...
    while True:
        # tamanho em bytes
        li_bytes = li_max_possible * li_struct_sz

        # names array
        lar_names = array.array('B', '\0' * li_bytes)

        # array length
        li_out_bytes = struct.unpack('iL', fcntl.ioctl(l_sck.fileno(), M_SIOCGIFCONF, struct.pack('iL', li_bytes, lar_names.buffer_info()[0])))[0]

        if li_out_bytes == li_bytes:
            li_max_possible *= 2

        else:
            break

    # names string
    ls_names = lar_names.tostring()

    # return
    return [(ls_names[li:li + 16].split('\0', 1)[0], socket.inet_ntoa(ls_names[li + 20:li + 24])) for li in xrange(0, li_out_bytes, li_struct_sz)]

# < the end >--------------------------------------------------------------------------------------
