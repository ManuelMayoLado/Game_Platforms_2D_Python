# -*- coding: utf-8 -*-

###LIBRERIAS NECESARIAS###
#pygame
#pyOpenGL

from __future__ import division

from modulos.clases import *
from modulos.funcions import *

from pygame.locals import *

import ctypes
import os
import sys

if os.name == 'nt' and sys.getwindowsversion()[0] >= 6:
    ctypes.windll.user32.SetProcessDPIAware()

#VARIABLES

camara_libre = True
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

    global _ON
    global _fase_cargada
    global camara_libre
    global mostrar_cadricula
    global ANCHO_PANTALLA_GL
    global ALTO_PANTALLA_GL

    #INICIAR OPENGL

    init_gl()

    #CARGAR TEXTURAS

    glGenTextures(2,[1,2])

    glBindTexture(GL_TEXTURE_2D,1)
    cargar_imagen_textura("texturas/textura-02.png")

    glBindTexture(GL_TEXTURE_2D,2)
    cargar_imagen_textura("texturas/ceo-01.png")

    #glDeleteTextures([1,2])


    #BUCLE XOGO
    #-----------------

    ''''''
    rect1 = rectangulo(60,65,10,10)
    cont_col = 0

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

            ID_LISTA_CADROS_COLISION = glGenLists(1)
            crear_lista(ID_LISTA_CADROS_COLISION,lista_vertices_cadros_colision,"rectangulo")

                #CADRICULA

            ID_LISTA_CADRICULA = glGenLists(1)
            glBindTexture(GL_TEXTURE_2D, 1)
            crear_lista(ID_LISTA_CADRICULA,vertices_cadricula,"liña")

            _fase_cargada = True

        #######################
        #######################

        #LIMPIAR VENTANA

        limpiar_ventana_gl(ANCHO_PANTALLA_GL,ALTO_PANTALLA_GL)

        glBindTexture(GL_TEXTURE_2D,0)

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
        glBindTexture(GL_TEXTURE_2D,2)
        glBegin(GL_QUADS)
        glTexCoord2f(0,0)
        glVertex2f(0,0)
        glTexCoord2f(1,0)
        glVertex2f(ANCHO_FASE,0)
        glTexCoord2f(1,1)
        glVertex2f(ANCHO_FASE,ALTO_FASE)
        glTexCoord2f(0,1)
        glVertex2f(0,ALTO_FASE)
        glEnd()

        #CADROS_COLISION
        glColor4f(0.8,0.8,0.8,1)
        glBindTexture(GL_TEXTURE_2D,1)
        glCallList(ID_LISTA_CADROS_COLISION)

        #QUITAR TEXTURAS
        glBindTexture(GL_TEXTURE_2D,0)

        #DEBUXAR PJ
        glColor4f(0.9, 0.7, 0, 0.8)
        debuxar_pj(pj.pos)

        #CADRICULA
        glColor4f(0.5, 0.5, 0.5, 0.5)
        if mostrar_cadricula:
            glCallList(ID_LISTA_CADRICULA)

        ''' PROBA '''

        glColor4f(1, 0.5, 1, 0.5)
        debuxar_rect_gl2(rect1)

        rect_pj = rectangulo(pj.pos[0],pj.pos[1],ANCHO_CADRO,ALTO_CADRO*2)

        if colision_rect(rect_pj,rect1):
            print 'COLISIONANDO',cont_col
            cont_col += 1


        ###########################################
        #FISICA
        ###########################################

        l_cadros_inferiores = cadros_inferiores(pj,lista_cadros_colision,NUM_CADROS_ANCHO_FASE,ANCHO_FASE,ALTO_FASE)
        distancia = distancia_sujeto_cadro(pj,l_cadros_inferiores)

        #DEBUXAR CADROS PARA CALCULAR COLISION
        glColor4f(1, 0, 0, 0.3)
        glLoadIdentity()
        glBegin(GL_QUADS)
        for c in l_cadros_inferiores:
            glVertex2f(c[0]*ANCHO_CADRO,c[1]*ALTO_CADRO)
            glVertex2f(c[0]*ANCHO_CADRO+c[2],c[1]*ALTO_CADRO)
            glVertex2f(c[0]*ANCHO_CADRO+c[2],c[1]*ALTO_CADRO+c[3])
            glVertex2f(c[0]*ANCHO_CADRO,c[1]*ALTO_CADRO+c[3])
        glEnd()

        if distancia:
            if distancia <= 0 and pj.fisica.vel[1] <= 0:
                pj.fisica.vel[1] = 0
                if ALTO_CADRO > abs(distancia) > 0.2:
                    pj.pos = [pj.pos[0],pj.pos[1]-distancia]
                pj_en_suelo = True
            else:
                pj.fisica.vel[1] -= pj.fisica.gravedad
                pj_en_suelo = False
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


        pj.pos[0] = pj.pos[0]+pj.fisica.vel[0]
        pj.pos[1] = pj.pos[1] + pj.fisica.vel[1]

        ############################################
        #EVENTOS
        ############################################

        ###### TECLAS PULSADAS ######

        tecla_pulsada = pygame.key.get_pressed()

        if tecla_pulsada[K_d]:
            pj.fisica.vel[0] = 0.5

        if tecla_pulsada[K_a]:
            pj.fisica.vel[0] = -0.5

        if tecla_pulsada[K_d] and tecla_pulsada[K_a] or not(tecla_pulsada[K_d] or tecla_pulsada[K_a]):
            pj.fisica.vel[0] = 0

        if tecla_pulsada[K_w] and pj_en_suelo:
            if len(pj.fisica.impulsos) == 0:
                pj.fisica.impulsos.append([0,0.4,5])


        ####### MOUSE ########

        pos_mouse = pygame.mouse.get_pos()

        if (MARCO_LATERAL/2 <= pos_mouse[0] <= ANCHO_VENTANA-MARCO_LATERAL/2
            and MARCO_VERTICAL / 2 <= pos_mouse[1] <= ALTO_VENTANA - MARCO_VERTICAL / 2):
            pos_mouse_gl = [
                (pos_mouse[0]-MARCO_LATERAL/2)*ANCHO_PANTALLA_GL/(ANCHO_VENTANA-MARCO_LATERAL)+pos_camara[0],
                ALTO_PANTALLA_GL-(
                    (pos_mouse[1]-MARCO_VERTICAL/2)*ALTO_PANTALLA_GL/(ALTO_VENTANA-MARCO_VERTICAL))+pos_camara[1]]
        else:
            pos_mouse_gl = False

        if pos_mouse_gl:
            glColor4f(1, 0, 0, 0.3)
            if pos_mouse_gl[0] < 0:
                pos_mouse_gl[0]-= ANCHO_CADRO
            if pos_mouse_gl[1] < 0:
                pos_mouse_gl[1] -= ALTO_CADRO
            if 0 <= pos_mouse_gl[0] <= ANCHO_FASE and 0 <= pos_mouse_gl[1] <= ALTO_FASE:
                debuxar_rect_gl(
                    [[int(pos_mouse_gl[0]/ANCHO_CADRO)*ANCHO_CADRO,int(pos_mouse_gl[1]/ALTO_CADRO)*ALTO_CADRO],
                    [int(pos_mouse_gl[0]/ANCHO_CADRO)*ANCHO_CADRO+ANCHO_CADRO,int(pos_mouse_gl[1]/ALTO_CADRO)*ALTO_CADRO],
                    [int(pos_mouse_gl[0]/ANCHO_CADRO)*ANCHO_CADRO+ANCHO_CADRO,int(pos_mouse_gl[1]/ALTO_CADRO)*ALTO_CADRO+ALTO_CADRO],
                    [int(pos_mouse_gl[0]/ANCHO_CADRO)*ANCHO_CADRO,int(pos_mouse_gl[1]/ALTO_CADRO)*ALTO_CADRO+ALTO_CADRO]])


        #EVENTOS

        for evento in pygame.event.get():

            #MOUSE
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 4:
                    ANCHO_PANTALLA_GL -= 3
                    if camara_libre:
                        pos_camara[0] += 1.5
                elif evento.button == 5:
                    ANCHO_PANTALLA_GL += 3
                    if camara_libre:
                        pos_camara[0] -= 1.5
                if evento.button in [4,5]:
                    ALTO_PANTALLA_GL = ANCHO_PANTALLA_GL / DIF_ASP

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

        pygame.display.flip()

        reloj.tick(FPS)

if __name__ == '__main__':
    main()