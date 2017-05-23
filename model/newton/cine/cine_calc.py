#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
cine_calc

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
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
# import logging
import math

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------
def calc_direcao(ft_pto1, ft_pto2):
    """
    DOCUMENT ME!
    """
    # calcula os deltas entre os ponto
    lf_dlt_x = ft_pto2[0] - ft_pto1[0]
    # M_LOG.debug ( "lf_dlt_x: " + str ( lf_dlt_x ))

    lf_dlt_y = ft_pto2[1] - ft_pto1[1]
    # M_LOG.debug ( "lf_dlt_y: " + str ( lf_dlt_y ))

    # os pontos estão na mesma coluna ?
    if 0. == lf_dlt_x:
        # os pontos estão na mesma linha ?
        if 0. == lf_dlt_y:
            # X e Y são o mesmo ponto, ângulo zero entre eles
            lf_ang = 0.

        # y2 > y1 ?
        elif lf_dlt_y > 0.:
            # y2 > y1, logo 180 graus entre eles (pi)
            lf_ang = math.pi / 2.

        # senão, y2 < y1
        else:
            # y2 < y1, logo -180 graus entre eles (3pi)
            lf_ang = 3. * math.pi / 2.

    # senão, não estão na mesma coluna
    else:
        # calcula o ângulo entre eles
        lf_ang = math.atan(lf_dlt_y / lf_dlt_x)

    # converte o ângulo em graus
    lf_deg = math.degrees(lf_ang)
    # M_LOG.debug ( "lf_deg: " + str ( lf_deg ))

    # x2 < x1
    if lf_dlt_x < 0.:
        lf_deg += math.degrees(math.pi)

    else:
        # x2 > x1 ?
        if lf_deg < 0.:
            lf_deg += math.degrees(2. * math.pi)

    # retorna a direção
    return lf_deg

# -------------------------------------------------------------------------------------------------
def conv_proa2direcao(ff_proa):
    """
    converte uma proa para um ângulo nos eixos cartesianos.
    """
    # proa e direção
    lf_proa = ff_proa

    # 2Pi degrees
    lf_2pi = math.degrees(2. * math.pi)

    # normaliza a proa (I)
    while lf_proa < 0.:
        lf_proa += lf_2pi

    # normaliza a proa (II)
    while lf_proa >= lf_2pi:
        lf_proa -= lf_2pi

    # converte a proa para radianos
    lf_proa = math.radians(lf_proa)

    # calcula as componentes X e Y da proa
    lf_proa_y = math.sin(lf_proa)
    lf_proa_x = math.cos(lf_proa)

    if lf_proa_x > 0.:
        if lf_proa_y > 0.:
            # direção
            lf_dir = math.asin(lf_proa_x)

        else:
            # componentes da direção
            lf_x_d = lf_proa_x
            lf_y_d = lf_proa_y

            # direção
            lf_dir = math.atan2(lf_x_d, lf_y_d)

    elif lf_proa_y > 0.:
        # componentes da direção
        lf_x_d = lf_proa_x
        lf_y_d = lf_proa_y

        # direção
        lf_dir = math.atan2(lf_x_d, lf_y_d) + (2. * math.pi)

    else:
        # direção
        lf_dir = math.pi + math.fabs(math.asin(lf_proa_x))

    # converte a direção para graus
    lf_dir = math.degrees(lf_dir)

    # zera infinitesimais
    if math.fabs(lf_dir) < 1.E-1:
        lf_dir = 0.

    # adapta a direção da aeronave ao norte magnético
    # lf_dir -= ft_Proa [ 1 ]

    # normaliza a direção (I)
    while lf_dir < 0.:
        lf_dir += lf_2pi

    # normaliza a direção (II)
    while lf_dir >= lf_2pi:
        lf_dir -= lf_2pi

    # retorna a direção
    return lf_dir

# -------------------------------------------------------------------------------------------------
def distancia_aleatoria_pouso(fui_pst_comp):
    """
    @return a distância retornada refere-se a distância até ao início da cabeceira.
    """
    # não está sendo considerada a aleatoreidade no pouso para que todas as aeronaves do
    # PeelOff pousem no mesmo ponto e saiam na mesma posição da pista principal para o taxi.
    if 0:
        lf_media = fui_pst_comp / 10.
        '''
        l_sigma = lf_media / 3.26

        R1 = Lib.Rand ()
        R2 = Lib.Rand ()

        X1 = math.sqrt ( -2. * math.log ( R1 )) * math.cos ( 2. * math.pi * R2 )

        X = lf_media + ( X1 * l_sigma )
        '''
    else:
        lf_media = fui_pst_comp / 15.

    # retorna a distância
    return lf_media

