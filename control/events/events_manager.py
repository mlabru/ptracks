# /usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
event_manager

coordinates communications between the model, views and controllers through the use of events

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

# < class CEventsManager >-------------------------------------------------------------------------

class CEventsManager(object):
    """
    coordinates communications between the model, views and controllers through the use of events
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # weakref
        from weakref import WeakKeyDictionary

        # listeners dictionary
        self.__dct_listeners = WeakKeyDictionary()
        assert self.__dct_listeners is not None

        # event queue
        self.__lst_event_queue = []

    # ---------------------------------------------------------------------------------------------
    def post(self, f_event):
        """
        difundir um evento a todos os membros da lista de recebedores

        @param f_event: evento a disseminar
        """
        # para todos os listeners cadastrados...
        for l_listener in self.__dct_listeners:
            # ...envio a notificação do evento
            l_listener.notify(f_event)

    # ---------------------------------------------------------------------------------------------
    def register_listener(self, f_listener):
        """
        register the object as listener

        @param f_listener: objeto a registrar
        """
        # coloca o objeto na lista de recebedores de eventos
        self.__dct_listeners[f_listener] = True

    # ---------------------------------------------------------------------------------------------
    def unregister_listener(self, f_listener):
        """
        unregister the object as listener

        @param f_listener: objeto a remover
        """
        # o objeto está na lista de recebedores de eventos ?
        if f_listener in self.__dct_listeners:
            # retira o objeto na lista de recebedores de eventos
            del self.__dct_listeners[f_listener]

# < the end >--------------------------------------------------------------------------------------
