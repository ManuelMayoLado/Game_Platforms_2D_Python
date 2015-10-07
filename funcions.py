# -*- coding: utf-8 -*-

#### FUNCIONS ####

from OpenGL.GL import *
from OpenGL.GLU import *

from constantes import *

def pos(n, num_cadros_ancho_fase):
	return [n % num_cadros_ancho_fase, n / num_cadros_ancho_fase]

def num(p, num_cadros_ancho_fase):
	return p[0]+p[1]*num_cadros_ancho_fase

def cargar_lista_cadros_colision(archivo,lista):
    text = open(archivo,"r").read()
    cont = 0
    for i in text:
        lista[cont] = int(i)
        cont += 1
    return lista

#OPENGL

def init_gl():
    glViewport(MARCO_LATERAL/2,0,ANCHO_VENTANA-MARCO_LATERAL,ALTO_VENTANA)
    glClearColor(0,0,0,0)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    #glEnable(GL_LINE_SMOOTH)
    #glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)


def limpiar_ventana_gl():
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,DIMENSIONS_GL_ESTANDAR,0,DIMENSIONS_GL)
    glTranslatef(0-pos_camara[0],0-pos_camara[1],0)
    glMatrixMode(GL_MODELVIEW)

def debuxar_rect_gl(vertices):
    glLoadIdentity()
    glBegin(GL_QUADS)
    #glTranslatef(pos[0], pos[1], 0)
    for i in vertices:
        glVertex2f(i[0],i[1])
    glEnd()

def debuxar_linha(vertices):
    glLoadIdentity()
    glBegin(GL_LINES)
    for i in vertices:
        glVertex2f(i[0],i[1])
    glEnd()

def texturas():
    texturaSurface = pygame.image.load("textura-02.png").convert_alpha()
    texturaData = pygame.image.tostring(texturaSurface, "RGBA", True)
    textID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D,textID)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texturaSurface.get_width(), texturaSurface.get_height(), 0,
                            GL_RGBA, GL_UNSIGNED_BYTE, texturaData)
    return textID