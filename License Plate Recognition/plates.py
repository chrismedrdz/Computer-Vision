#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter
import math
import sys
import os
import Image, ImageDraw, ImageFont
import random
import pygame
import cv2
import cv2.cv as cv
from pygame import mouse
import numpy as np

import ProcessImage
import DetectRegion
import OCR
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

icon = pygame.image.load('logo.png')
icon = pygame.transform.scale(icon, (32, 32))
pygame.display.set_icon(icon)
pygame.display.set_caption('Licence Plate Recognition') # Le ponemos nombre a la ventana
screen = pygame.display.set_mode((600, 600)) # Se ajusta el tamaño de la ventana

size = 440, 330 # Tamaño de la imagen a mostrar en GUI
CURRENT_IMAGE = 0
file_list = []
font = pygame.font.SysFont("Arial",38)

clock = pygame.time.Clock()

#---------------------------------------------------------------------
# Rutinas Principales
#---------------------------------------------------------------------
  # PIL to OpenCV Image
def pil_to_cvimage(img):
  cv_img = np.array(img) 
  # Convert RGB to BGR 
  cv_img = cv_img[:, :, ::-1].copy()
  return cv_img

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def ProcessPlate(img):
  GrayScale = ProcessImage.GrayScalePlate(img)
  MiddleFilter=ProcessImage.MiddleFilterPlate(GrayScale)
  Difference=ProcessImage.DifferencePlate(GrayScale,MiddleFilter)
  Binarization=ProcessImage.BinarizationPlate(GrayScale)

  return Difference

def print_string(texto):

  LicenceNumberArea = pygame.draw.rect(screen, GRAY,(380,419,202,52)) # Limpiamos la zona con el color de fondo de ventana

  LicenceNumberArea = pygame.draw.line(screen, (0, 0, 0), (380, 470), (580, 470),2) # Linea de la matricula

  TextSurf, TextRect = text_objects(texto, font, RED)
  TextRect.center = (480, 445)
  screen.blit(TextSurf, TextRect)

def print_image(str_path):
  picture = pygame.image.load(str_path)  
  rect = picture.get_rect()
  width, height = rect.size   # Get Image dimensions

  LicenceNumberArea = pygame.draw.rect(screen, GRAY,(50,420,350,52)) # Limpiamos la zona con el color de fondo de ventana

  LicencePlateArea = pygame.draw.rect(screen, WHITE,(50,420,200,50)) # Area donde mostraremos la matriculo detectada
  # Enmarcamos en un recuadro el area de la matricula
  pygame.draw.line(screen, (0, 0, 0), (50, 420), (250, 420),2) # Linea arriba
  pygame.draw.line(screen, (0, 0, 0), (50, 470), (250, 470),2) # Linea abajo
  pygame.draw.line(screen, (0, 0, 0), (50, 420), (50, 470),2) # Linea izquierda
  pygame.draw.line(screen, (0, 0, 0), (250, 420), (250, 470),2) # Linea derecha

  if width <= 200:
    x = 51+((200-width)/2)
  else:
    x = 51

  rect = rect.move((x, 423))
  screen.blit(picture, rect)

def validate(cnt):    
    rect=cv2.minAreaRect(cnt)  
    box=cv2.cv.BoxPoints(rect) 
    box=np.int0(box)  
    output=False
    width=rect[1][0]
    height=rect[1][1]
    if ((width!=0) & (height!=0)):
        if (((height/width>2) & (height>width)) | ((width/height>2) & (width>height))):
            if((height*width<5000) & (height*width>100)): 
                output=True
    return output

