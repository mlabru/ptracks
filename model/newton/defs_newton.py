#/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
defs_newton

defines e constantes válidas localmente

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/out  mlabru
initial release (Python/Linux)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < enums >----------------------------------------------------------------------------------------

# estado operacional (newton)
E_AUTOMATICA, E_CONTROLADA = xrange(2)

SET_EST_OPE = [E_AUTOMATICA, E_CONTROLADA]

# estado de ativação da aeronave (newton)
E_ATIVA, E_CANCELADA, E_FINALIZADA, E_PENDENTE, E_QUEUED = xrange(5)

SET_EST_ATV = [E_ATIVA, E_CANCELADA, E_FINALIZADA, E_PENDENTE, E_QUEUED]

# função operacional (newton)
E_ALT, E_APROXIMACAO, E_APXPERDIDA, E_CANCELA, E_CDIR, E_CESQ, E_CMNR, E_DECOLAGEM, E_DES, E_DIRFIXO, \
    E_DIRPNTO, E_ESPERA, E_IAS, E_ILS, E_INTRADIAL, E_MACH, E_MANUAL, E_MOV, E_NIV, E_NOPROC, E_POUSO, \
    E_PROA, E_SSR, E_SUB, E_SUBIDA, E_TRAJETORIA, E_VEL, E_VISU = xrange(28)

SET_FNC_OPE = [E_ALT, E_APROXIMACAO, E_APXPERDIDA, E_CANCELA, E_CDIR, E_CESQ, E_CMNR,E_DECOLAGEM, 
               E_DES, E_DIRFIXO, E_DIRPNTO, E_ESPERA, E_IAS, E_ILS, E_INTRADIAL, E_MACH, E_MANUAL, 
               E_MOV, E_NIV, E_NOPROC, E_POUSO, E_PROA, E_SSR, E_SUB, E_SUBIDA, E_TRAJETORIA, E_VEL, E_VISU]

DCT_FNC_OPE = {E_ALT:"ALT", E_APROXIMACAO:"APROXIMACAO", E_APXPERDIDA:"APXPERDIDA",
               E_CANCELA:"CANCELA", E_CDIR:"CDIR", E_CESQ:"CESQ", E_CMNR:"CMNR", E_DECOLAGEM:"DECOLAGEM", 
               E_DES:"DES", E_DIRFIXO:"DIRFIXO", E_DIRPNTO:"DIRPNTO", E_ESPERA:"ESPERA", E_IAS:"IAS", 
               E_ILS:"ILS", E_INTRADIAL:"INTRADIAL", E_MACH:"MACH", E_MANUAL:"MANUAL", E_MOV:"MOV", 
               E_NIV:"NIV", E_NOPROC:"NOPROC", E_POUSO:"POUSO", E_PROA:"PROA", E_SSR:"SSR", 
               E_SUBIDA:"SUBIDA", E_SUB:"SUB", E_TRAJETORIA:"TRAJETORIA", E_VEL:"VEL", E_VISU:"VISU"}

# fases de processamento da cinemática (newton)
E_FASE_2R, E_FASE_AFASTA, E_FASE_ALINHAR, E_FASE_APXALINHAR, E_FASE_ASSOCIADO, \
    E_FASE_BREAKPOINT, E_FASE_CRVAFASTA, E_FASE_CURVA, E_FASE_DECOLAGEM, E_FASE_DIRFIXO, \
    E_FASE_DIRPONTO, E_FASE_EIXO, E_FASE_ESPERA, E_FASE_ESTABILIZADA, E_FASE_FIXO, \
    E_FASE_INTERCEPTACAO, E_FASE_OPOSTA, E_FASE_PISTA, E_FASE_PROAINT, E_FASE_RAMPA, \
    E_FASE_RUMOALT, E_FASE_SETOR1, E_FASE_SETOR2, E_FASE_SETOR3, E_FASE_SUBIDA, E_FASE_TEMPO, \
    E_FASE_TEMPOSETOR, E_FASE_VOLTA, E_FASE_ZERO = xrange(29)

SET_FASE = [E_FASE_2R, E_FASE_AFASTA, E_FASE_ALINHAR, E_FASE_APXALINHAR, E_FASE_ASSOCIADO,
            E_FASE_BREAKPOINT, E_FASE_CRVAFASTA, E_FASE_CURVA, E_FASE_DECOLAGEM,
            E_FASE_DIRFIXO, E_FASE_DIRPONTO, E_FASE_EIXO, E_FASE_ESPERA, E_FASE_ESTABILIZADA,
            E_FASE_FIXO, E_FASE_INTERCEPTACAO, E_FASE_OPOSTA, E_FASE_PISTA, E_FASE_PROAINT,
            E_FASE_RAMPA, E_FASE_RUMOALT, E_FASE_SETOR1, E_FASE_SETOR2, E_FASE_SETOR3,
            E_FASE_SUBIDA, E_FASE_TEMPO, E_FASE_TEMPOSETOR, E_FASE_VOLTA, E_FASE_ZERO]

