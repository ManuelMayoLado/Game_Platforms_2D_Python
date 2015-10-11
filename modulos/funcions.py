# -*- coding: utf-8 -*-

#### FUNCIONS ####
##################

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

def cargar_fase(fase):
    lista_cadros_colision = []
    for i in range(fase.num_cadros):
        lista_cadros_colision.append(0)
    lista_cadros_colision = cargar_lista_cadros_colision(fase.doc_col,lista_cadros_colision)

    lista_vertices_cadros_colision = []
    for i in range(len(lista_cadros_colision)):
        if lista_cadros_colision[i]:
            pos_cadro = pos(i,fase.cadros_ancho)
            lista_vertices_cadros_colision.append(
                [pos_cadro[0]*ANCHO_CADRO,pos_cadro[1]*ALTO_CADRO])
            lista_vertices_cadros_colision.append(
                [pos_cadro[0]*ANCHO_CADRO+ANCHO_CADRO,pos_cadro[1]*ALTO_CADRO])
            lista_vertices_cadros_colision.append(
                [pos_cadro[0]*ANCHO_CADRO+ANCHO_CADRO,pos_cadro[1]*ALTO_CADRO+ALTO_CADRO])
            lista_vertices_cadros_colision.append(
                [pos_cadro[0]*ANCHO_CADRO,pos_cadro[1]*ALTO_CADRO+ALTO_CADRO])

    vertices_cadricula = []

    for i in range(fase.cadros_ancho+1):
        vertices_cadricula.append([i*ANCHO_CADRO,0])
        vertices_cadricula.append([i*ANCHO_CADRO,fase.alto])

    for i in range(fase.cadros_alto+1):
        vertices_cadricula.append([0,i*ALTO_CADRO])
        vertices_cadricula.append([fase.ancho,i*ALTO_CADRO])

    return fase.cadros_ancho,fase.cadros_alto,fase.num_cadros,lista_cadros_colision,fase.ancho,fase.alto,lista_vertices_cadros_colision,vertices_cadricula

#### COLISIÓNS ####

def cadros_inferiores(sujeto,lista,cadrados_ancho):
    pos_cadro_sujeto = int(sujeto.pos[0]/ANCHO_CADRO), int(sujeto.pos[1]/ALTO_CADRO)
    num_cadro_sujeto = num(pos_cadro_sujeto,cadrados_ancho)
    num_a_mirar = [num_cadro_sujeto,num_cadro_sujeto-cadrados_ancho]
    if not pos_cadro_sujeto[0] <= 0 and sujeto.pos < pos_cadro_sujeto[0]*ANCHO_CADRO:
        num_a_mirar.append(num_cadro_sujeto-1)
        num_a_mirar.append(num_cadro_sujeto-cadrados_ancho-1)
    if not pos_cadro_sujeto[0] >= cadrados_ancho-1 and sujeto.pos > pos_cadro_sujeto[0]*ANCHO_CADRO:
        num_a_mirar.append(num_cadro_sujeto+1)
        num_a_mirar.append(num_cadro_sujeto-cadrados_ancho+1)
    lista_cadros = []
    for n in num_a_mirar:
        try:
            if lista[n]:
                lista_cadros.append([pos(n,cadrados_ancho)[0],pos(n,cadrados_ancho)[1],ANCHO_CADRO,ALTO_CADRO])
        except:
            None

    return lista_cadros

def distancia_sujeto_cadro(sujeto,lista_cadros):
    conxunto_y = []
    if lista_cadros:
        for i in lista_cadros:
            conxunto_y.append(i[1])
        y = max(conxunto_y)
        distancia = sujeto.pos[1]-(y*ALTO_CADRO+ALTO_CADRO)
        return distancia
    else:
        return "nada"


#### OPENGL ####

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

def debuxar_rect_gl(vertices,id_text=False):
    glLoadIdentity()
    glBegin(GL_QUADS)
    for v in range(0,len(vertices),4):
        glTexCoord2f(0,0)
        glVertex2f(vertices[v][0],vertices[v][1])
        glTexCoord2f(1,0)
        glVertex2f(vertices[v+1][0],vertices[v+1][1])
        glTexCoord2f(1,1)
        glVertex2f(vertices[v+2][0],vertices[v+2][1])
        glTexCoord2f(0,1)
        glVertex2f(vertices[v+3][0],vertices[v+3][1])
    glEnd()

def debuxar_rect_2(x,y,ancho,alto):
    glLoadIdentity()
    glBegin(GL_QUADS)
    glVertex2f(x,y)
    glVertex2f(x+ancho,y)
    glVertex2f(x+ancho,y+alto)
    glVertex2f(x,y+alto)
    glEnd()

def debuxar_linha(vertices):
    glLoadIdentity()
    glBegin(GL_LINES)
    for v in vertices:
        glVertex2f(v[0],v[1])
    glEnd()

def cargar_imagen_textura(imagen):
    texturaSurface = pygame.image.load(imagen).convert_alpha()
    texturaData = pygame.image.tostring(texturaSurface, "RGBA", True)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texturaSurface.get_width(), texturaSurface.get_height(), 0,
                           GL_RGBA, GL_UNSIGNED_BYTE, texturaData)

def crear_lista(id_lista,vertices,forma,id_textura=False):
    glNewList(id_lista, GL_COMPILE) ### INICIO LISTA
    glLoadIdentity()
    if forma=="liña":
        debuxar_linha(vertices)
    elif forma=="rectangulo":
        if id_textura:
            debuxar_rect_gl(vertices,id_textura)
        else:
            debuxar_rect_gl(vertices)
    glEndList() ############################### FIN LISTA
