# -*- coding: utf-8 -*-

from constantes import *

import ctypes
import os
import sys

if os.name == 'nt' and sys.getwindowsversion()[0] >= 6:
	ctypes.windll.user32.SetProcessDPIAware()

#VARIABLES

pos_camara = [0,0]

#INICIAR PYGAME

pygame.init()

#PANTALLA

ventana = pygame.display.set_mode(RESOLUCION,pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.HWSURFACE)

Superficie_tiles = pygame.Surface((ANCHO_XOGO,ALTO_XOGO), pygame.SRCALPHA|pygame.HWSURFACE).convert()

pygame.display.set_caption("Xogo_Plataformas")

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