#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
glb_defs

defines e constantes válidas globalmente

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

# < config >---------------------------------------------------------------------------------------

# arquivo de configuração
D_CFG_FILE = "tracks.cfg"

# < diretórios >-----------------------------------------------------------------------------------

# diretório de airspaces
D_DIR_AIR = "airs"

# diretório de dados
D_DIR_DAT = "data"

# diretório de exercícios
D_DIR_EXE = "exes"

# diretório de imagens
D_DIR_IMG = "images"

# diretório de landscapes
D_DIR_MAP = "maps"

# diretório de procedimentos
D_DIR_PRC = "proc"

# diretório de sons
D_DIR_SND = "sounds"

# diretório de tabelas
D_DIR_TAB = "tabs"

# diretório de tráfegos
D_DIR_TRF = "traf"

# < mensagens >------------------------------------------------------------------------------------

# versão do conjunto de mensagens
D_MSG_VRS = 101

# códigos das mensagens

D_MSG_ADS = 111    # mensagens de dados ADS-B
D_MSG_CAD = 112    # mensagens de dados SiCAD
D_MSG_COR = 113    # mensagens de dados CORE
D_MSG_GAL = 114    # mensagens de dados galileu
D_MSG_NEW = 115    # mensagens de dados newton
D_MSG_PAR = 116    # mensagens de dados PAR

# mensagens de controle de exibição

# D_MSG_CKT = 121    # circuito  
D_MSG_CSG = 122    # callsign
D_MSG_RMK = 123    # range mark
# D_MSG_WRS = 124    # windrose

# mensagens de controle de aeronaves

# D_MSG_EXP = 131    # explosão da aeronave
D_MSG_KLL = 132    # cancela a aeronave
D_MSG_PIL = 133    # comandos de pilotagem

# mensagens de controle de simulação

D_MSG_ACC = 141    # fator de aceleração
D_MSG_EXE = 142    # código do exercício
D_MSG_FIM = 143    # término de simulação
D_MSG_FRZ = 144    # congela
D_MSG_SRV = 145    # servidor
D_MSG_TIM = 146    # horário
D_MSG_UFZ = 147    # descongela

# separador de campos na mensagem

D_MSG_SEP = '#'

# códigos das mensagens tratadas
# SET_MSG_TRATADAS = [D_MSG_CKT, D_MSG_EXP, D_MSG_WRS]

# códigos das mensagens válidas
SET_MSG_VALIDAS = [D_MSG_ACC, D_MSG_ADS, D_MSG_CAD, D_MSG_PIL, D_MSG_CSG, D_MSG_EXE, \
                   D_MSG_FIM, D_MSG_FRZ, D_MSG_GAL, D_MSG_KLL, D_MSG_NEW, D_MSG_PAR, \
                   D_MSG_RMK, D_MSG_SRV, D_MSG_TIM, D_MSG_UFZ,]

# códigos das mensagens válidas
SET_MSG_SUPER = [D_MSG_ACC, D_MSG_FIM, D_MSG_FRZ, D_MSG_UFZ]

# < rede >-----------------------------------------------------------------------------------------

# endereço default (multicast addresses range 224.0.0.0 / 239.255.255.255)
D_NET_ADDR = "227.12.2"
# endereço multicast de configuração
D_NET_CNFG = "229.12.2"
# endereço multicast de pilotagem
D_NET_CPIL = "231.12.2"
# endereço multicast de sensor
D_NET_SNSR = "233.12.2"
# endereço multicast de pistas
D_NET_TRKS = "235.12.2"
# endereço multicast de voip
D_NET_VOIP = "237.12.2"
# porta de comunicação
D_NET_PORT = 1970

# interface de entrada
D_NET_IFIN = None
# interface de saída
D_NET_IOUT = None

# web server
D_SRV_ADDR = "localhost"
D_SRV_PORT = 61000

# < tables >---------------------------------------------------------------------------------------

# tabela de aeródromos
D_TBL_AER = "tabAer"

# tabela de procedimentos de aproximação
D_TBL_APX = "tabApx"

# tabela de procedimentos de espera
D_TBL_ESP = "tabEsp"

# tabela de fixos
D_TBL_FIX = "tabFix"

# tabela de performances
D_TBL_PRF = "tabPrf"

# tabela de procedimentos de subida
D_TBL_SUB = "tabSub"

# tabela de procedimentos de trajetória
D_TBL_TRJ = "tabTrj"

# tabela de waypoints
D_TBL_WPT = "tabWpt"

# colour table
D_TBL_COLOUR = "tabColor.dat"

# font table
D_TBL_FONT = "tabFont.dat"

# < temporização >---------------------------------------------------------------------------------

# fast-time simulation acceleration factor
D_TIM_ACCL = 1

# reenvia a configuração do sistema a cada 5 seg (int)
D_TIM_CNFG = 5

# envio de mensagens de posicionamento de pistas ao CORE a cada 2 seg (int)
D_TIM_CORE = 2

# verifica o tempo de ativação das aeronaves a cada 30 seg (int)
D_TIM_FGEN = 30

# reenvia a hora do sistema a cada 1 seg (1Hz) (int)
D_TIM_HORA = 1

# verifica colisão entre aeronaves a cada 1 seg (1Hz) (int)
D_TIM_PROX = 1

# rotação do radar (4s)
D_TIM_RDAR = 4


# tratador de eventos (10Hz) (float)
D_TIM_EVNT = .1

# refresh de tela (10Hz) (float)
D_TIM_REFR = .1

# permite o schedule do sistema (round robin) (10Hz) (float)
D_TIM_RRBN = .1

# recalculo de posição de aeronave (1Hz) (float)
D_TIM_WAIT = 1

# < the end >--------------------------------------------------------------------------------------
