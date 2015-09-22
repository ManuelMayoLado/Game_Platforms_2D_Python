#CLASES

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
