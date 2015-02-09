#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Librerias
import Image
import math
from math import *
import time
import sys,pygame
import ImageDraw

#Marcaras de Gradiente Diferencial utilizadas
SobelX = [[-1,0,1],[-2,0,2],[-1,0,1]]
SobelY = [[1,2,1],[0,0,0],[-1,-2,-1]]

PrewittX = [[-1,0,1],[-1,0,1],[-1,0,1]]
PrewittY = [[1,1,1],[0,0,0],[-1,-1,-1]]

def gray_scale(im): #Rutina que convierte la imagen a escala de grises
    imagen_grises = im.copy() # Se hace una copia de la imagen original
    width, height = im.size # Obtenermos el tamaño de la imagen
    img = imagen_grises.convert('RGB') # Convertimos la imagen a RGB

    pixeles = imagen_grises.load() # Cargamos los pixeles de la imagen
    for i in range(width): # Se recorrre la imagen a lo ancho
        for j in range(height): # Se recorre la imagen a lo alto
            prom = sum(pixeles[i,j])/3 # Se calcula el promedio
            pixeles[i,j] = (prom,prom,prom) # Se agrega el nuevo valor al arreglo de pixeles
    
    return imagen_grises

def normalizar(norm):
    w,h = norm.size # Obtenermos el tamaño de la imagen
    pixeles = norm.load() # Cargamos los pixeles de la imagen
    lista_pixeles = [] # Lista que almacenara los nuevos pixeles de la nueva imagen normalizada
    for j in range(h): #Se recorre la imagen por todo lo alto
        for i in range(w): #Se recorre la imagen por todo lo ancho
            pix = pixeles[i,j][1]
            lista_pixeles.append(pix) # Se almacena el pixel en la lista de pixeles
    maximo = max(lista_pixeles) # Se obtiene el umbral mas alto de toda la lista de pixeles
    minimo = min(lista_pixeles) # Se obtiene el umbral mas bajo de toda la lista de pixeles
    l = 255.0/(maximo-minimo)  # Se calcula el valor del umbral de corte para identificar las magnitudes más fuertes

    for j in range(h):
        for i in range(w):
            pix = pixeles[i,j][1] #Se obtiene el pixel
            nuevo = int(floor((pix-minimo)*l)) # Nuevo pixel normalizado
            pixeles[i,j] = ((nuevo,nuevo,nuevo)) # Se almacena

    return norm

def convolucion(imagen, mascarax, mascaray): #Metodo de convolucion discreta para 2D
    width, height = imagen.size
    x, y = imagen.size 
    pixel = imagen.load()
    
    new_image = Image.new("RGB", (width,height))
    draw = ImageDraw.Draw(new_image)

    for i in range(width):  #Se recorre la imagen por todo lo ancho
        for j in range(height): # Se recorre la imagen por todo lo alto
            sumx=0.0 # Inicializamos la sumatoria de X en cero 
            sumy = 0.0 # Inicializamos la sumatoria de Y en cero 
            for m in range(len(mascarax[0])): # Recorremos la mascara en X a lo alto
                for h in range(len(mascaray[0])):# Recorremos la mascara en Y a lo alto
                    try:
                        mul_x= mascarax[m][h] * pixel[i+m, j+h][0]
                        mul_y= mascaray[m][h] * pixel[i+m, j+h][0]
                    except:
                        mul_x=0
                        mul_y=0
                    sumx+=mul_x # Se realiza la sumatoria de los valores en X
                    sumy+=mul_y # Se realiza la sumatoria de los valores en Y
            valorx = pow(sumx,2)
            valory = pow(sumy,2)
            grad = int(math.sqrt(valorx + valory)) # Se calcula el gradiente en RGB
            if grad <= 0:
                grad = 0
            elif grad >= 255:
                grad = 255
            pixel[i,j] = (grad, grad, grad) # Agregamos el nuevo valor al arreglo de la gradiente
            new_image.putpixel((i, j), (grad, grad, grad))
            #draw.point((i,j), 'red')
          
    return new_image

def main():
    pygame.init() # Se inicializa pygame para la creacion de la ventana de salida
    im = Image.open('input/imagen.jpg') # Se carga la imagen de entrada
    inicio = time.time() # Se inicia el contador de tiempo

    width, height = im.size
    screen = pygame.display.set_mode((width, height)) # Se ajusta el tamaño de la ventana a las medidas de la imagen
    pygame.display.set_caption('Bordes') # Le ponemos nombre a la ventana

    grises = gray_scale(im)
    grises.save('output/1. Gris.png') # Se guarda el primer paso (Escala de grises)
    normalizada = normalizar(grises)
    normalizada.save('output/2. Normalizada.png') # Se guarda el segundo paso (Imagen binarizada)
    nueva = convolucion(normalizada, SobelX, SobelY)
    nueva.save("output/3. Final.png") # Se guarda el ultimo paso (Mascara en imagen)
    img = pygame.image.load('output/3. Final.png') # Se despliega la imagen en la ventana
    screen = pygame.display.get_surface() 

    #Se calcula el tiempo de procesamiento
    fin = time.time()
    tiempo = fin - inicio
    print "Tiempo transcurrido -> " + str(tiempo) + " segundos"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.blit(img, (0,0))     
        pygame.display.update()

if __name__ == '__main__':
    main()