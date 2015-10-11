# -*- coding: utf-8 -*-

###LIBRERIAS NECESARIAS###
#pygame
#pyOpenGL

from __future__ import division

from modulos.constantes import *
from modulos.clases import *
from modulos.funcions import *

import ctypes
import os
import sys

if os.name == 'nt' and sys.getwindowsversion()[0] >= 6:
    ctypes.windll.user32.SetProcessDPIAware()

#VARIABLES

camara_libre = False
mostrar_cadricula = True

_fase_cargada = False

#FASES

lista_fases = [fase(0,50,35,"mapas/mapa_colisions.txt")]

num_fase = 0

#PERSONAJE

pj = personaxe(0,[20,120],1,objeto_fisico([0,0],0.06,[]))

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

    saltando = 10

    global _ON
    global _fase_cargada
    global camara_libre
    global mostrar_cadricula

    #INICIAR OPENGL

    init_gl()

    #CARGAR TEXTURAS

    #glBindTexture(GL_TEXTURE_2D,1)
    #cargar_imagen_textura("texturas/textura-02.png")

    #numero_texturas = 2

    #lista_texturas = []

    #for i in range(1,numero_texturas+1):
    #    lista_texturas.append(GLuint(i))

    #glGenTextures(numero_texturas,lista_texturas[0])

    #BUCLE XOGO
    #-----------------

    while _ON:

        reloj = pygame.time.Clock()

        #### CARGA DE FASE ####
        #######################

        if not _fase_cargada:

            fase_actual = lista_fases[num_fase]

            #VARIABLES

            cargar_fase(fase_actual)

            (NUM_CADROS_ANCHO_FASE,NUM_CADROS_ALTO_FASE,NUM_CADROS_TOTALES_FASE,lista_cadros_colision,
             ANCHO_FASE,ALTO_FASE,lista_vertices_cadros_colision,vertices_cadricula) = cargar_fase(fase_actual)

            #LISTAS DE OPENGL

                #CADROS_COLISION

            ID_LISTA_CADROS_COLISION = glGenLists(2)
            crear_lista(ID_LISTA_CADROS_COLISION,lista_vertices_cadros_colision,"rectangulo")

                #CADRICULA

            ID_LISTA_CADRICULA = glGenLists(1)
            glBindTexture(GL_TEXTURE_2D, 1)
            crear_lista(ID_LISTA_CADRICULA,vertices_cadricula,"liña")

            _fase_cargada = True

        #######################
        #######################

        #LIMPIAR VENTANA

        limpiar_ventana_gl()

        ############################################
        #DEBUXADO
        ############################################

        #DEBUXAR FONDO

        glColor4f(1, 1, 1, 1)
        glLoadIdentity()
        glBegin(GL_QUADS)
        glVertex2f(pos_camara[0],pos_camara[1])
        glVertex2f(ANCHO_PANTALLA_GL+pos_camara[0],pos_camara[1])
        glVertex2f(ANCHO_PANTALLA_GL+pos_camara[0],ALTO_PANTALLA_GL+pos_camara[1])
        glVertex2f(pos_camara[0],ALTO_PANTALLA_GL+pos_camara[1])
        glEnd()

        glColor4f(0.8,0.8,0.8,0.5)
        glLoadIdentity()
        glBegin(GL_QUADS)
        glVertex2f(0,0)
        glVertex2f(ANCHO_FASE,0)
        glVertex2f(ANCHO_FASE,ALTO_FASE)
        glVertex2f(0,ALTO_FASE)
        glEnd()

        #CADROS_COLISION

        glColor4f(0.4,0.7,0.2,0.7)

        glCallList(ID_LISTA_CADROS_COLISION)

        #glBindTexture(GL_TEXTURE_2D,False)

        #DEBUXAR PJ

        glColor4f(0, 0, 0.8, 1)
        debuxar_rect_gl(
            [(pj.pos[0],pj.pos[1]),
             (pj.pos[0]+ANCHO_CADRO,pj.pos[1]),
             (pj.pos[0]+ANCHO_CADRO,pj.pos[1]+ALTO_CADRO*2),
             (pj.pos[0],pj.pos[1]+ALTO_CADRO*2)]
        )

        #CADRICULA

        glColor4f(0.5, 0.5, 0.5, 0.5)

        if mostrar_cadricula:
            glCallList(ID_LISTA_CADRICULA)

        ###########################################
        #FISICA
        ###########################################

        l_cadros_inferiores = cadros_inferiores(pj,lista_cadros_colision,NUM_CADROS_ANCHO_FASE)
        distancia = distancia_sujeto_cadro(pj,l_cadros_inferiores)

        glColor4f(1,0,0,0.5)
        for i in l_cadros_inferiores:
            debuxar_rect_2(i[0]*ANCHO_CADRO,i[1]*ALTO_CADRO,i[2],i[3])

        if distancia <= 0 and pj.fisica.vel[1] < 0:
            pj.fisica.vel[1] = 0
            if abs(distancia) < ALTO_CADRO:
                pj.pos = [pj.pos[0],pj.pos[1]-distancia]
            pj_en_suelo = True
        else:
            pj.fisica.vel[1] -= pj.fisica.gravedad
            pj_en_suelo = False

        for impulso in pj.fisica.impulsos:
            pj.fisica.vel[0] += impulso[0]
            pj.fisica.vel[1] += impulso[1]
            impulso[2] -= 1

        for impulso in pj.fisica.impulsos:
            if impulso[2] <= 0:
                pj.fisica.impulsos.remove(impulso)

        pj.pos = pj.pos[0]+pj.fisica.vel[0],pj.pos[1]+pj.fisica.vel[1]

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


        ############################################
        #EVENTOS
        ############################################

        ###### TECLAS PULSADAS ######

        tecla_pulsada = pygame.key.get_pressed()

        if tecla_pulsada[K_d]:
            pj.fisica.vel[0] = 1

        if tecla_pulsada[K_a]:
            pj.fisica.vel[0] = -1

        if tecla_pulsada[K_d] and tecla_pulsada[K_a] or not(tecla_pulsada[K_d] or tecla_pulsada[K_a]):
            pj.fisica.vel[0] = 0

        if tecla_pulsada[K_w] and pj_en_suelo and not saltando:
            saltando = 10
            if len(pj.fisica.impulsos) == 0:
                pj.fisica.impulsos.append([0,0.4,5])

        saltando = max(0,saltando-1)

        ####### MOUSE ########

        pos_mouse = pygame.mouse.get_pos()

        if pos_mouse[0] >= MARCO_LATERAL/2 and pos_mouse[0] <= ANCHO_VENTANA-MARCO_LATERAL/2:
            pos_mouse_gl = [(pos_mouse[0]-MARCO_LATERAL/2)*ANCHO_PANTALLA_GL/(ANCHO_VENTANA-MARCO_LATERAL)+pos_camara[0],
                        ALTO_PANTALLA_GL-(pos_mouse[1]*ALTO_PANTALLA_GL/ALTO_VENTANA)+pos_camara[1]]
        else:
            pos_mouse_gl = False


        if pos_mouse_gl:
            glColor4f(1, 0, 0, 0.4)
            debuxar_linha([[pos_mouse_gl[0],pos_camara[1]],[pos_mouse_gl[0],ALTO_PANTALLA_GL+pos_camara[1]]])
            debuxar_linha([[pos_camara[0],pos_mouse_gl[1]],[ANCHO_PANTALLA_GL+pos_camara[0],pos_mouse_gl[1]]])
            if pos_mouse_gl[0] < 0:
                pos_mouse_gl[0]-= ANCHO_CADRO
            if pos_mouse_gl[1] < 0:
                pos_mouse_gl[1] -= ALTO_CADRO
            debuxar_rect_gl(
                [[int(pos_mouse_gl[0]/ANCHO_CADRO)*ANCHO_CADRO,int(pos_mouse_gl[1]/ALTO_CADRO)*ALTO_CADRO],
                [int(pos_mouse_gl[0]/ANCHO_CADRO)*ANCHO_CADRO+ANCHO_CADRO,int(pos_mouse_gl[1]/ALTO_CADRO)*ALTO_CADRO],
                [int(pos_mouse_gl[0]/ANCHO_CADRO)*ANCHO_CADRO+ANCHO_CADRO,int(pos_mouse_gl[1]/ALTO_CADRO)*ALTO_CADRO+ALTO_CADRO],
                [int(pos_mouse_gl[0]/ANCHO_CADRO)*ANCHO_CADRO,int(pos_mouse_gl[1]/ALTO_CADRO)*ALTO_CADRO+ALTO_CADRO]])


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