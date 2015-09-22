# -*- coding: utf-8 -*-

from constantes import *
from clases import *
from funcions import *

import ctypes
import os
import sys

if os.name == 'nt' and sys.getwindowsversion()[0] >= 6:
	ctypes.windll.user32.SetProcessDPIAware()

#VARIABLES

pos_camara = [0,0]

nivel = 0

tamanho_niveles = [[200,100],[500,300]]

NUM_CADROS_ANCHO_XOGO = tamanho_niveles[nivel][0]
NUM_CADROS_ALTO_XOGO = tamanho_niveles[nivel][1]

NUM_CADROS_TOTALES = NUM_CADROS_ANCHO_XOGO*NUM_CADROS_ALTO_XOGO

lista_cadros_colision = []

#PERSONAJE

pj = personaxe(0,[20,50],1,objeto_fisico([0,0],0.3,[0,0]))

#FUNCIONS SENCILLAS

def pos(n):
	return [n % NUM_CADROS_ANCHO_XOGO, n / NUM_CADROS_ANCHO_XOGO]

def num(p):
	return p[0]+p[1]*NUM_CADROS_ANCHO_XOGO

#LISTA DE CADROS(TILES)

for i in range(NUM_CADROS_TOTALES):
	lista_cadros_colision.append(0)

lista_cadros_colision = cargar_lista_cadros_colision("mapa_colisions.txt",lista_cadros_colision)

#INICIAR PYGAME

pygame.init()

#PANTALLA

ventana = pygame.display.set_mode(RESOLUCION,pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.HWSURFACE)

Superficie_tiles = pygame.Surface((ANCHO_XOGO,ALTO_XOGO),pygame.SRCALPHA|pygame.HWSURFACE).convert_alpha()

pygame.display.set_caption("Xogo_Plataformas")

#DEBUXAR CADROS-COLISION EN SUPERFICIE

for i in range(len(lista_cadros_colision)):
	if lista_cadros_colision[i]:
		rect_cadro_colision = pygame.Rect(pos(i)[0]*ANCHO_CADRO,pos(i)[1]*ALTO_CADRO,ANCHO_CADRO,ALTO_CADRO)
		Superficie_tiles.fill([200,50,50],rect_cadro_colision)

print lista_cadros_colision

#------------------------------------------------------------------------
#FUNCION MAIN
#------------------------------------------------------------------------

ON = True

def main():

	global ON

	#BUCLE XOGO
	#----------

	while ON:

		reloj = pygame.time.Clock()

		############################################
		#DEBUXADO
		############################################

		ventana.fill((255,255,255))

		#DEBUXAR CADRICULA

		for i in range(NUM_CADROS_ANCHO_XOGO):
			pygame.draw.line(ventana,(200,200,200),
							 (i*ANCHO_CADRO,0),
							 (i*ANCHO_CADRO,ALTO_XOGO))

		for i in range(NUM_CADROS_ALTO_XOGO):
			pygame.draw.line(ventana,(200,200,200),
							 (0,i*ALTO_CADRO),
							 (ANCHO_XOGO,i*ALTO_CADRO))

		ventana.blit(Superficie_tiles,[0,0])

		#DEBUXAR PJ

		rect_pj = pygame.Rect(pj.pos,[ANCHO_CADRO,ALTO_CADRO*2])
		pygame.draw.rect(ventana,[0,0,200],rect_pj)

		###########################################
		#FISICA
		###########################################

		pj.fisica.vel[1] += pj.fisica.gravedad

		pj.pos = pj.pos[0]+pj.fisica.vel[0],pj.pos[1]+pj.fisica.vel[1]


		############################################
		#EVENTOS
		############################################

		######TECLAS PULSADAS######

		tecla_pulsada = pygame.key.get_pressed()

		if tecla_pulsada[K_RIGHT] or tecla_pulsada[K_d]:
			pj.fisica.vel[0] = 5

		if tecla_pulsada[K_LEFT] or tecla_pulsada[K_a]:
			pj.fisica.vel[0] = -5


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