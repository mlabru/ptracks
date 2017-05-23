#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
view_handler

newton's HTTP server handler

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
import urllib2

import SimpleHTTPServer

# view
import view.visweb.generate_anv_json as anvjson
import view.visweb.generate_prf_json as prfjson
import view.visweb.generate_status_json as sttjson

# control
import control.control_debug as cdbg

# < defines >--------------------------------------------------------------------------------------

D_MODES_CONTENT_TYPE_CSS  = "text/css;charset=utf-8"
D_MODES_CONTENT_TYPE_GIF  = "image/gif"
D_MODES_CONTENT_TYPE_HTML = "text/html;charset=utf-8"
D_MODES_CONTENT_TYPE_JPG  = "image/jpg"
D_MODES_CONTENT_TYPE_JS   = "application/javascript;charset=utf-8"
D_MODES_CONTENT_TYPE_JSON = "application/json;charset=utf-8"

# < class CViewHandler >---------------------------------------------------------------------------

class CViewHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """
    handles any incoming request from the browser
    """
    # ---------------------------------------------------------------------------------------------
    def do_GET(self):
        """
        handler for the GET requests
        """
        # default path ?
        if "/" == self.path:
            self.path = "/index.html"

        # ditch any trailing query part (AJAX might add one to avoid caching)
        llst_path = self.path.split('?')
        self.path = llst_path[0]

        # check the file extension required and set the right mime type
        try:
            lv_send_reply = False

            # comando de pilotagem ?
            if "/cmd" == self.path: 
                # trata o comando de pilotagem
                ls_cmd = str(urllib2.unquote(llst_path[1])).strip().upper()

                self.server.emula.parse_msg_pil(ls_cmd)
                cdbg.M_DBG.debug("command: [{}/{}]".format(ls_cmd, ls_cmd[:7]))

                # create and send headers
                self.send_response(200)
                self.send_header("Content-type", D_MODES_CONTENT_TYPE_JSON)
                self.end_headers()

                # create and send json file
                self.wfile.write(sttjson.generate_status_json(self.server.dct_flight, ls_cmd[:7]))

            # json file ?
            elif self.path.endswith(".json"):
                # aircraft ?
                if "/data/aircraft.json" == self.path:
                    self.send_response(200)
                    self.send_header("Content-type", D_MODES_CONTENT_TYPE_JSON)
                    self.end_headers()

                    # monta e envia mensagem de aeronave
                    self.wfile.write(anvjson.generate_anv_json(self.server.dct_flight, self.server.coords))

                # performance ?
                elif "/data/prf.json" == self.path:
                    # create and send headers
                    self.send_response(200)
                    self.send_header("Content-type", D_MODES_CONTENT_TYPE_JSON)
                    self.end_headers()

                    # create and send json file
                    self.wfile.write(prfjson.generate_prf_json(self.server.dct_prf, llst_path[1]))

                # status ?
                elif "/data/status.json" == self.path:
                    # create and send headers
                    self.send_response(200)
                    self.send_header("Content-type", D_MODES_CONTENT_TYPE_JSON)
                    self.end_headers()

                    # create and send json file
                    self.wfile.write(sttjson.generate_status_json(self.server.dct_flight, llst_path[1]))

            # html file ?
            elif self.path.endswith(".html"):
                # set file type
                mimetype = D_MODES_CONTENT_TYPE_HTML
                lv_send_reply = True

            # css file ?
            elif self.path.endswith(".css"):
                # set file type
                mimetype = D_MODES_CONTENT_TYPE_CSS
                lv_send_reply = True

            # gif file ?
            elif self.path.endswith(".gif"):
                # set file type
                mimetype = D_MODES_CONTENT_TYPE_GIF
                lv_send_reply = True

            # jpeg file ?
            elif self.path.endswith(".jpg"):
                # set file type
                mimetype = D_MODES_CONTENT_TYPE_JPG
                lv_send_reply = True

            # javascript file ?
            elif self.path.endswith(".js"):
                # set file type
                mimetype = D_MODES_CONTENT_TYPE_JS
                lv_send_reply = True

            if lv_send_reply:
                # open the static file requested and send it
                f = open(os.curdir + os.sep + "public_html" + self.path)

                # create and send headers
                self.send_response(200)
                self.send_header("Content-type", mimetype)
                self.end_headers()

                # create and send contents
                self.wfile.write(f.read())

                # close file
                f.close()

        # em caso de erro...
        except IOError:
            # send error
            self.send_error(404, "File Not Found:[{}]".format(self.path))

    # ---------------------------------------------------------------------------------------------
    def log_error(self, format, *args): pass

    # ---------------------------------------------------------------------------------------------
    def log_message(self, format, *args): pass

    # ---------------------------------------------------------------------------------------------
    def log_request(self, code='-', size='-'): pass

# < the end >--------------------------------------------------------------------------------------
