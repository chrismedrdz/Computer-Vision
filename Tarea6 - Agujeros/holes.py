#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import sys
import os
import Image, ImageDraw, ImageFont
import random
import pygame
import numpy as np
import filters

# LISTADO DE COLORES
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
MAGENTA = (255,0,255)
YELLOW = (255,255,0)
CYAN = (0,255,255)
ORANGE = (255,128,0)
PURPLE = (76,0,173)

COLORS = [RED,GREEN,BLUE,MAGENTA,YELLOW,CYAN,ORANGE,PURPLE]
size = 20 # Tamaño del agujero que se va a pintar

def obtener_agujeros(vector, type = 1):
  pos = []
  maximo = max(vector)
  minimo = min(vector)
  umbral = (maximo + minimo)/2
  for i in range(1, len(vector) - 1):
    if type == 1:
      if (vector[i] > vector[i-1]) and (vector[i] > vector[i+1]):
        pos.append(i)
        if vector[i] > umbral: pos.append(i)
  
    elif type == 0:
      if (vector[i] < vector[i-1]) and (vector[i] < vector[i+1]): 
        pos.append(i)
        if vector[i] > umbral: pos.append(i)
  return pos

def get_histogram(im, orientation = 1):
  tmp = im.copy()
  pix = np.array(tmp.convert('L'))
  if orientation == 1:
    return [sum(x) for x in zip(*pix)]
  else:
    return [sum(x) for x in pix]

def verify_area(im, (x1, y1), (x2, y2)):
  w, h = im.size
  pix = im.load()
  area = abs(x2 - x1) * abs(y2 - y1)
  cont = 0
  i, j = (None, None)
  for x in range(x1, x2):
    for y in range(y1, y2):
      if x > 0 and x < w  and y > 0 and y < h:
        if pix[x, y] == (0, 0, 0):
          i, j = x, y
          cont += 1
  if cont > area * 0.2:
    return True, (i, j)
  else:
    return False, (i, j)

def dibujar_agujeros(bw, ver, hor):
  w, h = bw.size
  im = Image.open('input/hole.jpg').convert('RGB')
  draw = ImageDraw.Draw(im)
  pix = im.load()
  id = 1
  total = w*h
  areas = []
  for j in hor:
    for i in ver:
      (x1, y1), (x2, y2) = (i-(size/2), j-(size/2)), (i+(size/2), j+(size/2))
      confirm, begin = verify_area(bw, (x1, y1), (x2, y2))
      if confirm:
        if begin is not (None, None):
          n, coords = filters.bfs_origen(bw, begin, (255, 0, 0)) # Se aplica un BFS a los pixeles que corresponden al agujero
          sums = [sum(x) for x in zip(*coords)]
          center = (sums[0] / len(coords), sums[1] / len(coords))  # Se obtiene el centriode del agujero
          pix[center] = (255, 255, 0)
          areas.append(n)   # Se agrupa el area del agujero
          color = random.choice(COLORS)

          draw.ellipse(((center[0]-size/2, center[1]-size/2), (center[0]+size/2, center[1]+size/2)), outline = color, fill = color)
          draw.text(center, "%s"%id, fill = (0, 0, 0))
          id += 1
          
  for i in range(len(areas)):
    print "Agujero Encontrado ID: %s - Porcentaje Area: %0.2f%%"%(i, 100.0*(areas[i]/float(total)))
  im.save('output/Holes.png', 'PNG')  

def smooth(x,window_len=11,window='hanning'):
  s=np.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
  w=eval('np.'+window+'(window_len)')
  y=np.convolve(w/w.sum(), s, mode='valid')
  return y

if __name__ == "__main__":

  pygame.init() # Se inicializa pygame para la creacion de la ventana de salida

  im = Image.open('input/hole.jpg').convert('RGB') # Se carga la imagen de entrada y se convierte a RGB
  width, height = im.size
  screen = pygame.display.set_mode((width, height)) # Se ajusta el tamaño de la ventana a las medidas de la imagen
  pygame.display.set_caption('Agujeros') # Le ponemos nombre a la ventana   

  umbral = 90 # Umbral para la binarizacion de la imagen
  im = filters.binarizacion(im)

  vertical = get_histogram(im, 1)
  horizontal = get_histogram(im, 0)

  horizontal = list(smooth(np.array(horizontal)))
  vertical = list(smooth(np.array(vertical)))

  dibujar_agujeros(im, obtener_agujeros(vertical, type = 0), obtener_agujeros(horizontal, type = 0))

  img = pygame.image.load('output/Holes.png') # Se despliega la imagen en la ventana
  screen = pygame.display.get_surface() 

  while True:
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              sys.exit()
      screen.blit(img, (0,0))     
      pygame.display.update()