DCT_FASE = {E_FASE_2R: "2R", E_FASE_AFASTA: "AFASTA", E_FASE_ALINHAR: "ALINHAR",
            E_FASE_APXALINHAR: "APXALINHAR", E_FASE_ASSOCIADO: "ASSOCIADO",
            E_FASE_BREAKPOINT: "BREAKPOINT", E_FASE_CRVAFASTA: "CRVAFASTA",
            E_FASE_CURVA: "CURVA", E_FASE_DECOLAGEM: "DECOLAGEM", E_FASE_DIRFIXO: "DIRFIXO",
            E_FASE_DIRPONTO: "DIRPONTO", E_FASE_EIXO: "EIXO", E_FASE_ESPERA: "ESPERA",
            E_FASE_ESTABILIZADA: "ESTABILIZADA", E_FASE_FIXO: "FIXO",
            E_FASE_INTERCEPTACAO: "INTERCEPTACAO", E_FASE_OPOSTA: "OPOSTA",
            E_FASE_PISTA: "PISTA", E_FASE_PROAINT: "PROAINT", E_FASE_RAMPA: "RAMPA",
            E_FASE_RUMOALT: "RUMOALT", E_FASE_SETOR1: "SETOR1", E_FASE_SETOR2: "SETOR2",
            E_FASE_SETOR3: "SETOR3", E_FASE_SUBIDA: "SUBIDA", E_FASE_TEMPO: "TEMPO",
            E_FASE_TEMPOSETOR: "TEMPOSETOR", E_FASE_VOLTA: "VOLTA", E_FASE_ZERO: "ZERO"}

# sentidos de curva (D = direita, E = esquerda, M = menor ângulo) (newton)
E_DIREITA, E_ESQUERDA, E_MENOR = xrange(3)

SET_SENTIDOS_CURVA = [E_DIREITA, E_ESQUERDA, E_MENOR]

DCT_SENTIDOS_CURVA = {E_DIREITA:'D', E_ESQUERDA:'E', E_MENOR:'M'}

DCT_SENTIDOS_CURVA_INV = {v:k for k, v in DCT_SENTIDOS_CURVA.iteritems()}

# tipos de fixos (' ' = s/tipo, 'D' = DME, 'N' = NDB, 'V' = VOR)
E_BRANCO, E_DME, E_NDB, E_VOR = xrange(4)

SET_TIPOS_FIXOS = [E_BRANCO, E_DME, E_NDB, E_VOR]

DCT_TIPOS_FIXOS = {E_BRANCO:"s/tipo", E_DME:"DME", E_NDB:"NDB", E_VOR:"VOR"}

DCT_TIPOS_FIXOS_INV = {'D':E_DME, 'N':E_NDB, 'V':E_VOR} 

# < formats >--------------------------------------------------------------------------------------

D_FMT_APX = "APX{:03d}"
D_FMT_ESP = "ESP{:03d}"
D_FMT_FIX = "{}"
D_FMT_SUB = "SUB{:03d}"
D_FMT_TRJ = "TRJ{:04d}"

# < aeronaves >------------------------------------------------------------------------------------

# RotacaoSolo = 15.  # graus/seg
# RotacaoSolo8 = 45.  # graus/seg (família 8)

# VarAngTrafego = 6.  # graus/seg
# VarAngTrafego8 = 15.  # graus/seg (família 8)

# VarAngRota = 3.  # graus/seg
# VarAngRota8 = 7.  # graus/seg (família 8)

# < máximos >--------------------------------------------------------------------------------------

# quantidade máxima de aerádromos
# D_MAX_Aerodromos = 1

# quantidade máxima de aeronaves
# D_MAX_Aeronaves = 50

# quantidade máxima de aeronaves ativas
# D_MAX_Ativas = 12  # para resolução de (  800,  600 )
# D_MAX_Ativas = 13  # para resolução de ( 1024,  768 )
# D_MAX_Ativas = 17  # para resolução de ( 1280,  960 )
# D_MAX_Ativas = 15  # para resolução de ( 1280,  990 )
# D_MAX_Ativas = 19  # para resolução de ( 1280, 1024 )
# D_MAX_Ativas = 5000  # para resolução de ( 1280,  990 )

# quantidade máxima de cabeceiras
# D_MAX_Cabeceiras = 2

# quantidade máxima de circuitos
# D_MAX_Circuitos = 3

# quantidade de desenhos de aeronaves
# D_MAX_Desenhos = 5

# quantidade máxima de escalas
# D_MAX_Escalas = 3

# quantidade máxima de famílias
# D_MAX_Familias = 8

# quantidade máxima de figuras do cenário
# D_MAX_Figuras = 40

# quantidade máxima de gravações para replay
# D_MAX_Gravações = 5000

