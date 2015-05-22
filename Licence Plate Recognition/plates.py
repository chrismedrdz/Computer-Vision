#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter
import math
import sys
import os
import Image, ImageDraw, ImageFont
import random
import pygame
import  cv2
from pygame import mouse
import numpy as np

from pytesser import *

import ProcessImage
import DetectRegion

# LISTADO DE COLORES
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
MAGENTA = (255,0,255)
YELLOW = (255,255,0)
CYAN = (0,255,255)
ORANGE = (255,128,0)
PURPLE = (76,0,173)
BLACK = (0,0,0)
GRAY = (238,233,233)
GRAY2 = (197,194,194)
GRAY3 = (44, 43, 43)
WHITE = (255,255,255)

pygame.init() # Se inicializa pygame para la creacion de la ventana de salida

#the default cursor
DEFAULT_CURSOR = mouse.get_cursor()

#the hand cursor
_HAND_CURSOR = (
"     XX         ",
"    X..X        ",
"    X..X        ",
"    X..X        ",
"    X..XXXXX    ",
"    X..X..X.XX  ",
" XX X..X..X.X.X ",
"X..XX.........X ",
"X...X.........X ",
" X.....X.X.X..X ",
"  X....X.X.X..X ",
"  X....X.X.X.X  ",
"   X...X.X.X.X  ",
"    X.......X   ",
"     X....X.X   ",
"     XXXXX XX   ")
_HCURS, _HMASK = pygame.cursors.compile(_HAND_CURSOR, ".", "X")
HAND_CURSOR = ((16, 16), (5, 1), _HCURS, _HMASK)

screen = pygame.display.get_surface() 

size = 440, 330 # Tamaño de la imagen a mostrar en GUI
CURRENT_IMAGE = 0
file_list = []

clock = pygame.time.Clock()

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def ProcessPlate(img):
  GrayScale = ProcessImage.GrayScalePlate(img)
  MiddleFilter=ProcessImage.MiddleFilterPlate(GrayScale)
  Difference=ProcessImage.DifferencePlate(GrayScale,MiddleFilter)
  #Convolution=ProcessImage.Convolution(Difference,SobelX,SobelY)
  #Thresholding=ProcessImage.Thresholding(Convolution)
  Binarization=ProcessImage.BinarizationPlate(GrayScale)

  return Difference

def detect_plate():
  global CURRENT_IMAGE

  image_path = 'input/'+file_list[CURRENT_IMAGE]
  img=Image.open(image_path) # Abrir la imagen

  print ' \n|| Imagen a Analizar: '+image_path+' || \n'

  '''
  En esta fase Procesamos la imagen del auto para aplicarle los filtros necesarios para poder
  trabajar con ella y facilitar el paso de detección de la región de la placa.
  '''
  # Mascaras de convolucion utilizadas
  SobelX = [[-1.0, 0.0, 1.0], [-2.0, 0.0, 2.0], [-1.0, 0.0, 1.0]]
  SobelY = [[1.0, 2.0, 1.0], [0.0, 0.0, 0.0], [-1.0, -2.0, -1.0]]

  print '>> Iniciando Procesamiento de Imagen'

  #PreProcessImage(img)
  
  GrayScale = ProcessImage.GrayScale(img)
  MiddleFilter=ProcessImage.MiddleFilter(GrayScale)
  Difference=ProcessImage.Difference(GrayScale,MiddleFilter)
  Convolution=ProcessImage.Convolution(Difference,SobelX,SobelY)
  Thresholding=ProcessImage.Thresholding(Convolution)
  Binarization=ProcessImage.Binarization(Thresholding)
  
  pixels=ProcessImage.PossiblePixels(Binarization)
  Dilated=ProcessImage.Dilatation(Binarization,pixels)
  print '<< Procesamiento de Imagen finalizado\n'


  print '>> Iniciando Deteccion de la Region posible de la Placa'
  # Se detecta la region en donde pudiera estar la placa
  shapes,x,y=DetectRegion.DetectShapes(Dilated)
  FramePlate=DetectRegion.FramePlate(img,x,y)

  picture = pygame.image.load(FramePlate)
  picture = pygame.transform.scale(picture, size)
  rect = picture.get_rect()
  rect = rect.move((80, 70))
  screen.blit(picture, rect)
  pygame.display.update() # Mostrar en pantalla imagen con recuadro rojo de la posible placa

  print '>> Posible Region de la Placa encontrada'
  
  
  imgPlate = cv2.imread('output/10. Region Placa.png',0)

  thresh_value = 100;
  max_thresh = 255;

  #                       src gray, threshold_value, max_BINARY_value, threshold_type
  ret,thresh = cv2.threshold(imgPlate,    127,                255,               1) # Se obtiene el umbral 
  cv2.bitwise_not(imgPlate, imgPlate);


  #Find bounding box
  #Bb=findBB(imgPlate);


  filtered = cv2.adaptiveThreshold(imgPlate.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41, 3)
  
  # Some morphology to clean up image
  kernel = np.ones((5,5), np.uint8)
  #kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
  opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
  closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

  #thresh = cv2.threshold(filtered,150,255,cv2.THRESH_BINARY_INV) # threshold
  dilated = cv2.dilate(thresh,kernel,iterations = 13) # dilate
  #contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours


  #gray = cv2.cvtColor(imgPlate,cv2.COLOR_BGR2GRAY)
  blur = cv2.GaussianBlur(imgPlate,(5,5),0)
  thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)
  contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
  cv2.drawContours(imgPlate,contours,-1,(0,255,0),3)


  imgPlate = Image.fromarray(imgPlate)
  imgPlate.save('output/14. Mejorada.png')

  #im = cv2.imread('output/14. Mejorada.png')

  # Se obtiene por OCR el String de la Placa Detectada
  text = image_to_string(imgPlate)
  #text = 'SPK-41-84'

  font = pygame.font.SysFont("Arial",38)
  TextSurf, TextRect = text_objects(text, font, RED)
  TextRect.center = (300, 445)
  screen.blit(TextSurf, TextRect)

  print '\nMatricula: '+text

  return False

