#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
events_basic

what follows is a list of all events. None of these classes should perform any tasks, as that
could introduce vulnerabilities if and when I write the netcode

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
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# control
import events_model as model  # control.events.events_model as model

# < class CChange >--------------------------------------------------------------------------------

class CChange(model.CEventsModel):
    """
    data changed event class
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # init super class
        super(CChange, self).__init__()

        # herdados de CEventsModel
        # self.s_name    # event name

        self.s_name = "Data Changed event"

# < class CFreeze >--------------------------------------------------------------------------------

class CFreeze(model.CEventsModel):
    """
    freeze event class
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fv_freeze):
        """
        constructor
        """
        # init super class
        super(CFreeze, self).__init__()

        # herdados de CEventsModel
        # self.s_name    # event name

        # event name
        self.s_name = "Freeze event"

        # freeze flag
        self.__v_freeze = fv_freeze

    # ---------------------------------------------------------------------------------------------
    @property
    def v_freeze(self):
        """
        get freeze flag
        """
        return self.__v_freeze

# < class CIdle >----------------------------------------------------------------------------------

class CIdle(model.CEventsModel):
    """
    idle event class
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # init super class
        super(CIdle, self).__init__()

        # herdados de CEventsModel
        # self.s_name    # event name

        # event name
        self.s_name = "Idle event"

# < class CQuit >----------------------------------------------------------------------------------

class CQuit(model.CEventsModel):
    """
    program quit event class
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # init super class
        super(CQuit, self).__init__()

        # herdados de CEventsModel
        # self.s_name    # event name

        # event name
        self.s_name = "Program Quit event"

# < class CSave2Disk >-----------------------------------------------------------------------------

class CSave2Disk(model.CEventsModel):
    """
    program save to disk event class
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_table):
        """
        constructor
        """
        # init super class
        super(CSave2Disk, self).__init__()

        # herdados de CEventsModel
        # self.s_name    # event name

        # event name
        self.s_name = "Program Save2Disk event"

        # save table name
        self.__s_table = fs_table

    # ---------------------------------------------------------------------------------------------
    @property
    def s_table(self):
        """
        get table name
        """
        return self.__s_table

# < class CStart >--------------------------------------------------------------------------------

class CStart(model.CEventsModel):
    """
    process start event class
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # init super class
        super(CStart, self).__init__()

        # herdados de CEventsModel
        # self.s_name    # event name

        self.s_name = "Process Start event"

# < class CTick >----------------------------------------------------------------------------------

class CTick(model.CEventsModel):
    """
    CPU tick event class
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # init super class
        super(CTick, self).__init__()

        # herdados de CEventsModel
        # self.s_name    # event name

        # event name
        self.s_name = "CPU Tick event"

# < the end >--------------------------------------------------------------------------------------
