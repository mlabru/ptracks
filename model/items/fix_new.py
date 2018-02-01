#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------------------------
fix_new

mantém as informações sobre um fixo

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
-------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import sys

# libs
import libs.coords.coord_defs as cdefs

# model
import model.items.fix_model as model
import model.newton.defs_newton as ldefs

# control
import control.events.events_basic as events

# < class CFixNEW >--------------------------------------------------------------------------------

class CFixNEW(model.CFixModel):
    """
    mantém as informações específicas sobre fixo
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_model, f_data=None, fs_ver="0001"):
        """
        @param f_model: event manager
        @param f_data: dados do fixo
        @param fs_ver: versão do formato dos dados
        """
        # check input
        assert f_model

        # init super class
        super(CFixNEW, self).__init__()

        # salva o model manager localmente
        self.__model = f_model

        # salva o event manager localmente
        self.__event = f_model.event

        # herdados de CFixModel
        # self.v_fix_ok       # ok (bool)
        # self.i_fix_id       # identificação do fixo
        # self.s_fix_indc     # indicativo do fixo
        # self.s_fix_desc     # descrição do fixo
        # self.en_fix_tipo    # tipo de fixo (enum)
        # self.f_fix_x        # X
        # self.f_fix_y        # Y
        # self.f_fix_z        # Z

        # latitude
        self.__f_fix_lat = 0.
        # longitude
        self.__f_fix_lng = 0.
        # elevação
        self.__f_fix_elev = 0.

        # freqüência
        self.__f_fix_freq = 0.

        # recebeu dados ?
        if f_data is not None:
            # recebeu uma lista ?
            if isinstance(f_data, dict):
                # cria um fixo com os dados da lista
                self.load_fix(f_data, fs_ver)

            # recebeu um fixo ?
            elif isinstance(f_data, CFixNEW):
                # copia o fixo
                self.copy_fix(f_data)

    # ---------------------------------------------------------------------------------------------
    def copy_fix(self, f_fix):
        """
        copy constructor. Copia para este fixo os dados de um outro fixo

        @param f_fix: fixo a ser copiado
        """
        # check input
        assert f_fix

        # copy super class attributes
        super(CFixNEW, self).copy_fix(f_fix)

        # longitude
        self.__f_fix_lng = f_fix.f_fix_lng
        # latitude
        self.__f_fix_lat = f_fix.f_fix_lat
        # elevação
        self.__f_fix_elev = f_fix.f_fix_elev

        # freqüência
        self.__f_fix_freq = f_fix.f_fix_freq

    # ---------------------------------------------------------------------------------------------
    def load_fix(self, fdct_data, fs_ver="0001"):
        """
        carrega os dados do fixo a partir de um dicionário (formato 0001)

        @param fdct_data: dicionário com os dados do fixo
        @param fs_ver: versão do formato
        """
        # formato versão 0.01 ?
        if "0001" == fs_ver:
            # cria a fixo
            self.make_fix(fdct_data)

        # senão, formato desconhecido
        else:
            # logger
            l_log = logging.getLogger("CFixNEW::load_fix")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: formato {} desconhecido.".format(fs_ver))

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # cai fora...
            sys.exit(1)

    # ---------------------------------------------------------------------------------------------
    def make_fix(self, fdct_data):
        """
        carrega os dados de fixo a partir de um dicionário (formato 0001)

        @param fdct_data: dicionário com os dados do fixo
        """
        # identificação do fixo
        if "nFix" in fdct_data:
            self.s_fix_indc = fdct_data["nFix"]

        # descrição
        if "descricao" in fdct_data:
            self.s_fix_desc = fdct_data["descricao"]

        # freqüência
        if "frequencia" in fdct_data:
            # freqüência
            self.f_fix_freq = float(fdct_data["frequencia"])

        # tipo
        if "tipo" in fdct_data:
            # obtém o tipo do fixo
            lc_tipo = str(fdct_data["tipo"]).strip().upper()

            # valida o sentido de curva
            self.en_fix_tipo = ldefs.DCT_TIPOS_FIXOS_INV.get(lc_tipo, ldefs.E_BRANCO)

        # coord (lat, lng)
        if "coord" in fdct_data:
            # latitude e longitude
            self.__f_fix_lat, self.__f_fix_lng = self.__model.coords.from_dict(fdct_data["coord"])

        # elevação (m)
        if "elevacao" in fdct_data:
            # elevação (m)
            self.f_fix_elev = float(fdct_data["elevacao"]) * cdefs.D_CNV_FT2M

        # converte para xyz
        self.f_fix_x, self.f_fix_y, self.f_fix_z = self.__model.coords.geo2xyz(self.__f_fix_lat, self.__f_fix_lng, 0.)

        # (bool)
        self.v_fix_ok = True

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def f_fix_elev(self):
        """
        get elevação do fixo
        """
        return self.__f_fix_elev

    @f_fix_elev.setter
    def f_fix_elev(self, f_val):
        """
        set elevação do fixo
        """
        self.__f_fix_elev = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_fix_freq(self):
        """
        get freqüência do fixo
        """
        return self.__f_fix_freq

    @f_fix_freq.setter
    def f_fix_freq(self, f_val):
        """
        set freqüência do fixo
        """
        self.__f_fix_freq = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_fix_lat(self):
        """
        get latitude
        """
        return self.__f_fix_lat

    @f_fix_lat.setter
    def f_fix_lat(self, f_val):
        """
        set latitude
        """
        self.__f_fix_lat = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_fix_lng(self):
        """
        get longitude
        """
        return self.__f_fix_lng

    @f_fix_lng.setter
    def f_fix_lng(self, f_val):
        """
        set longitude
        """
        self.__f_fix_lng = f_val

# < the end >--------------------------------------------------------------------------------------
