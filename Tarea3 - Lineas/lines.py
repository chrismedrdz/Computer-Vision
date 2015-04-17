#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Librerias
import Image
import math
from math import *
import time
import sys,pygame
import ImageDraw
import numpy
import filters

def main():
    #Marcaras de Gradiente Diferencial utilizadas
    SobelX = [[-1,0,1],[-2,0,2],[-1,0,1]]
    SobelY = [[1,2,1],[0,0,0],[-1,-2,-1]]

    PrewittX = [[-1,0,1],[-1,0,1],[-1,0,1]]
    PrewittY = [[1,1,1],[0,0,0],[-1,-1,-1]]

    pygame.init() # Se inicializa pygame para la creacion de la ventana de salida
    im = Image.open('input/input.png') # Se carga la imagen de entrada
    inicio = time.time() # Se inicia el contador de tiempo

    width, height = im.size
    screen = pygame.display.set_mode((width, height)) # Se ajusta el tamaño de la ventana a las medidas de la imagen
    pygame.display.set_caption('Lineas') # Le ponemos nombre a la ventana

    grises = filters.gray_scale(im)
    grises.save('output/1. Gris.png') # Se guarda el primer paso (Escala de grises)
    
    normalizada = filters.normalizar(grises)
    normalizada.save('output/2. Normalizada.png') # Se guarda el segundo paso (Imagen binarizada)

    #image = filters.imageToPixels(normalizada)    
    image = filters.imageToPixels(im)
    pixels = image["pixels"]
    w, h = image["size"][0], image["size"][1]

    print ' Alto: ',h
    print ' Ancho: ',w

    original = filters.slicing(pixels, w)     # Se guardan los pixeles originales para utilizarlos en la imagen final

    gx = filters.convolution(image, SobelY)  # Se aplica mascara Sobel en X y se obtienen los valores gx para de pixel
    gy = filters.convolution(image, SobelY)  # Se aplica mascara Sobel en Y y se obtienen los valores gy para de pixel


    mag = filters.normalize(filters.euclidean(gx, gy)) # Se obtienen las magnitudes del vector gradiente de cada pixel
    
    resultado = list()

    results = [[(None,None) for x in range(w)] for y in range(h)] 
    # Se crea una lista y se inicializa a (None,None)

    pares = dict()   
    cont = 0

    histo = dict()

    # Se obtienen los angulos de cada pixel
    for y in xrange(h): # Se recorre cada fila de la imagen
        datos = list() # Para guardar las parejas de (theta,rho) de cada pixel
        for x in xrange(w): # Se recorre cada columna de la imagen
            hor = gx[y][x][1] # Se obtiene el gradiente horizontal de ese pixel
            ver = gy[y][x][1] # Se obtiene el gradiente vetical de ese pixel
            #magnitud = mag[y][x] # Se obtiene la magnitud del vector gradiente de ese pixel
            if fabs(hor) > 0.00001:
                #theta = atan(ver / hor) # Se obtiene el valor de theta segun la formula: arctan(gy/gx)
                theta = atan2(ver,hor) # Se obtiene el valor de theta segun la formula: arctan(gy/gx)
                # Se utliza la funcion atan2 para obtener mas flexibilidad al momento de tratar valores negativos y divisiones entre cero.
            else:
                if fabs(hor) + fabs(ver) < 0.00001:
                    theta = None # aqui no hay nada en ninguna direccion
                elif fabs(ver - hor) < 0.00001: # casi iguales
                    theta = atan2(1.0)
                elif hor * ver > 0.0: # mismo signo
                    theta = pi 
                else: # negativo -> -pi
                    theta = 0.0
            
            if theta is not None:
                # Nos aseguramos de que este entre 0 y PI (0 y 180) 
                while theta < 0.00001:
                    theta += pi
                while theta > pi:
                    theta -= pi

                rho = (x - w/2) * cos(theta) + (h/2 - y) * sin(theta) # Se hace el calculo de rho para ese pixel
                # Para aplicar la transformada de Hough es necesario discretizar el espacio de parametros en celdad de acomulacion
                theta = int(degrees(theta))/18   # Se discretizan los angulos 
                par = ("%d"%(theta), "%d"%rho)
                #print 'theta: ',theta,', rho: ',rho

                datos.append(par)  # Se almacenan pares de (theta y rho)
                results[y][x] = par

                if x > 0 and y > 0 and x < w-1 and y < h-1:  # Se descartan los bordes debido al ruido que meten
                    if par in histo:                         # Verificamos si existe el par (theta, rho)
                        histo[par] += 1                      # Se aumenta la coincidencia en ese par
                    else:                                    # De no existir la Combinacion               
                        histo[par] = 1                       # Se crea una coincidencia

            else:
                datos.append((None, None)) # Si el angulo no existe, se crea un par vacio
                results[y][x] = (None, None)

        resultado.append(datos)


        # Ordenamos las frecuencias, las mas relevantes primero
        frec = filters.frecuentes(histo, int(ceil(len(histo) * 2.5))) # Cantidad de pares de valores (theta, rho) a utilizar

        new_image = list()   # Se iran almacenando los nuevos pixeles para crear una nueva imagen con las lineas detectadas

        
        for y in xrange(h):
            renglon = list()                      
            for x in xrange(w):
                (ang, rho) = results[y][x]                    # Obtenemos el par (theta, rho) de ese pixel
                #print 'Angulo: ',ang
                if(ang, rho) in frec:                         # Si ese par se toma en cuenta, verificamos el tipo de linea que es                           
                    if(ang == -10 or ang == 0 or ang == 10):  # Se verifica si es linea horizontal
                        renglon.append((255,0,0))             # Se pinta el pixel a rojo 
                    elif(ang == -5 or ang == 5):              # Si es vertical
                        renglon.append((0,0,255))             # Se pinta el pixel a azul 
                    else:                                     # Si no es vertidcal u horizontal se asume que es una diagonal
                        renglon.append((0,255,0))             # Se pinta el pixel a verde 
                else:                                         # Si el par no se toma en cuenta 
                    renglon.append(original[y][x])            # Se coloca el pixel que normalmente iria en esa posicion
                    #renglon.append((255,255,255))            # Se coloca el pixel que normalmente iria en esa posicion
            new_image.append(renglon)
 
    nueva = Image.new("RGB", (w,h))

    for y in range(h):  # Se recorre la imagen por todo lo ancho
        for x in range(w): # Se recorre la imagen por todo lo alto
            nueva.putpixel((x, y), new_image[y][x])

    nueva.save("output/3. Lineas.png") # Se guarda la imagen con mascaras aplicadas en X y Y

    img = pygame.image.load('output/3. Lineas.png') # Se despliega la imagen en la ventana
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