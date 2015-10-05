# -*- coding: utf-8 -*-

from __future__ import division

import pygame

from pygame.locals import *

def simplificar_fraccion(dividendo, divisor):
        for i in range(dividendo,2,-1):
            if dividendo%i == 0 and divisor%i == 0:
                    return dividendo/i, divisor/i
        return None

#CONSTANTES

pygame.display.init()

FPS = 60

RESOLUCION = [pygame.display.Info().current_w,pygame.display.Info().current_h]

RESOLUCION = 800,600

ANCHO_VENTANA, ALTO_VENTANA = RESOLUCION

ASPECTRO = RESOLUCION[0]/RESOLUCION[1]
ASPECTRO_P =  simplificar_fraccion(*RESOLUCION)

print ASPECTRO_P

DIMENSIONS_GL = 150
DIMENSIONS_GL_ESTANDAR = DIMENSIONS_GL*1.3333

ANCHO_PANTALLA_GL = DIMENSIONS_GL*ASPECTRO
ALTO_PANTALLA_GL = DIMENSIONS_GL

ANCHO_CADRO = 5
ALTO_CADRO = 5

MARCO_LATERAL = int(ANCHO_VENTANA - ((DIMENSIONS_GL_ESTANDAR*ANCHO_VENTANA)/ANCHO_PANTALLA_GL))
MARCO_VERTICAL = 0

COLOR_LIMPIADO = [1,1,1,1]

pos_camara = [0,0]