# -------------------------------------------------------------------------------------------------
def distancia_direcao(ft_pto1, ft_pto2):
    """
    calcula a distância e direção entre dois pontos.
    """
    # calcula a distância entra os pontos
    lf_dist = distancia_entre_pontos(ft_pto1, ft_pto2)

    # calcula a distância entra os pontos
    lf_deg = calc_direcao(ft_pto1, ft_pto2)

    # retorna a distância e o ângulo entre os pontos
    return lf_dist, lf_deg

# -------------------------------------------------------------------------------------------------
def distancia_entre_pontos(ft_pto1, ft_pto2):
    """
    calcula a distância euclidiana entre os pontos
    """
    # calcula o delta X entre os pontos (dx)
    lf_dlt_x = ft_pto1[0] - ft_pto2[0]
    # M_LOG.debug ( "lf_dlt_x: " + str ( lf_dlt_x ))

    # calcula o delta Y entre os pontos (dy)
    lf_dlt_y = ft_pto1[1] - ft_pto2[1]
    # M_LOG.debug ( "lf_dlt_y: " + str ( lf_dlt_y ))

    # retorna a distância euclidiana entre os pontos
    return math.sqrt((lf_dlt_x ** 2) + (lf_dlt_y ** 2))

# -------------------------------------------------------------------------------------------------
def distancia_inicio_curva(ff_dir_atu, ff_dir_reta, fd_raio):
    """
    calcula a distância entre o ponto de inicio da curva ate a reta em questão.
    """
    lf_teta = math.degrees(math.pi) - math.fabs(ff_dir_atu - ff_dir_reta)
    lf_teta = math.radians(lf_teta)

    lf_dist = fd_raio / math.tan(lf_teta / 2.)
    lf_dist *= math.sin(lf_teta)

    # retorna a distância
    return lf_dist

# -------------------------------------------------------------------------------------------------
def distancia_ponto_reta(ft_pto, ft_reta):
    """
    calcula a distância (com sinal) de um ponto a uma reta no plano.

    @param ft_pto:  tupla ponto ( x, y )
    @param ft_reta: tupla reta ( a, b, c )
    """
    # calcula a raiz
    lf_sqrt = math.sqrt((ft_reta[0] ** 2) + (ft_reta[1] ** 2))
    # assert 0. != lf_sqrt

    lf_val = ((ft_reta[0] * ft_pto[0]) + (ft_reta[1] * ft_pto[1]) + ft_reta[2])

    # retorna a distância
    return lf_val / lf_sqrt

# -------------------------------------------------------------------------------------------------
def distancia_ponto_reta_abs(ft_pto, ft_reta):
    """
    calcula a distância de um ponto a uma reta no plano

    @param ft_pto:  tupla ponto ( x, y ).
    @param ft_reta: tupla reta ( a, b, c ).
    """
    # retorna a distância
    return math.fabs(distancia_ponto_reta(ft_pto, ft_reta))

# -------------------------------------------------------------------------------------------------
def sentido_rotacao(ff_dir, fd_dem):
    """
    verifica se a aeronave deve girar para a esquerda, direita ou manter a direção atual.

    @return I = igual, H = horário ou A = anti-horário.
    """
    # obtém a direção atual
    li_dir = int(round(ff_dir))

    # obtém a direção de demanda
    li_dem = int(round(fd_dem))

    # direção atual = demanda ?
    if li_dem == li_dir:
        # se for, mantem o sentido
        lc_sentido = 'I'

    # senão, direção atual != demanda
    else:
        # direção demanda < atual ?
        if li_dem < li_dir:
            # ajusta a demanda
            li_dem += 360

        if (li_dem - li_dir) > 180:
            # se for, sentido horário
            lc_sentido = 'H'

        else:
            # se não, sentido anti-horário
            lc_sentido = 'A'

    # retorna o sentido
    return lc_sentido

# < the end >--------------------------------------------------------------------------------------
