#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
events_flight

generic event superclass. What follows is a list of all events. None of these classes should
perform any tasks, as that could introduce vulnerabilities

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# control
import control.events.events_model as model

# < class CFlight >--------------------------------------------------------------------------------

class CFlight(model.CEventsModel):
    """
    CFlight event class
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_callsign):
        """
        contructor
        """
        # init super class
        super(CFlight, self).__init__()

        # herdados de CEventsModel
        # self.s_name    # event name

        # save event id
        self.s_name = "Flight event"

        # save callsign
        self.__s_callsign = fs_callsign

    # ---------------------------------------------------------------------------------------------
    @property
    def s_callsign(self):
        return self.__s_callsign

# < class CFlightExplode >--------------------------------------------------------------------------

class CFlightExplode(CFlight):
    """
    CFlightExplode event class
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_callsign):
        """
        contructor
        """
        # init super class
        super(CFlightExplode, self).__init__(fs_callsign)

        # herdados de CFlight
        # self.s_name        # event name
        # self.s_callsign    # callsign

        # save event id
        self.s_name = "FlightExplode event"

# < class CFlightKill >-----------------------------------------------------------------------------

class CFlightKill(CFlight):
    """
    CFlightKill event class
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_callsign):
        """
        contructor
        """
        # init super class
        super(CFlightKill, self).__init__(fs_callsign)

        # herdados de CFlight
        # self.s_name        # event name
        # self.s_callsign    # callsign

        # save event id
        self.s_name = "FlightKill event"

# < class CFlightUpdate >---------------------------------------------------------------------------

class CFlightUpdate(CFlight):
    """
    CFlightUpdate event class
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_callsign):
        """
        contructor
        """
        # init super class
        super(CFlightUpdate, self).__init__(fs_callsign)

        # herdados de CFlight
        # self.s_name        # event name
        # self.s_callsign    # callsign

        # save event id
        self.s_name = "FlightUpdate event"

# < the end >--------------------------------------------------------------------------------------
