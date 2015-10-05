# -*- coding: utf-8 -*-

from __future__ import division

from constantes import *
from clases import *
from funcions import *

import ctypes
import os
import sys

if os.name == 'nt' and sys.getwindowsversion()[0] >= 6:
	ctypes.windll.user32.SetProcessDPIAware()

#FASES

lista_fases = [fase(0,100,30,"mapa_colisions.txt")]

fase_cargada = False

num_fase = 0

#PERSONAJE

pj = personaxe(0,[20,50],1,objeto_fisico([0,0],0.3,[0,0]))

#FUNCIONS SENCILLAS

NUM_CADROS_ANCHO_XOGO = 0

def pos(n):
	return [n % NUM_CADROS_ANCHO_XOGO, n / NUM_CADROS_ANCHO_XOGO]

def num(p):
	return p[0]+p[1]*NUM_CADROS_ANCHO_XOGO

#INICIAR PYGAME

pygame.init()

#VENTANA

ventana = pygame.display.set_mode([ANCHO_VENTANA,ALTO_VENTANA],FULLSCREEN|OPENGL|DOUBLEBUF|HWSURFACE)

pygame.display.set_caption("Xogo_Plataformas")

#------------------------------------------------------------------------
#FUNCION MAIN
#------------------------------------------------------------------------

_ON = True

def main():

	global _ON
	global _fase_cargada

	init_gl()

	#BUCLE XOGO
	#-----------------

	while _ON:

		reloj = pygame.time.Clock()

		#### CARGA DE FASE ####
		#######################

		if not fase_cargada:

			fase_actual = lista_fases[num_fase]

			#VARIABLES

			NUM_CADROS_ANCHO_FASE = fase_actual.cadros_ancho
			NUM_CADROS_ALTO_FASE = fase_actual.cadros_alto
			NUM_CADROS_TOTALES_FASE = NUM_CADROS_ANCHO_FASE * NUM_CADROS_ALTO_FASE
			lista_cadros_colision = []
			for i in range(NUM_CADROS_TOTALES_FASE):
				lista_cadros_colision.append(0)
			lista_cadros_colision = cargar_lista_cadros_colision(fase_actual.doc_col,lista_cadros_colision)

			ANCHO_FASE = fase_actual.ancho
			ALTO_FASE = fase_actual.alto

			vertices_cadricula = []

			for i in range(NUM_CADROS_ANCHO_FASE+1):
				vertices_cadricula.append([i*ANCHO_CADRO,0])
				vertices_cadricula.append([i*ANCHO_CADRO,ALTO_FASE])

			for i in range(NUM_CADROS_ALTO_FASE+1):
				vertices_cadricula.append([0,i*ALTO_CADRO])
				vertices_cadricula.append([ANCHO_FASE,i*ALTO_CADRO])

			#LISTAS DE OPENGL

			#CADRICULA

			LISTA_CADRICULA = glGenLists(1)
			glNewList(LISTA_CADRICULA, GL_COMPILE) ### INICIO LISTA
			glLoadIdentity()
			glBegin(GL_LINES)
			glColor4f(0.5, 0.5, 0.5, 0.5)
			for v in vertices_cadricula:
				glVertex2f(v[0],v[1])
			glEnd()
			glEndList()	############################### FIN LISTA

			_fase_cargada = True

		#######################

		#LIMPIAR VENTANA

		limpiar_ventana_gl()

		glLoadIdentity()
		glBegin(GL_QUADS)
		glColor4f(*COLOR_LIMPIADO)
		glVertex2f(pos_camara[0],pos_camara[1])
		glVertex2f(ANCHO_VENTANA+pos_camara[0],pos_camara[1])
		glVertex2f(ANCHO_VENTANA+pos_camara[0],ALTO_VENTANA+pos_camara[1])
		glVertex2f(pos_camara[0],ALTO_VENTANA+pos_camara[1])
		glEnd()


		############################################
		#DEBUXADO
		############################################

		#CADRICULA

		glCallList(LISTA_CADRICULA)

		#DEBUXAR PJ

		ver = [[0,0],[5,0],[5,5],[0,5]]

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

		if tecla_pulsada[K_d]:
			pj.fisica.vel[0] = 5

		if tecla_pulsada[K_a]:
			pj.fisica.vel[0] = -5

		#CAMARA

		if tecla_pulsada[K_RIGHT]:
			pos_camara[0] += 1
		if tecla_pulsada[K_LEFT]:
			pos_camara[0] -= 1
		if tecla_pulsada[K_UP]:
			pos_camara[1] += 1
		if tecla_pulsada[K_DOWN]:
			pos_camara[1] -= 1

		#EVENTOS

		for evento in pygame.event.get():

			#TECLADO
			if evento.type == pygame.KEYDOWN:
				#ESC
				if evento.key == K_ESCAPE:
					_ON = False

			#QUIT
			if evento.type == pygame.QUIT:
				_ON = False

		if not _ON:
			pygame.display.quit()
			break

		pygame.display.flip()

		reloj.tick(FPS)

if __name__ == '__main__':
	main()