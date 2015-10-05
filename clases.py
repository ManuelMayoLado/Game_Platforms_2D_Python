#CLASES

from constantes import *

class fase:
    def __init__(self,num,cadros_ancho,cadros_alto,doc_col):
        self.num = num
        self.cadros_ancho = cadros_ancho
        self.cadros_alto = cadros_alto
        self.doc_col = doc_col
        self.ancho = cadros_ancho * ANCHO_CADRO
        self.alto = cadros_alto * ALTO_CADRO

class objeto_fisico:
    def __init__(self,vel,gravedad,impulso):
        self.vel = vel
        self.gravedad = gravedad
        self.impulso = impulso

class personaxe:
    def __init__(self,imagen,pos,estado,fisica):
        self.imagen = imagen
        self.pos = pos
        self.estado = estado
        self.fisica = fisica
