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

def cadros_inferiores(sujeto,lista,cadrados_ancho,ancho_fase,alto_fase):
    lista_cadros = []
    if (sujeto.pos[0] > -ANCHO_CADRO and sujeto.pos[0] < ancho_fase+ANCHO_CADRO
        or
        sujeto.pos[1] > -ALTO_CADRO and sujeto.pos[1] < alto_fase+ALTO_CADRO):
        pos_cadro_sujeto = int(sujeto.pos[0]/ANCHO_CADRO), int(sujeto.pos[1]/ALTO_CADRO)
        num_cadro_sujeto = num(pos_cadro_sujeto,cadrados_ancho)
        num_a_mirar = [num_cadro_sujeto,num_cadro_sujeto-cadrados_ancho]
        if sujeto.pos[0] < pos_cadro_sujeto[0]*ANCHO_CADRO:
            num_a_mirar.append(num_cadro_sujeto-1)
            num_a_mirar.append(num_cadro_sujeto-cadrados_ancho-1)
        if sujeto.pos[0] > pos_cadro_sujeto[0]*ANCHO_CADRO:
            num_a_mirar.append(num_cadro_sujeto+1)
            num_a_mirar.append(num_cadro_sujeto-cadrados_ancho+1)
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
        return None


#### OPENGL ####

def init_gl():
    glViewport(MARCO_LATERAL/2,MARCO_VERTICAL/2,ANCHO_VENTANA-MARCO_LATERAL,ALTO_VENTANA-MARCO_VERTICAL)
    glClearColor(0,0,0,0)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    #glEnable(GL_LINE_SMOOTH)
    #glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)


def limpiar_ventana_gl(ancho_gl,alto_gl):
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,ancho_gl,0,alto_gl)
    glTranslatef(0-pos_camara[0],0-pos_camara[1],0)
    glMatrixMode(GL_MODELVIEW)

def debuxar_rect_gl(vertices,pos=False):
    glLoadIdentity()
    if pos:
        glTranslatef(pos[0], pos[1], 0)
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

def debuxar_pj(posicion):
    debuxar_rect_gl(
    [[-ANCHO_CADRO/2.0,-ALTO_CADRO],
     [ANCHO_CADRO/2.0,-ALTO_CADRO],
     [ANCHO_CADRO/2.0,ALTO_CADRO],
     [-ANCHO_CADRO/2.0,ALTO_CADRO]],
    [posicion[0]+ANCHO_CADRO/2.0,posicion[1]+ALTO_CADRO])

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

def crear_lista(id_lista,vertices,forma):
    glNewList(id_lista, GL_COMPILE) ### INICIO LISTA
    glLoadIdentity()
    if forma=="liña":
        debuxar_linha(vertices)
    elif forma=="rectangulo":
        debuxar_rect_gl(vertices)
    glEndList() ############################### FIN LISTA
