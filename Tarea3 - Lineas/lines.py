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

def sort_dictionary(d):
  return sorted(d.items(), key=lambda x: x[1], reverse = True)
 
def hough_transform(im, umb, gradx, grady):
  gx = gradx.load()                                               # Se apuntan los pixeles a la imagen del gradiente en X
  gy = grady.load()                                               # Se apuntan los pixeles a la imagen del gradiente en Y

  pixels = []                                                     # Se crea un array en donde se almacenaran los pares de toda la imagen
  combination = {}                                                # Se crea un diccionario en donde se almacenaran los 
  angles = []                                                     # Se crea un array en donde se almacenaran los angulos encontrados
  w, h = im.size                                                  # Obtenermos las dimensiones de la imagen (width,height)

  for i in range(w):                                              # Se recorre por todo lo ancho de la imagen
    tmp = list()                                                  # Para guardar las parejas de (theta,rho) de cada pixel se crea una lista temporal
    for j in range(h):                                            # Se recorre por todo lo alto de la imagen
      x = gx[i, j][0]                                             # Se obtiene el gradiente horizontal de ese pixel
      y = gy[i, j][0]                                             # Se obtiene el gradiente vertical de ese pixel
      theta = 0.0                                                 # Se inicializa el valor de tetha en 0.0
      if abs(x) + abs(y) <= 0.0:
        theta = None                                              # Aqui no hay nada en ninguna direccion
      elif x == 0 and y == 255:
        theta = 90                                                # Tetha es igual a 90 (vertical)
      else:
        theta = math.degrees(abs(y/x))                            # Se obtiene el valor de theta segun la formula: abs(hor/ver) en grados
        #theta = atan(ver / hor)                                  # Se obtiene el valor de theta segun la formula: arctan(gy/gx)
      if theta is not None:
        rho = abs((i) * math.cos(theta) + (j) * math.sin(theta))  # Se hace el calculo de rho para ese pixel
        if not theta in angles:  angles.append(theta)
        if i > 0 and i < w-1 and j > 0 and j < h - 1:
          if (rho, theta) in combination:
            combination[(rho, theta)] += 1                        # Se aumenta la coincidencia en ese par
          else:                                                   # De no existir la Combinacion 
            combination[(rho, theta)] = 1                         # Se crea una coincidencia
        tmp.append((rho, theta))                                  # Se guarda en lista temporal
      else:                                                       # Si el angulo no existe,
        tmp.append((None, None))                                  # Se crea un par vacio
    pixels.append(tmp)

  # Ordenamos las frecuencias, las mas relevantes primero
  combination = sort_dictionary(combination)
  n = int(math.ceil(len(combination) * umb))
  frec = {}
  for i in range(n):
    (rho, theta) = combination[i][0]
    frec[(rho, theta)] = combination[1]

  pix = im.load()                                                 # Se recorre por todo lo ancho de la imagen
  for i in range(w):                                              # Se recorre por todo lo ancho de la imagen
    for j in range(h):                                            # Se recorre por todo lo alto de la imagen
      if i > 0 and j > 0 and i < w and j < h:                     # Se verifica que las variables estén entre el ancho y el alto
        rho, theta = pixels[i][j]                                 # Obtenemos el par (rho, theta) de ese pixel
        if (rho, theta) in frec:                                  # Si ese par se toma en cuenta, verificamos el tipo de linea que es   
          if theta == 0:                                          # Se verifica si es linea horizontal
            pix[i, j] = (255, 0, 0)                               # Se pinta el pixel a rojo 
          elif theta == 90:                                       # Si es vertical (90 grados)
            pix[i, j] = (0, 0, 255)                               # Se pinta el pixel a azul 
          else:                                                   # Si el par no se toma en cuenta 
            pix[i, j] = (0, 255, 0)                               # Se coloca el pixel que normalmente iria en esa posicion
  im.save('output/4. Lineas.png')
  return im

if __name__ == "__main__":

    pygame.init()                                                 # Se inicializa pygame para la creacion de la ventana de salida
    # Mascaras de convolucion utilizadas
    SobelX = [[-1,0,1],[-2,0,2],[-1,0,1]]
    SobelY = [[1,2,1],[0,0,0],[-1,-2,-1]]

    im = Image.open('input/input.png')                            # Se carga la imagen de entrada
    width, height = im.size                                       # Obtenermos las dimensiones de la imagen (width,height)
    screen = pygame.display.set_mode((width, height))             # Se ajusta el tamaño de la ventana a las medidas de la imagen
    pygame.display.set_caption('Lineas')                          # Le ponemos nombre a la ventana   

    grises = filters.gray_scale(im)
    grises.save('output/1. Gris.png')                             # Se guarda el primer paso (Escala de grises)
    normalizada = filters.normalizar(grises)
    normalizada.save('output/2. Normalizada.png')                 # Se guarda el segundo paso (Imagen Normalizada)
    binarizada = filters.binarizacion(normalizada)
    binarizada.save('output/3. Binarizada.png')                   # Se guarda el tercer paso (Imagen Binarizada)
 
    gradx = filters.convolucion2(binarizada, SobelX)              # Se obtienen las magnitudes del vector gradiente en X
    grady = filters.convolucion2(binarizada, SobelY)              # Se obtienen las magnitudes del vector gradiente en Y
    
    umbral = filters.umbral(binarizada)[2]                        # Se obtiene el valor del umbral de corte
    hough_transform(binarizada, umbral, gradx,grady)              # Se obtienen las líneas mediante el metodo de la Transformada de Hough

    img = pygame.image.load('output/4. Lineas.png')               # Se despliega la imagen en la ventana
    screen = pygame.display.get_surface() 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.blit(img, (0,0))     
        pygame.display.update()