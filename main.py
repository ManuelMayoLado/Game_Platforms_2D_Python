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

#VARIABLES

camara_libre = False
mostrar_cadricula = True

#FASES

lista_fases = [fase(0,50,30,"mapa_colisions.txt")]

fase_cargada = False

num_fase = 0

#PERSONAJE

pj = personaxe(0,[20,120],1,objeto_fisico([0,0],0.1,[]))

#INICIAR PYGAME

pygame.init()

#VENTANA

ventana = pygame.display.set_mode([ANCHO_VENTANA,ALTO_VENTANA],OPENGL|DOUBLEBUF|HWSURFACE)

pygame.display.set_caption("Xogo_Plataformas")

#------------------------------------------------------------------------
#FUNCION MAIN
#------------------------------------------------------------------------

_ON = True

def main():

	global _ON
	global _fase_cargada
	global camara_libre
	global mostrar_cadricula

	movemento_pj = []

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

			lista_vertices_cadros_colision = []
			for i in range(len(lista_cadros_colision)):
				if lista_cadros_colision[i]:
					pos_cadro = pos(i,NUM_CADROS_ANCHO_FASE)
					lista_vertices_cadros_colision.append(
						[pos_cadro[0]*ANCHO_CADRO,pos_cadro[1]*ALTO_CADRO])
					lista_vertices_cadros_colision.append(
						[pos_cadro[0]*ANCHO_CADRO+ANCHO_CADRO,pos_cadro[1]*ALTO_CADRO])
					lista_vertices_cadros_colision.append(
						[pos_cadro[0]*ANCHO_CADRO+ANCHO_CADRO,pos_cadro[1]*ALTO_CADRO+ALTO_CADRO])
					lista_vertices_cadros_colision.append(
						[pos_cadro[0]*ANCHO_CADRO,pos_cadro[1]*ALTO_CADRO+ALTO_CADRO])

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

			#CADROS_COLISION

			LISTA_CADROS_COLISION = glGenLists(2)
			glNewList(LISTA_CADROS_COLISION, GL_COMPILE) ### INICIO LISTA
			glLoadIdentity()
			glBegin(GL_QUADS)
			glColor4f(1,0.3,0.3,1)
			for v in lista_vertices_cadros_colision:
				glVertex2f(v[0],v[1])
			glEnd()
			glEndList() ############################### FIN LISTA

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
		#######################

		#LIMPIAR VENTANA

		limpiar_ventana_gl()

		glColor4f(1, 1, 1, 1)
		debuxar_rect_gl(
			[(pos_camara[0],pos_camara[1]),
			(ANCHO_VENTANA+pos_camara[0],pos_camara[1]),
			(ANCHO_VENTANA+pos_camara[0],ALTO_VENTANA+pos_camara[1]),
			(pos_camara[0],ALTO_VENTANA+pos_camara[1])]
		)

		############################################
		#DEBUXADO
		############################################

		#CADROS_COLISION

		glCallList(LISTA_CADROS_COLISION)

		#DEBUXAR PJ

		glColor4f(0, 0, 0.8, 1)
		debuxar_rect_gl(
			[(pj.pos[0],pj.pos[1]),
			(pj.pos[0]+ANCHO_CADRO,pj.pos[1]),
			(pj.pos[0]+ANCHO_CADRO,pj.pos[1]+ALTO_CADRO*2),
			(pj.pos[0],pj.pos[1]+ALTO_CADRO*2)]
		)

		#CADRICULA

		if mostrar_cadricula:
			glCallList(LISTA_CADRICULA)

		###########################################
		#FISICA
		###########################################

		pj.fisica.vel[1] -= pj.fisica.gravedad

		for impulso in pj.fisica.impulsos:
			pj.fisica.vel[0] += impulso[0]
			pj.fisica.vel[1] += impulso[1]

		pj.pos = pj.pos[0]+pj.fisica.vel[0],pj.pos[1]+pj.fisica.vel[1]

		############################################
		#EVENTOS
		############################################

		######TECLAS PULSADAS######

		tecla_pulsada = pygame.key.get_pressed()

		if tecla_pulsada[K_d]:
			pj.fisica.vel[0] = 1

		if tecla_pulsada[K_a]:
			pj.fisica.vel[0] = -1

		if tecla_pulsada[K_d] and tecla_pulsada[K_a] or not(tecla_pulsada[K_d] or tecla_pulsada[K_a]):
			pj.fisica.vel[0] = 0

		#CAMARA

		if camara_libre:
			if tecla_pulsada[K_RIGHT]:
				pos_camara[0] += 1
			if tecla_pulsada[K_LEFT]:
				pos_camara[0] -= 1
			if tecla_pulsada[K_UP]:
				pos_camara[1] += 1
			if tecla_pulsada[K_DOWN]:
				pos_camara[1] -= 1
		else:
			pos_camara[0] = pj.pos[0]-(ANCHO_PANTALLA_GL/2-ANCHO_CADRO/2)
			pos_camara[1] = pj.pos[1]-(ALTO_PANTALLA_GL/2-ALTO_CADRO)

			pos_camara[0] = max(pos_camara[0], 0)
			pos_camara[0] = min(pos_camara[0], ANCHO_FASE-ANCHO_PANTALLA_GL)

			pos_camara[1] = max(pos_camara[1], 0)
			pos_camara[1] = min(pos_camara[1], ALTO_FASE-ALTO_PANTALLA_GL)


		#EVENTOS

		for evento in pygame.event.get():

			#TECLADO
			if evento.type == pygame.KEYDOWN:

				#CAMARA_LIBRE
				if evento.key == K_c:
					if camara_libre:
						camara_libre=False
					else:
						camara_libre=True

				#MOSTRAR_CADRICULA
				if evento.key == K_v:
					if mostrar_cadricula:
						mostrar_cadricula = False
					else:
						mostrar_cadricula = True

				#ESC - CERRAR  XOGO
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