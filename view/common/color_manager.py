#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
color_manager

system colour manager

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

revision 0.1  2015/fev  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2016/09"

# < imports >--------------------------------------------------------------------------------------

# python library
import ast
import logging
import os
import sys

# control
import control.events.events_basic as evtbas

# < module data >----------------------------------------------------------------------------------

# brightness category
M_MasterCategory = -1

# colors
M_DefWindowBackClr = 0
M_DefWindowTextClr = 1
M_DefWindowLeftTopClr = 2
M_DefWindowRightBottomClr = 3
M_DefWindowTitleClr = 4
M_DefMenuBackClr = 5
M_DefMenuTextClr = 6
M_DefMenuLeftTopClr = 7
M_DefMenuRightBottomClr = 8
M_DefMenuHighBackClr = 9
M_DefMenuHighTextClr = 10
M_DefMenuDisTextClr = 11
M_LastFixedClr = 11

# int
M_PercentColor = 8

# < class CColorData >-----------------------------------------------------------------------------

class CColorData(object):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # (str) 
        self.s_descricao = ""
        # (tuple) 
        self.t_color = None
        # (int) 
        self.i_group_no = M_MasterCategory

# class < CColorManager >--------------------------------------------------------------------------

class CColorManager(object):
    """
    manages the colors
    """
    # fixed color ids
    c_color_id = wnd_default_bkgrnd, wnd_default_frgrnd, wnd_default_highlight, \
                 wnd_default_shadow, color_title, menu_default_bkgrnd, menu_default_frgrnd, \
                 menu_default_highlight, menu_default_shadow, sel_menu_default_bkgrnd, \
                 sel_menu_default_frgrnd, grayed_out = xrange(12)

    # color number dictionary
    c_dct_color_no = {wnd_default_bkgrnd: "wnd_default_bkgrnd",
                      wnd_default_frgrnd: "wnd_default_frgrnd",
                      wnd_default_highlight: "wnd_default_highlight",
                      wnd_default_shadow: "wnd_default_shadow",
                      color_title: "color_title",
                      menu_default_bkgrnd: "menu_default_bkgrnd",
                      menu_default_frgrnd: "menu_default_frgrnd",
                      menu_default_highlight: "menu_default_highlight",
                      menu_default_shadow: "menu_default_shadow",
                      sel_menu_default_bkgrnd: "sel_menu_default_bkgrnd",
                      sel_menu_default_frgrnd: "sel_menu_default_frgrnd",
                      grayed_out: "grayed_out"}

    # colors dictionary
    c_dct_color = {"wnd_default_bkgrnd": (None, (255, 255, 255), -1),
                   "wnd_default_frgrnd": (None, (0, 0, 0), -1),
                   "wnd_default_highlight": (None, (255, 255, 255), -1),
                   "wnd_default_shadow": (None, (128, 128, 128), -1),
                   "color_title": (None, (10, 36, 106), -1),
                   "menu_default_bkgrnd": (None, (212, 208, 200), -1),
                   "menu_default_frgrnd": (None, (0, 0, 0), -1),
                   "menu_default_highlight": (None, (255, 255, 255), -1),
                   "menu_default_shadow": (None, (128, 128, 128), -1),
                   "sel_menu_default_bkgrnd": (None, (10, 36, 106), -1),
                   "sel_menu_default_frgrnd": (None, (255, 255, 255), -1),
                   "grayed_out": (None, (128, 128, 128), -1)}
                                                                   
    # brightness category
    c_category = AOCSymbCategory, AOCDbCategory, NonAOCSymbCategory, NonAOCDbCategory, \
                 MouseCategory, WeatherCategory, OtherMapCategory, LineCategory, \
                 NavCategory, RangeMarkersCategory, AsdToolsCategory, WindowsCategory, \
                 DFFinderCategory = xrange(13)

    # brightness category
    c_lst_category = [AOCSymbCategory, AOCDbCategory, NonAOCSymbCategory, NonAOCDbCategory,
                      MouseCategory, WeatherCategory, OtherMapCategory, LineCategory,
                      NavCategory, RangeMarkersCategory, AsdToolsCategory, WindowsCategory,
                      DFFinderCategory]

    # ---------------------------------------------------------------------------------------------
    def __init__(self, fo_config=None, fs_path=None):
        """
        @param fs_path: color table file path (basestring)
        """
        # init super class
        super(CColorManager, self).__init__()

        # (int)
        self.__lst_category = [100 for _ in xrange(len(self.c_lst_category))]

        # (int)
        self.__i_master_category = 100

        # via config ?
        if fo_config is not None:
            # get default tables dir & expand user (~)
            ls_dir = os.path.expanduser(fo_config.dct_config["dir.tab"])

            # dir not found ?
            if not os.path.exists(ls_dir):
                # logger
                l_log = logging.getLogger("CColorManager::__init__")
                l_log.setLevel(logging.CRITICAL)
                l_log.critical("<E01: error loading color table: directory [{}] not found.".format(ls_dir))

                # abort
                sys.exit()
                                                    
            # create color manager
            fs_path = os.path.join(ls_dir, fo_config.dct_config["tab.clr"])

        # load color table
        self.__load_ctable(fs_path)

    # ---------------------------------------------------------------------------------------------
    def extract_attributes(self, fs_data):
        """
        extract the attributes contained in line

        @param fs_data: attribute line

        @return extrated attributes
        """
        # check input
        if not fs_data or (len(fs_data) < 1):
            # get out...
            return

        # split line on |
        llst_attr = fs_data.split('|')

        # get brightness category
        li_cat = int(llst_attr[0].strip())

        # get color
        lt_cor = ast.literal_eval("({})".format(llst_attr[1].strip()))

        if -2 == li_cat:
            lt_cor = (int(lt_cor[0] * 255), int(lt_cor[1] * 255), int(lt_cor[2] * 255))

        # get remarks
        ls_rem = llst_attr[2].strip().lower()

        # return
        return (ls_rem, lt_cor, li_cat)

    # ---------------------------------------------------------------------------------------------
    def get_brightness(self, fi_category):
        """
        gets the brightness according to the category argument
        
        @param fi_category: the category
    
        @return the brightness value of the category
        """
        if M_MasterCategory == fi_category:
            # return
            return self.__i_master_category

        # return
        return self.__lst_category[fi_category]

    # ---------------------------------------------------------------------------------------------
    def get_color(self, fs_name):
        """
        returns the color according to the color name from the color table

        @param fs_name: the color name

        @return the color if the function is successful, otherwise (255, 255, 255)
        """
        # get color
        lt_cor = self.c_dct_color.get(fs_name.lower(), None)

        if lt_cor is None:
            # return
            return (255, 255, 255)

        # return
        return self.transform_color(self.c_dct_color[fs_name][1], self.c_dct_color[fs_name][2])

    # ---------------------------------------------------------------------------------------------
    def get_color_by_no(self, fi_color_no):
        """
        returns the color according to the color position

        @param fi_color_no: the color position

        @return color tuple according to the color position if the function is successful,
                otherwise default white color (255,255,255)
        """
        ls_name = self.c_dct_color_no.get(fi_color_no, None)

        if ls_name is None:
            # return
            return (255, 255, 255)

        # return
        return self.get_color(ls_name)

    # ---------------------------------------------------------------------------------------------
    def __load_ctable(self, fs_path):
        """
        faz a carga do airspace

        @return flag e mensagem
        """
        # open color table file
        lfd_tab = open(fs_path, 'r')
        assert lfd_tab

        # for all lines in file...
        for ls_line in lfd_tab.readlines():
            # have content ?
            if len(ls_line) > 0:
                # comment or empty line ? 
                if (ls_line.startswith('#') or ls_line.startswith(';') or 
                    ls_line.startswith("--") or ls_line.startswith('\n')):
                    # next line
                    continue

                # trata itens de uma linha do color table
                # self.trata_linha(re.findall(r"<(.*?)>", ls_line))

                # first element must be a color name
                ls_key, ls_val = ls_line.split('=')

                # strip and lower key
                ls_key = ls_key.strip().lower()

                # get color from dictionary
                l_cor = self.c_dct_color.get(ls_key, None)                

                if l_cor is None:
                    # put a new color in dictionary
                    self.c_dct_color_no[len(self.c_dct_color)] = ls_key

                # update dictionary
                self.c_dct_color[ls_key] = self.extract_attributes(ls_val)                 

        # close file
        lfd_tab.close()

        # retorna ok
        return True, None

    # ---------------------------------------------------------------------------------------------
    def set_brightness(self, fi_category, fi_value):
        """
        sets the brightness according to the category argument

        @param fi_category: the category
        @param fi_value: the brightness value
        """
        # master category ?
        if M_MasterCategory == fi_category:
            # save master category brightness
            self.__i_master_category = fi_value

        # otherwise,...
        else:
            # save category brightness
            self.__lst_category[fi_category] = fi_value

            # windows category ?
            if M_WindowsCategory == fi_category:
                pass  # setColors()

            # mouse category ?
            if M_MouseCategory == fi_category:
                pass  # setCursorColors()

    # ---------------------------------------------------------------------------------------------
    def transform_color(self, ft_color, fi_category):
        """
        computes the color argument according to the brightness category argument

        @param ft_color: the color
        @param fi_category: the category
    
        @return color tuple
        """
        # check input
        assert ft_color
                        
        # get colors
        li_red = ft_color[0]
        li_green = ft_color[1]
        li_blue = ft_color[2]

        # master category ? 
        if M_MasterCategory == fi_category:
            li_offset = 100

        # otherwise,...
        else:
            li_offset = self.__lst_category[fi_category]

        # calculate new colors
        li_red = int((li_red * li_offset) / 100.)
        li_green = int((li_green * li_offset) / 100.)
        li_blue = int((li_blue * li_offset) / 100.)

        # normalize
        
        if li_red < 0:
            li_red = 0
    
        elif li_red > 255:
            li_red = 255

        if li_green < 0:
            li_green = 0 

        elif li_green > 255:
            li_green = 255

        if li_blue < 0:
            li_blue = 0

        elif li_blue > 255:
            li_blue = 255

        # return
        return (li_red, li_green, li_blue)

    # ---------------------------------------------------------------------------------------------
    def transform_color_no(self, fi_color_no, fi_category):
        """
        computes the color according to the color position and the brightness category arguments

        @param color: the color
        @param fi_category: the category
    
        @return color tuple
        """
        ls_name = self.c_dct_color_no.get(fi_color_no, None)

        if ls_name is None:
            # return
            return (255, 255, 255)

        return self.transform_color(self.c_dct_color[ls_name][1], fi_category)

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def lst_category(self):
        """
        get category list
        """
        return self.__lst_category

    @lst_category.setter
    def lst_category(self, f_val):
        """
        set category list
        """
        self.__lst_category = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def i_master_category(self):
        """
        get master category
        """
        return self.__i_master_category

    @i_master_category.setter
    def i_master_category(self, f_val):
        """
        set master category
        """
        self.__i_master_category = f_val

# -------------------------------------------------------------------------------------------------
# bootstrap process

if "__main__" == __name__:
    # logger
    logging.basicConfig()
        
    cm = CColorManager(None, "../data/colors.dat")

    print cm.get_color("sel_menu_default_bkgrnd")
    print cm.get_color_by_no(5)
                    
# < the end >--------------------------------------------------------------------------------------
