#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import sys
import os
import Image, ImageDraw, ImageFont
import random
import filters
import pygame

circulo = 0

# COLORES PRIMARIOS
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
MAGENTA = (255,0,255)
YELLOW = (255,255,0)
CYAN = (0,255,255)

COLORS = [RED,GREEN,BLUE,MAGENTA,YELLOW,CYAN]

def paint_circles(im, coords, radius):
  umbral = 2
  global circulo
  borders = Image.open('output/4. Mascara.png') # Abrir imagen de bordes detectados
  grad = borders.load()
  w, h = im.size
  pix = im.load()
  draw = ImageDraw.Draw(im)
  D = filters.distance((0, 0), (w, h))
  for x, y in coords:
    rg = 255
    v1, v2, v3, v4 = False, False, False, False

    for k in range(-umbral, umbral):
      curr_radius = radius + k

      if x + curr_radius < w and x + curr_radius > 0 and x - curr_radius < w and  x - curr_radius > 0:
        if grad[x + curr_radius, y] != (0, 0, 0):
          v1 = True
        if grad[x - curr_radius, y] != (0, 0, 0):
          v2 = True
      if y + curr_radius < h and y + curr_radius > 0 and y - curr_radius < h and  y - curr_radius > 0:
        if grad[x, y + curr_radius] != (0, 0, 0):
          v3 = True
        if grad[x, y - curr_radius] != (0, 0, 0):
          v4 = True

        if v1 and v2 and v3 and v4:
          #color = random.randint(0,255),random.randint(0,255),random.randint(0,255) # Se genera un color aleatorio
          color = random.choice(COLORS)
          pix[x, y] = (color) 
          draw.text((x, y), '%s'%(circulo+1), (color))
          d = 2.0 * radius
          print "Circulo #: %s Radio: %s  Diametro: %.01f "%(circulo+1, radius, d)
          circulo += 1
          
          draw.ellipse((x-radius, y-radius, x+radius, y+radius), outline = (color))
          break
  im.save('output/5. Circulos.png', 'PNG')


def group_votes(frec, (w, h)):
    dim = max(w, h)
    for padding in range (1, int(round(dim*0.1))):
        c = True
        while c:
            c = False
            for i in range(w):
                for j in range(h):
                    v = frec[i][j]
                    if v > 0:
                        for n in range(-padding, padding):
                            for m in range(-padding, padding):
                                if not (n == 0 and m == 0):
                                    if i + m >= 0 and i + m < w and j + n >= 0 and j + n < h:
                                        v2 = frec[i + m][j + n]
                                        if v2 > 0:
                                            if v - padding >= v2:
                                                frec[i][j] = v + v2 
                                                frec[i + m][j + n] = 0
                                                c = True
    return frec

def find_centers(im, radius, gradx, grady):
  w, h = im.size
  Gx = gradx.load()
  Gy = grady.load()
  frec = filters.zeros(w, h)
  pix = im.load()

  for i in range(w):
    for j in range(h):
      if Gy[i, j] != (0, 0, 0) or Gx[i, j] != (0, 0, 0):
        r, g, b = Gx[i, j]
        gx = (r+g+b)/3
        r, g, b = Gy[i, j]
        gy = (r+g+b)/3
        g = math.sqrt(gx ** 2 + gy ** 2)

        if abs(g) > 0:
          theta = math.atan2(gy , gx)
          xc = int(round(i - radius * math.cos(theta+math.radians(90.0))))
          yc = int(round(j - radius * math.sin(theta+math.radians(90.0))))
          if xc >= 0 and xc < w and yc >= 0 and yc < h:
              frec[xc][yc] += 1
  frec = group_votes(frec, (w, h))
  max_ = 0
  suma = 0.0
  for x in xrange(w):
    for y in xrange(h):
      v = frec[x][y]
      suma += v
      if v > max_:
        max_ = v
  promedio = suma / (w * h)
  umbral = (max_ + promedio) / 2.0
  coords = []
  for x in xrange(w):
    for y in xrange(h):
      v = frec[x][y]
      if v > umbral:
        coords.append((x, y))
  return coords

def circle_detection(im, radius, gradx, grady):
  conv = filters.convolucion2(im, juntas)  
  conv.save("output/4. Mascara.png", "png")
  coords = find_centers(im, radius, gradx, grady) #encontrar coordenadas del circulo y sus centros
  paint_circles(im, coords, radius)


if __name__ == "__main__":

    pygame.init() # Se inicializa pygame para la creacion de la ventana de salida
    
    # Mascaras de convolucion utilizadas
    SobelX = [[-1,0,1],[-2,0,2],[-1,0,1]]
    SobelY = [[1,2,1],[0,0,0],[-1,-2,-1]]

    juntas = [[0, 2, 2], [-2, 0, 2], [-2, -2, 0]]

    im = Image.open('input/input.png') # Se carga la imagen de entrada
    width, height = im.size
    screen = pygame.display.set_mode((width, height)) # Se ajusta el tamaño de la ventana a las medidas de la imagen
    pygame.display.set_caption('Circulos') # Le ponemos nombre a la ventana   

    grises = filters.gray_scale(im)
    grises.save('output/1. Gris.png') # Se guarda el primer paso (Escala de grises)
    normalizada,umbral = filters.normalizar(grises)
    normalizada.save('output/2. Normalizada.png') # Se guarda el segundo paso (Imagen Normalizada)
    binarizada = filters.binarizacion(normalizada)
    binarizada.save('output/3. Binarizada.png') # Se guarda el segundo paso (Imagen Normalizada)
 
    gradx = filters.convolucion2(binarizada, SobelX)
    grady = filters.convolucion2(binarizada, SobelY)
    
    posibles_radios = [25,49]

    for r in posibles_radios:
    #for r in xrange(50,53):  
        circle_detection(binarizada, r, gradx, grady)

    img = pygame.image.load('output/5. Circulos.png') # Se despliega la imagen en la ventana
    screen = pygame.display.get_surface() 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.blit(img, (0,0))     
        pygame.display.update()