def next_image() :
  l = len(file_list)
  global CURRENT_IMAGE

  if CURRENT_IMAGE < l :
    CURRENT_IMAGE = CURRENT_IMAGE+1
  if CURRENT_IMAGE == l :
    CURRENT_IMAGE = 0

  filename = 'input/'+file_list[CURRENT_IMAGE]
  img = pygame.image.load(image_path)
  picture = pygame.image.load(filename)
  picture = pygame.transform.scale(picture, size)
  rect = picture.get_rect()
  rect = rect.move((80, 70))
  screen.blit(picture, rect)
  pygame.display.update()

  return False

def previous_image() :
  l = len(file_list)
  global CURRENT_IMAGE

  if CURRENT_IMAGE <= l and CURRENT_IMAGE != 0 :
    CURRENT_IMAGE = CURRENT_IMAGE-1
  if CURRENT_IMAGE == 0 :
    CURRENT_IMAGE = l-1

  filename = 'input/'+file_list[CURRENT_IMAGE]
  img = pygame.image.load(image_path)
  picture = pygame.image.load(filename)
  picture = pygame.transform.scale(picture, size)
  rect = picture.get_rect()
  rect = rect.move((80, 70))
  screen.blit(picture, rect)
  pygame.display.update()

  return False

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    pygame.draw.rect(screen, ic,(x,y,w,h))

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        #pygame.draw.rect(screen, ac,(x,y,w,h))
        pygame.mouse.set_cursor(*HAND_CURSOR)
        if click[0] == 1 and action != None:
          action()

    else:
        pygame.mouse.set_cursor(*DEFAULT_CURSOR)

    

    smallText = pygame.font.SysFont("Arial",20)
    textSurf, textRect = text_objects(msg, smallText,BLACK)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

def createGUI():
  screen.fill(GRAY) # Se aplica fondo de la ventana

  font = pygame.font.SysFont("Arial",40)
  TextSurf, TextRect = text_objects("Licence Plate Recognition", font, BLACK)
  TextRect.center = (300, 30)
  screen.blit(TextSurf, TextRect)

  filename = 'input/'+file_list[CURRENT_IMAGE]
  img = pygame.image.load(image_path)
  picture = pygame.image.load(filename)
  picture = pygame.transform.scale(picture, size)
  rect = picture.get_rect()


  LicenceNumberArea = pygame.draw.rect(screen, WHITE,(200,420,200,50)) # Area donde mostraremos la matriculo detectada
  # Enmarcamos en un recuadro el area de la matricula
  pygame.draw.line(screen, (0, 0, 0), (200, 420), (400, 420),2) # Linea arriba
  pygame.draw.line(screen, (0, 0, 0), (200, 470), (400, 470),2) # Linea abajo
  pygame.draw.line(screen, (0, 0, 0), (200, 420), (200, 470),2) # Linea izquierda
  pygame.draw.line(screen, (0, 0, 0), (400, 420), (400, 470),2) # Linea derecha
  
  rect = rect.move((80, 70))
  screen.blit(picture, rect)

  # Enmarcamos en un recueadro el area de la IMAGEN
  pygame.draw.line(screen, BLACK, (77, 68), (523, 68),4) # Linea arriba
  pygame.draw.line(screen, BLACK, (77, 401), (523, 401),4) # Linea abajo
  pygame.draw.line(screen, BLACK, (77, 68), (77, 403),4) # Linea izquierda
  pygame.draw.line(screen, BLACK, (521, 68), (521, 403),4) # Linea derecha
  
  #pygame.display.flip()

if __name__ == "__main__":

  # Se obtienen las imagenes del directorio plates
  for file in os.listdir("input"):
    if file.endswith(".jpg") or file.endswith(".png"):
        file_list.append(file)

  images = []

  for i in range(len(file_list)):
    image_path = 'input/'+file_list[i]
    im = Image.open(image_path).convert('RGB')
    im.thumbnail(size, Image.ANTIALIAS)
    images.append(im) # Se carga la imagen de entrada y se convierte a RGB

  pygame.display.set_caption('Licence Plate Recognition') # Le ponemos nombre a la ventana
  screen = pygame.display.set_mode((600, 600)) # Se ajusta el tamaño de la ventana
  createGUI()

  while True:
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              sys.exit()
      button("<< Previous",130,530,100,50,GRAY2,GRAY,previous_image)
      button("Next >>",370,530,100,50,GRAY2,GRAY,next_image)
      button("Detect Plate!",250,480,100,50,RED,GRAY,detect_plate)
      pygame.display.update()
      #pygame.display.flip()
      clock.tick(8)