def detect_plate():
  global CURRENT_IMAGE

  print_string('Wait')

  image_path = 'input/'+file_list[CURRENT_IMAGE]
  img=Image.open(image_path) # Abrir la imagen

  print ' \n|| Imagen a Analizar: '+image_path.replace("input/","")+' || \n'

  '''
  En esta fase Procesamos la imagen del auto para aplicarle los filtros necesarios para poder
  trabajar con ella y facilitar el paso de detección de la región de la placa.
  '''
  # Mascaras de convolucion utilizadas
  SobelX = [[-1.0, 0.0, 1.0], [-2.0, 0.0, 2.0], [-1.0, 0.0, 1.0]]
  SobelY = [[1.0, 2.0, 1.0], [0.0, 0.0, 0.0], [-1.0, -2.0, -1.0]]

  print '>> Iniciando Procesamiento de Imagen'

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
  RegionPlate=DetectRegion.GetRegion(img,x,y)

  picture = pygame.image.load(FramePlate)
  picture = pygame.transform.scale(picture, size)
  rect = picture.get_rect()
  rect = rect.move((80, 70))
  screen.blit(picture, rect)
  pygame.display.update()

  print '>> Posible Region de la Placa encontrada'  

  imgPlate = cv2.imread('output/10. Region Placa.png')
  imgPlateGray = cv2.imread('output/10. Region Placa.png',0)

  ret,gray = cv2.threshold(imgPlateGray,125,255,0)
  gray2 = gray.copy()
  mask = np.zeros(gray.shape,np.uint8)

  cont = 0

  contours, hier = cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
  for cnt in contours:
    epsilon = 0.05*cv2.arcLength(cnt,True)
    approx = cv2.approxPolyDP(cnt,epsilon,True)

    if validate(approx): # Si el Area del contorno está entre 100 y 5000 pixeles
      cv2.drawContours(imgPlate,[cnt],0,0,0)
      x,y,w,h = cv2.boundingRect(approx)
      # Se recorta la imagen con las dimensiones de la forma encontrada
      PlateCrop = imgPlate[y:y+h,x:x+w]
      cont += 1

  if cont == 0:
    PlateCrop = imgPlate

  cv2.imwrite('output/11. Placa Recortada.png',PlateCrop)
  img = Image.open('output/11. Placa Recortada.png').convert('RGB')

  EqualizedPlate=ProcessImage.EqualizePlate(img)

  original = Image.open('output/12. Placa Equalizada.png')

  if cont != 0:
    width, height = original.size # Se obtienen las dimensiones de la imagen
    left = width * 0.03
    top = height * 0.24
    cropped_plate = original.crop(   ( int(left) , int(top), int(width-left), int(height-top)  )   )
    cropped_plate.save('output/13. Placa Cortada.png')
  else: 
    width, height = original.size # Se obtienen las dimensiones de la imagen
    left = width * 0.15
    top = height * 0.3
    cropped_plate = original.crop(   ( int(left) , int(top), int(width-left), int(height-top)  )   )
    cropped_plate.save('output/13. Placa Cortada.png')

  # Se escala la imagen de la placa para mostrarla en GUI
  baseheight = 45
  hpercent = (baseheight / float(cropped_plate.size[1]))
  wsize = int((float(cropped_plate.size[0]) * float(hpercent)))
  escaled_plate = cropped_plate.resize((wsize, baseheight), Image.ANTIALIAS)
  str_path = 'output/14. Placa Escalada45px.png'
  escaled_plate.save(str_path)

  # Se muestra en la GUI la imagen de la Placa
  print_image(str_path)
  
  # Se obtiene por OCR el String de la Placa Detectada
  ocr_image_cv = OCR.PrepareImage('output/13. Placa Cortada.png');
  text = OCR.Recognize(ocr_image_cv)

  # Se muestra en la GUI el Numero de Matricula detectada
  print_string(text)
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

  TextSurf, TextRect = text_objects("Licence Plate Recognition", font, BLACK)
  TextRect.center = (300, 30)
  screen.blit(TextSurf, TextRect)

  filename = 'input/'+file_list[CURRENT_IMAGE]
  img = pygame.image.load(image_path)
  picture = pygame.image.load(filename)
  picture = pygame.transform.scale(picture, size)
  rect = picture.get_rect()


  LicenceNumberArea = pygame.draw.rect(screen, WHITE,(50,420,200,50)) # Area donde mostraremos la matricula detectada
  # Enmarcamos en un recuadro el area de la matricula
  pygame.draw.line(screen, (0, 0, 0), (50, 420), (250, 420),2) # Linea arriba
  pygame.draw.line(screen, (0, 0, 0), (50, 470), (250, 470),2) # Linea abajo
  pygame.draw.line(screen, (0, 0, 0), (50, 420), (50, 470),2) # Linea izquierda
  pygame.draw.line(screen, (0, 0, 0), (250, 420), (250, 470),2) # Linea derecha


  # Linea donde se escribira el numero de matricula
  pygame.draw.line(screen, (0, 0, 0), (380, 470), (580, 470),2) # Linea abajo
  
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

  createGUI()

  while True:
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              sys.exit()
      button("<< Previous",130,530,100,50,GRAY2,GRAY,previous_image)
      button("Next >>",370,530,100,50,GRAY2,GRAY,next_image)
      button("Detect Plate!",250,480,100,50,RED,GRAY,detect_plate)
      pygame.display.update()
      clock.tick(5)