#FUNCIONS

def cargar_lista_cadros_colision(archivo,lista):
    text = open(archivo,"r").read()
    cont = 0
    for i in text:
        lista[cont] = int(i)
        cont += 1
    return lista