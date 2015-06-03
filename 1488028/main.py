#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import sys
import os
import Image, ImageDraw, ImageFont
import random
import pygame
import numpy as np
import cv2
import cv
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

def validate(cnt):    
    rect=cv2.minAreaRect(cnt)  
    box=cv.cv.BoxPoints(rect) 
    box=np.int0(box)  
    output=False
    width=rect[1][0]
    height=rect[1][1]
    if ((width!=0) & (height!=0)):
        if((height*width<5000) & (height*width>100)): 
            output=True
    return output

#http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_watershed/py_watershed.html
if __name__ == "__main__":

	pygame.init() # Se inicializa pygame para la creacion de la ventana de salida

	im = Image.open('input/1.png').convert('RGB') # Se carga la imagen de entrada y se convierte a RGB
	width, height = im.size
	screen = pygame.display.set_mode((width, height)) # Se ajusta el tamaño de la ventana a las medidas de la imagen
	pygame.display.set_caption('Ordinary Test') # Le ponemos nombre a la ventana   

	#gray = filters.gray_scale(im)

	img = cv2.imread('input/1.png')
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


	cv2.imwrite('output/1. threshold.png',thresh)
	#img = Image.open('output/1. threshold.png').convert('RGB')


	# noise removal
	kernel = np.ones((3,3),np.uint8)
	opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

	# sure background area
	sure_bg = cv2.dilate(opening,kernel,iterations=3)

	# Finding sure foreground area
	dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
	ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

	# Finding unknown region
	sure_fg = np.uint8(sure_fg)
	unknown = cv2.subtract(sure_bg,sure_fg)
	cv2.imwrite('output/2. unknown.png',unknown)

	cont = 0
	image, contours, hierarchy = cv2.findContours(unknown,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	
	for cnt in contours:
		epsilon = 0.05*cv2.arcLength(cnt,True)
		approx = cv2.approxPolyDP(cnt,epsilon,True)

	if validate(approx): # Si el Area del bache esta entre 100 y 5000 pixeles
	    cv2.drawContours(img,[cnt],255,0,0)
	    x,y,w,h = cv2.boundingRect(approx)
	    # Se recorta la imagen con las dimensiones de la forma encontrada
	    ImageCrop = img[y:y+h,x:x+w]
	    cont += 1

	if cont == 0:
		ImageCrop = img

	#cv2.imwrite('output/11. Placa Recortada.png',PlateCrop)


	cv2.imshow('result',img)




	'''
	# Marker labelling
	ret, markers = cv2.connectedComponents(sure_fg)
	# Add one to all labels so that sure background is not 0, but 1
	markers = markers+1
	# Now, mark the region of unknown with zero
	markers[unknown==255] = 0
	markers = cv2.watershed(img,markers)
	img[markers == -1] = [255,0,0]
	'''

	#cv2.imshow('result',img)


	surface = pygame.image.load('output/2. unknown.png') # Se despliega la imagen en la ventana
	#surface = pygame.image.fromstring(corners.tostring(),corners.size,'RGB')

	screen = pygame.display.get_surface() 

	while True:
	  for event in pygame.event.get():
	      if event.type == pygame.QUIT:
	          sys.exit()
	  screen.blit(surface, (0,0))     
	  pygame.display.update()