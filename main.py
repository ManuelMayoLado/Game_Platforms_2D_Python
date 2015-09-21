# -*- coding: utf-8 -*-

from constantes import *
from clases import *

import ctypes
import os
import sys

if os.name == 'nt' and sys.getwindowsversion()[0] >= 6:
	ctypes.windll.user32.SetProcessDPIAware()

#VARIABLES

pos_camara = [0,0]

nivel = 0

tamanho_niveles = [[50,20],[500,300]]

NUM_CADROS_ANCHO_XOGO = tamanho_niveles[nivel][0]
NUM_CADROS_ALTO_XOGO = tamanho_niveles[nivel][1]

NUM_CADROS_TOTALES = NUM_CADROS_ANCHO_XOGO*NUM_CADROS_ALTO_XOGO

lista_cadros = []

#FUNCIONS SENCILLAS

def pos(n):
	return [n % NUM_CADROS_ANCHO_XOGO, n / NUM_CADROS_ANCHO_XOGO]

def num(p):
	return p[0]+p[1]*NUM_CADROS_ANCHO_XOGO

#LISTA DE CADROS(TILES)

for i in range(NUM_CADROS_TOTALES):
	lista_cadros.append(cadro(i,pos(i),False,False))

#INICIAR PYGAME

pygame.init()

#PANTALLA

ventana = pygame.display.set_mode(RESOLUCION,pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.HWSURFACE)

Superficie_tiles = pygame.Surface((ANCHO_XOGO,ALTO_XOGO), pygame.SRCALPHA|pygame.HWSURFACE).convert()

pygame.display.set_caption("Xogo_Plataformas")

#DEBUXAR CADROS EN SUPERFICIE

Superficie_tiles.fill((0,0,0))

'''
####USAR MELLOR FILL
'''

'''
pygame.draw.rect(Superficie_tiles,[200,100,100],rect_cadro)

for i in lista_cadros:
	if i.bool:
		rect_cadro = pygame.Rect(i.pos[0]*ANCHO_CADRO,i.pos[1]*ALTO_CADRO,ANCHO_PANTALLA,ALTO_CADRO)
		pygame.draw.rect(Superficie_tiles,[200,100,100],rect_cadro)
'''
#------------------------------------------------------------------------
#BUCLE XOGO
#------------------------------------------------------------------------

ON = True

def main():

	global ON

	while ON:

		reloj = pygame.time.Clock()

		############################################
		#DEBUXADO
		############################################

		ventana.fill((255,255,255))

		ventana.blit(Superficie_tiles,[0,0])

		#DEBUXAR CADRICULA

		for i in range(NUM_CADROS_ANCHO_XOGO):
			pygame.draw.line(ventana,(200,200,200),
							 (i*ANCHO_CADRO,0),
							 (i*ANCHO_CADRO,ALTO_XOGO))

		for i in range(NUM_CADROS_ALTO_XOGO):
			pygame.draw.line(ventana,(200,200,200),
							 (0,i*ALTO_CADRO),
							 (ANCHO_XOGO,i*ALTO_CADRO))

		############################################
		#EVENTOS
		############################################

		for evento in pygame.event.get():

			#TECLADO
			if evento.type == pygame.KEYDOWN:
				#ESC
				if evento.key == K_ESCAPE:
					ON = False

			#QUIT
			if evento.type == pygame.QUIT:
				ON = False

		if not ON:
			pygame.display.quit()
			break

		pygame.display.update()

		reloj.tick(FPS)

if __name__ == '__main__':
	main()