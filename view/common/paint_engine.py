#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
paint_engine

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
__date__ = "2015/12"

# < imports >--------------------------------------------------------------------------------------

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

# libs
# import libs.coords.coord_defs as cdefs
import libs.coords.pos_lat_lng as pll

# model
import model.common.glb_data as gdata
import model.common.tMath as tMath
import model.common.fix as cfix

import model.newton.defs_newton as ldefs

# < class CPaintEngine >---------------------------------------------------------------------------

class CPaintEngine(object):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # init super class
        super(CPaintEngine, self).__init__()

    # ---------------------------------------------------------------------------------------------
    def draw_aerodromo(self, fo_widget, f_aer):
        """
        DOCUMENT ME!
        """
        # check input
        assert fo_widget

        # posição do aeródromo
        l_pos = fo_widget.viewport.translate_pos(pll.CPosLatLng(f_aer.f_aer_lat, f_aer.f_aer_lng))

        # X/Y do aeródromo
        lf_x = l_pos.f_x
        lf_y = l_pos.f_y

        # blip size
        lf_blip_size = fo_widget.viewport.f_blip_size

        # cria um QPainter
        lo_painter = QtGui.QPainter(fo_widget)
        assert lo_painter is not None

        # seleciona a cor do aeródromo
        lo_painter.setPen(gdata.G_DCT_COLORS["aerodromo"])

        # desenha o aeródromo (...um +)
        lo_painter.drawLine(int(lf_x - lf_blip_size / 2.), int(lf_y), int(lf_x + lf_blip_size / 2.), int(lf_y))
        lo_painter.drawLine(int(lf_x), int(lf_y - lf_blip_size / 2.), int(lf_x), int(lf_y + lf_blip_size / 2.))

        # seleciona a cor e fonte do texto
        lo_painter.setPen(gdata.G_DCT_COLORS["name"])
        lo_painter.setFont(QtGui.QFont("Arial", int(lf_blip_size * 1.5)))

        # desenha o texto (indicativo do aeródromo)
        lo_painter.drawText(int(lf_x + lf_blip_size), int(lf_y + lf_blip_size * 2), f_aer.s_aer_indc)

        # para todas as pistas do aeródromo...
        for l_pis in f_aer.dct_aer_pistas.values():
            # posição da cabeceira da pista
            l_cab = fo_widget.viewport.translate_pos(pll.CPosLatLng(l_pis.f_pst_lat, l_pis.f_pst_lng))

            # obtém a posição da cabeceira oposta da pista
            l_cab_opos = fo_widget.viewport.translate_pos(pll.CPosLatLng(l_pis.f_pst_cab_opos_lat, l_pis.f_pst_cab_opos_lng))

            # cria uma caneta 
            l_pen = QtGui.QPen()
            assert l_pen

            # configura cor e estilo da caneta
            l_pen.setColor(gdata.G_DCT_COLORS["pista"])
            l_pen.setStyle(QtCore.Qt.DashDotLine)

            # seleciona a caneta
            lo_painter.setPen(l_pen)

            # desenha a pista ( ...uma + )
            lo_painter.drawLine(int(l_cab.f_x), int(l_cab.f_y), int(l_cab_opos.f_x), int(l_cab_opos.f_y))

        # libera o QPainter
        del lo_painter

    # ---------------------------------------------------------------------------------------------
    def drawApproach(self, fo_widget, f_anv, f_name):
        """
        DOCUMENT ME!
        """
        # check input
        assert fo_widget

        lf_blip_size = fo_widget.viewport.f_blip_size

        rwy = fo_widget.airspace.runway(f_name)
        l_pos = fo_widget.viewport.translate_pos(rwy.pos)

        lf_x = l_pos.f_x
        lf_y = l_pos.f_y

        l_track = tMath.trackOpposite(rwy.getTrack())
        l_track = 10.

        x1 = int(lf_x + fo_widget.viewport.pPNM() * tMath.dsin(l_track) * 10)
        y1 = int(lf_y - fo_widget.viewport.pPNM() * tMath.dcos(l_track) * 10)

        x2 = int(lf_x + fo_widget.viewport.pPNM() * tMath.dsin(l_track + 4) * 11)
        y2 = int(lf_y - fo_widget.viewport.pPNM() * tMath.dcos(l_track + 4) * 11)

        x3 = int(lf_x + fo_widget.viewport.pPNM() * tMath.dsin(l_track - 4) * 11)
        y3 = int(lf_y - fo_widget.viewport.pPNM() * tMath.dcos(l_track - 4) * 11)

        lo_painter = QtGui.QPainter(fo_widget)
        assert lo_painter is not None

        lo_painter.setPen(gdata.G_DCT_COLORS["instruction"])

        lo_painter.drawLine(x, y, x1, y1)
        lo_painter.drawLine(x, y, x2, y2)
        lo_painter.drawLine(x, y, x3, y3)

        lo_painter.drawLine(x1, y1, x2, y2)
        lo_painter.drawLine(x1, y1, x3, y3)

        l_pos = fo_widget.viewport.translate_pos(f_anv.radarPosition())

        str = "APP-%s" % f_name

        lo_painter.setFont(QtGui.QFont("Arial", int(lf_blip_size * 1.5)))
        lo_painter.drawText(int(l_pos.f_x + lf_blip_size), int(l_pos.f_y + lf_blip_size * 2), str)

        del lo_painter

    # ---------------------------------------------------------------------------------------------
    def draw_aproximacao(self, fo_widget, f_apx):
        """
        DOCUMENT ME!
        """
        # check input
        assert fo_widget

        # blip size
        lf_blip_size = fo_widget.viewport.f_blip_size

        # create painter
        lo_painter = QtGui.QPainter(fo_widget)
        assert lo_painter is not None

        # create pen
        l_pen = QtGui.QPen()
        assert l_pen

        # for all breakpoints...
        for l_ndx, l_brk in enumerate(f_apx.lst_apx_brk):
            # get breakpoint id
            ls_id = (ldefs.D_FMT_APX + "-{}").format(f_apx.i_prc_id, l_brk.i_brk_id)

            # breakpoint position
            l_pos = fo_widget.viewport.translate_pos(pll.CPosLatLng(l_brk.f_brk_lat, l_brk.f_brk_lng))

            # not first breakpoint ?
            if 0 != l_ndx:
                # set line colour
                l_pen.setColor(gdata.G_DCT_COLORS["aproximacao"])
                # set line style
                l_pen.setStyle(QtCore.Qt.DashLine)
                # seleciona a caneta
                lo_painter.setPen(l_pen)

                # draw line
                lo_painter.drawLine(tMath.round(l_pos_ant.f_x, 0), tMath.round(l_pos_ant.f_y, 0),
                                    tMath.round(l_pos.f_x, 0), tMath.round(l_pos.f_y, 0))

            # seleciona a cor e fonte do texto
            lo_painter.setPen(gdata.G_DCT_COLORS["name"])
            lo_painter.setFont(QtGui.QFont("Arial", int(lf_blip_size)))

            # desenha o texto (indicativo do breakpoint)
            lo_painter.drawText(int(l_pos.f_x - lf_blip_size * 2), int(l_pos.f_y - lf_blip_size), ls_id)

            # posição anterior
            l_pos_ant = l_pos
            
        # remove o painter
        del lo_painter

    # ---------------------------------------------------------------------------------------------
    def draw_arp(self, fo_widget):
        """
        DOCUMENT ME!
        """
        # check input
        assert fo_widget

        # get ARP position
        l_pos = fo_widget.viewport.translate_pos(fo_widget.viewport.center)

        # get ARP x/y
        lf_x = l_pos.f_x
        lf_y = l_pos.f_y

        # get blip size
        lf_blip_size = fo_widget.viewport.f_blip_size

        # create QPainter
        lo_painter = QtGui.QPainter(fo_widget)
        assert lo_painter is not None

        # set ARP colour
        lo_painter.setPen(gdata.G_DCT_COLORS["arp"])

        # draw ARP (...um +)
        lo_painter.drawLine(int(lf_x - lf_blip_size / 2.), int(lf_y), int(lf_x + lf_blip_size / 2.), int(lf_y))
        lo_painter.drawLine(int(lf_x), int(lf_y - lf_blip_size / 2.), int(lf_x), int(lf_y + lf_blip_size / 2.))

        # set text colour & font
        lo_painter.setPen(gdata.G_DCT_COLORS["arp"])
        lo_painter.setFont(QtGui.QFont("Arial", int(lf_blip_size * 1.5)))

        # draw text (indicativo)
        lo_painter.drawText(int(lf_x + lf_blip_size), int(lf_y + lf_blip_size * 2), "CTR")

        # free QPainter
        del lo_painter

    # ---------------------------------------------------------------------------------------------
    def drawArrival(self, fo_widget, rt):
        """
        DOCUMENT ME!
        """
        # check input
        assert fo_widget

        i = 0
        while i < len(rt._aoItem):

            name = rt._aoItem[i].sName

            lo_painter = QtGui.QPainter(fo_widget)
            assert lo_painter is not None

            lo_painter.setPen(gdata.G_DCT_COLORS["arrival"])

            if (i + 1) < len(rt._aoItem):

                l_pos = fo_widget.viewport.translate_pos(fo_widget._airspace.getPosition(rt._aoItem[i].sName))
                assert l_pos is not None

                lf_x = l_pos.f_x
                lf_y = l_pos.f_y

                l_pos = fo_widget.viewport.translate_pos(fo_widget._airspace.getPosition(rt._aoItem[i + 1].sName))
                assert l_pos is not None

                lo_painter.drawLine(tMath.round(lf_x, 0), tMath.round(lf_y, 0),
                                    tMath.round(l_pos.f_x, 0), tMath.round(l_pos.f_y, 0))

            del lo_painter

            if name[2:].isdigit():
                self.draw_waypoint(fo_widget, rt._aoItem[i].sName, True)

            else:
                self.draw_waypoint(fo_widget, rt._aoItem[i].sName, False)

            i += 1

    # ---------------------------------------------------------------------------------------------
    def draw_background(self, fo_widget, fo_painter):
        """
        DOCUMENT ME!
        """
        # check input
        assert fo_widget
        assert fo_painter

        # fill background
        fo_painter.fillRect(QtCore.QRect(0, 0, fo_widget.width() - 1, fo_widget.height() - 1), gdata.G_DCT_COLORS["radar_background"])

    # ---------------------------------------------------------------------------------------------
    def draw_blip(self, fo_widget, f_anv):
        """
        DOCUMENT ME!
        """
        # check input
        assert fo_widget

        # converte a posição lat/lng da aeronave para x/y
        l_pos = fo_widget.viewport.translate_pos(f_anv.position)
                        
        lf_x = l_pos.f_x
        lf_y = l_pos.f_y

        # tamanho do blip
        lf_blip_size = fo_widget.viewport.f_blip_size

        # cria o painter
        lo_painter = QtGui.QPainter(fo_widget)
        assert lo_painter is not None

        # configura a caneta
        lo_painter.setPen(gdata.G_DCT_COLORS["blip"])

        # paint blip
        lo_painter.drawArc(int(lf_x - lf_blip_size * 0.7),
                           int(lf_y - lf_blip_size * 0.7),
                           int(lf_blip_size * 1.4),
                           int(lf_blip_size * 1.4), 0, 16 * 360)

        # paint lide
        lo_painter.drawLine(int(lf_x + lf_blip_size),
                            int(lf_y - lf_blip_size),
                            int(lf_x + lf_blip_size * 5),
                            int(lf_y - lf_blip_size * 5))

        # configura a fonte
        lo_painter.setFont(QtGui.QFont("Arial", int(lf_blip_size * 1.5)))

        # paint callsign
        l_rect_cs = lo_painter.drawText(int(lf_x + lf_blip_size * 6),
                                        int(lf_y - lf_blip_size * 7),
                                        int(lf_blip_size * 20), 
                                        int(lf_blip_size * 2),
                                        QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop, "{}".format(f_anv.s_callsign))

        # move drawing rect down (next line)
        l_rect_cs.setTop(int(l_rect_cs.y() + lf_blip_size * 2))
        l_rect_cs.setBottom(int(l_rect_cs.bottom() + lf_blip_size * 2))

        # nível
        l_str = "{:d}".format(int(round(f_anv.f_alt / 100., 0)))
        l_rect_niv = lo_painter.drawText(l_rect_cs, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop, l_str)
                        
        # move drawing rect down (next line)
        l_rect_cs.setTop(int(l_rect_cs.y() + lf_blip_size * 2))
        l_rect_cs.setBottom(int(l_rect_cs.bottom() + lf_blip_size * 2))

        # magnetic track
        # l_str = "{:03d}".format(round(f_anv.f_true_heading, 0))
        l_str = "{:03d}".format(int(round(f_anv.f_rumo_mag, 0)))
        l_rect_pro = lo_painter.drawText(l_rect_cs, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop, l_str)
                                
        # groundspeed
        # l_str = "{:d}".format(f_anv.radar_ground_speed())
        l_str = "{:d}".format(int(round(f_anv.f_ias, 0)))
        l_rect_ias = lo_painter.drawText(l_rect_cs, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop, l_str)

        # arrow
        center = l_rect_niv.right() + (l_rect_ias.left() - l_rect_niv.right()) / 2.
        bot = l_rect_niv.bottom() - 4 * lf_blip_size / 5.
        top = l_rect_niv.top() + lf_blip_size / 2.

        # aeronave descendo ?
        if f_anv.isDescending():
            lo_painter.drawLine(int(center + lf_blip_size * .5), top, center, bot)
            lo_painter.drawLine(int(center - lf_blip_size * .5), top, center, bot)

        # senão, aeronave subindo ?
        elif f_anv.isClimbing():
            lo_painter.drawLine(int(center + lf_blip_size * .5), bot, center, top)
            lo_painter.drawLine(int(center - lf_blip_size * .5), bot, center, top)

        # trail
        lo_painter.drawPoint(lf_x, lf_y)

        # para todas as posições do rastro...
        for li_ndx in xrange(8):
            # get trail position
            l_pos = f_anv.trail(li_ndx)

            if l_pos is None:
                break

            # converte a posição do rastro
            l_pos = fo_widget.viewport.translate_pos(l_pos)

            # desenha o rastro
            lo_painter.drawPoint(l_pos.f_x, l_pos.f_y)

        # remove o painter
        del lo_painter

    # ---------------------------------------------------------------------------------------------
    def drawDeparture(self, fo_widget, rt):
        """
        DOCUMENT ME!
        """
        # check input
        assert fo_widget

        i = 0
        pen = QtGui.QPen()
        name = ""

        while i < len(rt._aoItem):
            name = rt._aoItem[i].s_name
            l_log.info("name: " + str(name))

            lo_painter = QtGui.QPainter(fo_widget)
            assert lo_painter is not None

            pen.setColor(gdata.G_DCT_COLORS["departure"])
            pen.setStyle(QtCore.Qt.DashLine)

            lo_painter.setPen(pen)

            if (i + 1) < len(rt._aoItem):

                l_pos = fo_widget.viewport.translate_pos(fo_widget._airspace.getPosition(rt._aoItem[i].s_name))
                lf_x = l_pos.f_x
                lf_y = l_pos.f_y
                l_pos = fo_widget.viewport.translate_pos(fo_widget._airspace.getPosition(rt._aoItem[i + 1].s_name))

                lo_painter.drawLine(tMath.round(lf_x, 0), tMath.round(lf_y, 0),
                                    tMath.round(l_pos.f_x, 0), tMath.round(l_pos.f_y, 0))

            del lo_painter

            if name[2: len(name) - 1].isdigit():
                self.draw_waypoint(fo_widget, rt._aoItem[i].s_name, True)

            else:
                self.draw_waypoint(fo_widget, rt._aoItem[i].s_name, False)

            i += 1

    # ---------------------------------------------------------------------------------------------
    def drawDirect(self, fo_widget, f_anv, f_name):
        """
        DOCUMENT ME!
        """
        # check input
        assert fo_widget

        l_pos = fo_widget.viewport.translate_pos(f_anv.radarPosition())

        lf_x = l_pos.f_x
        lf_y = l_pos.f_y

        lf_blip_size = fo_widget.viewport.f_blip_size

        l_pos = fo_widget.viewport.translate_pos(fo_widget._airspace.getPosition(f_name))

        lo_painter = QtGui.QPainter(fo_widget)
        assert lo_painter is not None

        lo_painter.setPen(gdata.G_DCT_COLORS["instruction"])
        lo_painter.drawLine(l_pos.f_x, l_pos.f_y, lf_x, lf_y)

        lo_painter.setFont(QtGui.QFont("Arial", int(lf_blip_size * 1.5)))
        lo_painter.drawText(int(l_pos.f_x + lf_blip_size), int(l_pos.f_y + lf_blip_size * 2), f_name)

        del lo_painter

    # ---------------------------------------------------------------------------------------------
    def draw_navaid(self, fo_widget, f_fix, f_kind=None):
        """
        DOCUMENT ME!
        """
        # check input
        assert fo_widget

        # get beacon position
        l_pos = fo_widget.viewport.translate_pos(pll.CPosLatLng(f_fix.f_fix_lat, f_fix.f_fix_lng))

        # get X/Y
        lf_x = l_pos.f_x
        lf_y = l_pos.f_y

        # get blip size
        lf_blip_size = fo_widget.viewport.f_blip_size

        # create QPainter
        lo_painter = QtGui.QPainter(fo_widget)
        assert lo_painter is not None

        # DME ?
        if ldefs.E_DME == f_fix.en_fix_tipo:
            # set DME colour
            lo_painter.setPen(gdata.G_DCT_COLORS["dme"])

            # draw beacon (...um o)
            lo_painter.drawEllipse(int(lf_x), int(lf_y), int(lf_blip_size), int(lf_blip_size))

        # NDB ?
        elif ldefs.E_NDB == f_fix.en_fix_tipo:    
            # set NDB colour
            lo_painter.setPen(gdata.G_DCT_COLORS["ndb"])

            # draw beacon (...um o)
            lo_painter.drawEllipse(int(lf_x), int(lf_y), int(lf_blip_size), int(lf_blip_size))

        # VOR ?
        elif ldefs.E_VOR == f_fix.en_fix_tipo:    
            # set VOR colour
            lo_painter.setPen(gdata.G_DCT_COLORS["vor"])

            # draw beacon (...um o)
            lo_painter.drawRect(int(lf_x - lf_blip_size / 2.), int(lf_y - lf_blip_size / 2.), 
                                int(lf_blip_size), int(lf_blip_size))

        # senão,...
        else:
            # set waypoint colour
            lo_painter.setPen(gdata.G_DCT_COLORS["navaid"])

            # draw beacon (...um +)
            lo_painter.drawLine(int(lf_x - lf_blip_size / 2.), int(lf_y), int(lf_x + lf_blip_size / 2.), int(lf_y))
            lo_painter.drawLine(int(lf_x), int(lf_y - lf_blip_size / 2.), int(lf_x), int(lf_y + lf_blip_size / 2.))

        # waypoint ?
        if f_kind is None:
            # set text colour & font
            lo_painter.setPen(gdata.G_DCT_COLORS["name"])
            lo_painter.setFont(QtGui.QFont("Arial", int(lf_blip_size * 1.5)))

            # draw waypoint name (indicativo do fixo)
            lo_painter.drawText(int(lf_x + lf_blip_size), int(lf_y + lf_blip_size * 2), f_fix.s_fix_indc)

        # free QPainter
        del lo_painter

    # ---------------------------------------------------------------------------------------------
    def drawRoute(self, fo_widget, f_anv, f_name):
        """
        DOCUMENT ME!
        """
        # check input
        assert fo_widget

        lf_blip_size = fo_widget.viewport.f_blip_size

        srt = fo_widget._airspace.route(f_name)

        lo_painter = QtGui.QPainter(fo_widget)
        assert lo_painter is not None

        lo_painter.setPen(gdata.G_DCT_COLORS["instruction"])

        i = 0
        while (i + 1) < len(srt._aoItem):
            l_pos = fo_widget.viewport.translate_pos(fo_widget._airspace.getPosition(srt._aoItem[i].s_name))

            lf_x = l_pos.f_x
            lf_y = l_pos.f_y

            l_pos = fo_widget.viewport.translate_pos(fo_widget._airspace.getPosition(srt._aoItem[i + 1].s_name))

            lo_painter.drawLine(l_pos.f_x, l_pos.f_y, x, lf_y)

            i += 1

        l_pos = fo_widget.viewport.translate_pos(f_anv.radarPosition())

        lo_painter.setFont(QtGui.QFont("Arial", int(lf_blip_size * 1.5)))
        lo_painter.drawText(int(l_pos.f_x + lf_blip_size), int(l_pos.f_y + lf_blip_size * 2), f_name)

        del lo_painter

    # ---------------------------------------------------------------------------------------------
    def drawRunway(self, fo_widget, f_rwy):
        """
        DOCUMENT ME!
        """
        # check input
        assert fo_widget

        # obtém a posição da runway
        l_pos = fo_widget.viewport.translate_pos(f_rwy.pos)

        # componentes X e Y
        lf_x = l_pos.f_x
        lf_y = l_pos.f_y

        # obtém a direção da runway
        l_track = tMath.trackOpposite(f_rwy.fTrack)

        x_mile = fo_widget.viewport.pPNM() * tMath.dsin(l_track)
        y_mile = -fo_widget.viewport.pPNM() * tMath.dcos(l_track)

        # cria um painter
        lo_painter = QtGui.QPainter(fo_widget)
        assert lo_painter is not None

        # seleciona a caneta
        lo_painter.setPen(gdata.G_DCT_COLORS["runway"])

        for li_ndx in xrange(1, 25, 2):
            lo_painter.drawLine(int(lf_x + li_ndx * x_mile), int(lf_y + li_ndx * y_mile),
                                int(lf_x + (li_ndx + 1) * x_mile), int(lf_y + (li_ndx + 1) * y_mile))

        lo_painter.drawLine(int(lf_x + 10 * x_mile - y_mile / 2.), int(lf_y + 10 * y_mile + x_mile / 2.),
                            int(lf_x + 10 * x_mile + y_mile / 2.), int(lf_y + 10 * y_mile - x_mile / 2.))
        lo_painter.drawLine(int(lf_x + 25 * x_mile - y_mile / 2.), int(lf_y + 25 * y_mile + x_mile / 2.),
                            int(lf_x + 25 * x_mile + y_mile / 2.), int(lf_y + 25 * y_mile - x_mile / 2.))

        # libera o painter
        del lo_painter

    # ---------------------------------------------------------------------------------------------
    def draw_subida(self, fo_widget, f_sub):
        """
        DOCUMENT ME!
        """
        # check input
        assert fo_widget

        # get blip size
        lf_blip_size = fo_widget.viewport.f_blip_size

        # create painter
        lo_painter = QtGui.QPainter(fo_widget)
        assert lo_painter is not None

        # create pen
        l_pen = QtGui.QPen()
        assert l_pen

        # for all breakpoints...
        for l_ndx, l_brk in enumerate(f_sub.lst_sub_brk):
            # get breakpoint id
            ls_id = (ldefs.D_FMT_SUB + "-{}").format(f_sub.i_prc_id, l_brk.i_brk_id)

            # breakpoint position
            l_pos = fo_widget.viewport.translate_pos(pll.CPosLatLng(l_brk.f_brk_lat, l_brk.f_brk_lng))

            # not first breakpoint ?
            if 0 != l_ndx:
                # set line colour
                l_pen.setColor(gdata.G_DCT_COLORS["subida"])
                # set line style
                l_pen.setStyle(QtCore.Qt.DashLine)
                # seleciona a caneta
                lo_painter.setPen(l_pen)

                # draw line
                lo_painter.drawLine(tMath.round(l_pos_ant.f_x, 0), tMath.round(l_pos_ant.f_y, 0),
                                    tMath.round(l_pos.f_x, 0), tMath.round(l_pos.f_y, 0))

            # seleciona a cor e fonte do texto
            lo_painter.setPen(gdata.G_DCT_COLORS["name"])
            lo_painter.setFont(QtGui.QFont("Arial", int(lf_blip_size)))

            # desenha o texto (indicativo do breakpoint)
            lo_painter.drawText(int(l_pos.f_x - lf_blip_size * 2), int(l_pos.f_y - lf_blip_size), ls_id)

            # salva a posição anterior
            l_pos_ant = l_pos
            
        # remove o painter
        del lo_painter

    # ---------------------------------------------------------------------------------------------
    def draw_trajetoria(self, fo_widget, f_trj):
        """
        DOCUMENT ME!
        """
        # check input
        assert fo_widget
        assert f_trj

        # get blip size
        lf_blip_size = fo_widget.viewport.f_blip_size

        # create painter
        lo_painter = QtGui.QPainter(fo_widget)
        assert lo_painter is not None

        # create pen
        l_pen = QtGui.QPen()
        assert l_pen

        # for all breakpoints...
        for l_ndx, l_brk in enumerate(f_trj.lst_trj_brk):
            # get breakpoint id
            ls_id = (ldefs.D_FMT_TRJ + "-{}").format(f_trj.i_prc_id, l_brk.i_brk_id)

            # breakpoint position
            l_pos = fo_widget.viewport.translate_pos(pll.CPosLatLng(l_brk.f_brk_lat, l_brk.f_brk_lng))

            # not first breakpoint ?
            if 0 != l_ndx:
                # set line colour
                l_pen.setColor(gdata.G_DCT_COLORS["trajectory"])
                # set line style
                l_pen.setStyle(QtCore.Qt.DashDotLine)
                # seleciona a caneta
                lo_painter.setPen(l_pen)

                # draw line
                lo_painter.drawLine(tMath.round(l_pos_ant.f_x, 0), tMath.round(l_pos_ant.f_y, 0),
                                    tMath.round(l_pos.f_x, 0), tMath.round(l_pos.f_y, 0))

            # select colour & font
            lo_painter.setPen(gdata.G_DCT_COLORS["trajectory_name"])
            lo_painter.setFont(QtGui.QFont("Arial", int(lf_blip_size)))

            # draw text (indicativo do breakpoint)
            lo_painter.drawText(int(l_pos.f_x - lf_blip_size * 2), int(l_pos.f_y - lf_blip_size), ls_id)

            # save last position
            l_pos_ant = l_pos
            
        # free painter
        del lo_painter

    # ---------------------------------------------------------------------------------------------
    def drawTransition(self, fo_widget, rt):
        """
        DOCUMENT ME!
        """
        # check input
        assert fo_widget

        i = 0
        while (i < len(rt._aoItem)):

            lo_painter = QtGui.QPainter(fo_widget)
            assert lo_painter is not None

            lo_painter.setPen(gdata.G_DCT_COLORS["transition"])

            if (i + 1) < len(rt._aoItem):
                l_pos = fo_widget.viewport.translate_pos(fo_widget._airspace.getPosition(rt._aoItem[i].s_name))

                lf_x = l_pos.f_x
                lf_y = l_pos.f_y

                l_pos = fo_widget.viewport.translate_pos(fo_widget._airspace.getPosition(rt._aoItem[i + 1].s_name))
                lo_painter.drawLine(tMath.round(lf_x, 0), tMath.round(
                    lf_y, 0), tMath.round(l_pos.f_x, 0), tMath.round(l_pos.f_y, 0))

            del lo_painter

            self.draw_waypoint(fo_widget, rt._aoItem[i].s_name, True)

            i += 1

    # ---------------------------------------------------------------------------------------------
    def drawVector(self, fo_widget, f_anv, rv):
        """
        DOCUMENT ME!
        """
        # check input
        assert fo_widget

        l_pos = fo_widget.viewport.translate_pos(f_anv.radarPosition())

        lf_blip_size = fo_widget.viewport.f_blip_size

        str = "%03d" % rv
        rvec = rv - fo_widget._airspace.variation()

        lo_painter = QtGui.QPainter(fo_widget)
        assert lo_painter is not None

        lo_painter.setFont(QtGui.QFont("Arial", int(lf_blip_size * 1.5)))
        lo_painter.setPen(gdata.G_DCT_COLORS["instruction"])

        lo_painter.drawLine(int(l_pos.f_x),
                           int(l_pos.f_y),
                           int(l_pos.f_x + 2000 * tMath.dsin(rvec)),
                           int(l_pos.f_y - 2000 * tMath.dcos(rvec)))

        lo_painter.setFont(QtGui.QFont("Arial", int(lf_blip_size * 1.5)))

        if (rvec < 90) or ((rvec > 180) and (rvec < 270)):
            lo_painter.drawText(int(lf_blip_size + l_pos.f_x + lf_blip_size * 25 * tMath.dsin(rvec)),
                               int(lf_blip_size * 3 + l_pos.f_y - lf_blip_size * 25 * tMath.dcos(rvec)), str)
        else:
            lo_painter.drawText(int(lf_blip_size + l_pos.f_x + lf_blip_size * 25 * tMath.dsin(rvec)),
                               int(-lf_blip_size + l_pos.f_y - lf_blip_size * 25 * tMath.dcos(rvec)), str)

        del lo_painter

    # ---------------------------------------------------------------------------------------------
    def draw_waypoint(self, fo_widget, f_obj, fv_nameless):
        """
        DOCUMENT ME!
        """
        if isinstance(f_obj, str):
            self.__draw_waypoint_name(fo_widget, f_obj, fv_nameless)

        elif isinstance(f_obj, cfix.CFix):
            self.__draw_waypoint_fix(fo_widget, f_obj, fv_nameless)

    # ---------------------------------------------------------------------------------------------
    def __draw_waypoint_name(self, fo_widget, f_name, fv_nameless):
        """
        DOCUMENT ME!
        """
        pos = fo_widget._airspace.getPosition(f_name)

        l_fix = cfix.CFix(f_name, pos._fLat, pos._fLng)
        assert l_fix

        self.__draw_waypoint_fix(fo_widget, l_fix, fv_nameless)

        del l_fix

    # ---------------------------------------------------------------------------------------------
    def __draw_waypoint_fix(self, fo_widget, f_fix, fv_nameless):
        """
        DOCUMENT ME!
        """
        # check input
        assert fo_widget

        l_pos = fo_widget.viewport.translate_pos(f_fix.pos)

        lf_x = l_pos.f_x
        lf_y = l_pos.f_y

        lf_blip_size = fo_widget.viewport.f_blip_size

        lo_painter = QtGui.QPainter(fo_widget)
        assert lo_painter is not None

        lo_painter.setPen(gdata.G_DCT_COLORS["waypoint"])
        lo_painter.drawLine(int(lf_x - lf_blip_size / 2.), int(lf_y), int(lf_x + lf_blip_size / 2.), int(lf_y))
        lo_painter.drawLine(int(lf_x), int(lf_y - lf_blip_size / 2.), int(lf_x), int(lf_y + lf_blip_size / 2.))

        if not fv_nameless:
            lo_painter.setPen(gdata.G_DCT_COLORS["name"])
            lo_painter.setFont(QtGui.QFont("Arial", int(lf_blip_size * 1.5)))
            lo_painter.drawText(int(lf_x + lf_blip_size), int(lf_y + lf_blip_size * 2.), f_fix.s_name)

        del lo_painter

    # ---------------------------------------------------------------------------------------------
    def invert(self, f_clr):
        """
        DOCUMENT ME!
        """
        # check input
        assert f_clr

        f_clr.setRed(255 - f_clr.red())
        f_clr.setGreen(255 - f_clr.green())
        f_clr.setBlue(255 - f_clr.blue())

    # ---------------------------------------------------------------------------------------------
    def setColors(self, fv_inverted):
        """
        DOCUMENT ME!
        """
        if fv_inverted:
            self.invert(gdata.G_DCT_COLORS["aerodromo"])
            self.invert(gdata.G_DCT_COLORS["arp"])
            self.invert(gdata.G_DCT_COLORS["arrival"])
            self.invert(gdata.G_DCT_COLORS["radar_background"])
            self.invert(gdata.G_DCT_COLORS["blip"])
            self.invert(gdata.G_DCT_COLORS["departure"])
            self.invert(gdata.G_DCT_COLORS["dme"])
            self.invert(gdata.G_DCT_COLORS["instruction"])
            self.invert(gdata.G_DCT_COLORS["name"])
            self.invert(gdata.G_DCT_COLORS["ndb"])
            self.invert(gdata.G_DCT_COLORS["pista"])
            self.invert(gdata.G_DCT_COLORS["runway"])
            self.invert(gdata.G_DCT_COLORS["subida"])
            self.invert(gdata.G_DCT_COLORS["trajectory"])
            self.invert(gdata.G_DCT_COLORS["transition"])
            self.invert(gdata.G_DCT_COLORS["vor"])

            gdata.G_DCT_COLORS["navaid"] = QtGui.QColor(200, 0, 0, 255)

# < the end >--------------------------------------------------------------------------------------