# quantidade máxima de pistas
# D_MAX_Pistas = 2

# quantidade máxima de pontos adjacentes
# D_MAX_PontosAdjs = 5

# quantidade máxima de pontos de saída de pista
# D_MAX_PontosArr = 6

# quantidade máxima de pontos de decolagem
# D_MAX_PontosDep = 3

# quantidade máxima de pontos no solo
# D_MAX_PontosNoSolo = 45

# quantidade máxima de segmentos
# D_MAX_Segmentos = 4

# quantidade máxima de trechos no percurso
# D_MAX_Trechos = 30

# quantidade máxima de vértices de um polígono
# D_MAX_Vertices = 40

# < quantidades >----------------------------------------------------------------------------------

# quantidade de atributos dos dados de aeronaves
# D_QTD_AtribAnv = 13

# quantidade de atributos dos dados gerais do exercício
# D_QTD_AtribExe = 12

# quantidade de atributos das aeronaves
# D_QTD_AtribAer = 9

# quantidade de atributos das pistas
# D_QTD_AtribPista = 17

# quantidade de atributos dos dados iniciais do cenário. Os atributos quantidade de Pistas e
# quantidade de Pontos no Solo ficam em posições dos outros seis atributos diferentes no arquivo
# D_QTD_AtribIniciais = 8

# quantidade de itens da tabela de performace
# D_QTD_ItensPerform = 16

# < sets >-----------------------------------------------------------------------------------------

# S_ConfValidas = ['S', 'N']
# S_EscalasValidas = [1, 2, 3]
# S_SentidosGiro = ['A', 'H', 'I']

# S_STATUS_Aeronaves = ['A', 'E']
# S_STATUS_Circuitos = ['C', 'K', 'V']
# S_STATUS_Exercicio = ['D', 'G', 'T']

# status solo (newton)
# !V!S_STATUS_SOLO = ['C', 'D', 'P']

# status vôo (newton)
SET_STATUS_VOO = ['C', 'D', 'P']

# S_ProasValidas = [ x for x in xrange ( 360 ) ]
# S_DifAngValidas = [x for x in xrange(160, 200)]
# S_DifAngAceitaveis = [x for x in xrange(0, 20)]
# S_AeronavesValidas = [ ( x + 1 ) for x in xrange ( xMAX_Aeronaves ) ]
# S_FamiliasValidas  = [ ( x + 1 ) for x in xrange ( xMAX_Familias ) ]
# S_CircuitosValidos = [ ( x + 1 ) for x in xrange ( xMAX_Circuitos ) ]

# < texts >----------------------------------------------------------------------------------------

# versão
# D_TXT_Mjr = "0"
# D_TXT_Mnr = "1"
# D_TXT_Rls = "0.1p"
# D_TXT_Vrs = D_TXT_Mjr + "." + D_TXT_Mnr
# D_TXT_Bld = D_TXT_Vrs + "-" + D_TXT_Rls

# programa
# D_TXT_Prg = "newton"
# D_TXT_Tit = D_TXT_Prg + " " + D_TXT_Vrs
# D_TXT_Hdr = D_TXT_Prg + " " + D_TXT_Bld

# mensagens de erro (gvm)
# D_MSG_MNA = u"Máquina não autorizada. Terminando !!!"

# mensagens ao piloto
# D_MSG_01 = 1
# D_MSG_45 = 45
# D_MSG_46 = 46
# D_MSG_47 = 47
# D_MSG_48 = 48
# D_MSG_49 = 49
# D_MSG_50 = 50

# < defines >--------------------------------------------------------------------------------------

# fator de aceleração na fase de decolagem (from cfg)
D_FATOR_ACEL = 2

# altitude máxima na TMA (from cfg)
D_ALT_MAX_TMA = 50000  # era 10000

# velocidade máxima na TMA (from cfg)
D_VEL_MAX_TMA = 500  # era 250

# variação de temperatura
G_EXE_VAR_TEMP_ISA = 10

# flight levels (newton)
# D_FL250 = 7620.0    # Fl 250 em metros (25000 x FT2M = 7620.0 m)
# D_FL280 = 8534.4    # Fl 280 em metros (28000 x FT2M = 8534.4 m)

# D_GAMA = 1.4     # razão de calor específico para o ar nas CNTP.
# D_RGAS = 1718    # modelo da atmosfera terrestre da NASA, baseada em valores de densidade, pressão e temperatura do ar

# definição para pouso e ILS (newton)
D_DST_RAMPA = 3

# D_FAIXA_MT = 15.2392563
# D_RAZAO_LIM = 5.5877

# definição para interceptação de radial
# D_ESQUERDA = 1
# D_DIREITA = -1

# D_RAD_C = -1
# D_RAD_S = 1

# D_QDM = -1
# D_QDR = 1

# < the end >--------------------------------------------------------------------------------------
