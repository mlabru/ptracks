#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
get_address

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

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import os

# -------------------------------------------------------------------------------------------------
def get_address(f_config, fs_addr_key):
    """
    @param f_config: gerente de configuração (config manager)
    @param fs_addr_key: address key
    """
    # check input
    assert f_config
    assert fs_addr_key

    # dicionário de configuração
    ldct_config = f_config.dct_config
    assert ldct_config is not None

    # canal de comunicação (3)
    li_canal = int(ldct_config.get("glb.canal", 3))

    assert (li_canal > 2) and (li_canal < 200)

    # monta o endereço ('235.0.0.3')
    ls_addr = "{}.{}".format(ldct_config.get(fs_addr_key, "235.0.0"), str(li_canal))
    assert ls_addr

    # porta (1961)
    li_port = int(ldct_config.get("net.port", 1961))

    # lista de interfaces disponíveis
    llst_iface = os.listdir("/sys/class/net/")
    assert llst_iface is not None

    # interface de entrada (None)
    ls_ifce_in = ldct_config.get("net.ifin", None)

    if ls_ifce_in not in llst_iface:
        ls_ifce_in = None

    # interface de saída (None)
    ls_ifce_out = ldct_config.get("net.iout", None)

    if ls_ifce_out not in llst_iface:
        ls_ifce_out = None

    # return
    return ((ls_ifce_in, ''), (ls_ifce_out, '')), ls_addr, li_port

# < the end >--------------------------------------------------------------------------------------
