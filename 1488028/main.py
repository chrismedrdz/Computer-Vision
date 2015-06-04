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
import filters

def scale_image(img):

	height, width, _ = img.shape

	baseheight = 500
	hpercent = (baseheight / float(height))
	wsize = int((float(width) * float(hpercent)))
	scaled = cv2.resize(img, (wsize, baseheight)) 
	cv2.imwrite('output/01. scaled.png',scaled)
	screen = pygame.display.set_mode((wsize, baseheight)) 

	return scaled

if __name__ == "__main__":

	pygame.init() # Init pygame for GUI

	im = Image.open('input/1.png').convert('RGB') # Se carga la imagen de entrada y se convierte a RGB
	width, height = im.size
	pygame.display.set_caption('Ordinary Test') # Le ponemos nombre a la ventana   

	# Get image input
	img = cv2.imread('input/1.png')

	# Scale the Image to 500 baseHeight
	scaled = scale_image(img)
	#Set display dimensions

	#Convert image to GRAY SCALE
	gray = cv2.cvtColor(scaled,cv2.COLOR_BGR2GRAY)
	cv2.imwrite('output/02. gray.png',gray)

	#threasholding the grayscale image
	ret, thresh = cv2.threshold(gray,100,255, cv2.THRESH_BINARY)
	cv2.imwrite('output/03. threshold.png',thresh)

	# Erode image 7 times
	kernel = np.ones((2,2),np.uint8)

	erode = cv2.erode(thresh,kernel, iterations = 7)
	#erode(gray,Erode,Mat(),Point(2,2),7)
	cv2.imwrite('output/04. eroded.png',erode)

	# Dilate image 7 times
	dilate = cv2.dilate(thresh,kernel,iterations=1)
	#dilate=dilate(gray,Dilate,Mat(),Point(2,2),7)
	cv2.imwrite('output/05. dilated.png',dilate)

	# Get the thresholding of binary inverted
	ret, thresh_dilated = cv2.threshold(erode,1, 50, cv2.THRESH_BINARY_INV)
	cv2.imwrite('output/06. thresh dilated.png', thresh_dilated)

	path_trace = cv2.add(erode,thresh_dilated)
	cv2.imwrite('output/07. path trace.png', path_trace)

	_, contours, hier = cv2.findContours(erode,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	
	# Find the index of the largest contour
	areas = [cv2.contourArea(c) for c in contours]
	max_index = np.argmax(areas)

	img = cv2.drawContours(scaled, contours, max_index, (255,255,255), -1)
	cv2.imwrite('output/08. contour road.png',img)


	img = Image.open('output/08. contour road.png').convert('RGB')
	new_image = Image.new("RGB", (img.size[0],img.size[1]))

	im = Image.open('output/01. scaled.png').convert('RGB')

	for i in range(img.size[0]):
		for j in range (img.size[1]):
			(r,g,b)=img.getpixel((i,j))

			if (r,g,b) == (255,255,255):
				new_image.putpixel((i, j), im.getpixel((i,j)) )
			else:
				new_image.putpixel((i, j), (0, 255, 0))

	new_image.save('output/09. road.png')


	img = cv2.imread('output/09. road.png')
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	_, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

	# noise removal
	kernel = np.ones((3,3),np.uint8)
	opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

	# sure background area
	sure_bg = cv2.dilate(opening,kernel,iterations=3)
	cv2.imwrite('output/10. anomalies_shapes.png', sure_bg)

	# Finding sure foreground area
	dt = cv2.distanceTransform(opening, 2, 3)
	dt = ((dt - dt.min()) / (dt.max() - dt.min()) * 255).astype(np.uint8)
	_, sure_fg = cv2.threshold(dt, 100, 255, cv2.THRESH_BINARY)

	sure_fg = np.uint8(thresh)
	#cv2.imshow('sure_fg',sure_fg)

	unknown = cv2.subtract(sure_bg,sure_fg)
	#cv2.imshow('unknown',unknown)

	# Marker labelling
	_, markers = cv2.connectedComponents(sure_fg)
	markers = markers+0

	# Now, mark the region of unknown with zero
	markers[unknown==255] = 0

	markers = cv2.watershed(img,markers)
	img[markers == -1] = [0,0,255]

	cv2.imwrite('output/11. anomalies.png', img)


	# Find anomalies contours for display results in console
	_, contours2, hier = cv2.findContours(sure_bg,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	areas = [cv2.contourArea(c) for c in contours2]
	
	anomalies = list() # array for anomalies detected
	cont=1
	for a in range(len(areas)):
		if areas[a] < 1000 : # Omits external contours
			anomalies.append(areas)
			print '\tAnomalie # '+str(cont)+' : crash area -> '+str(areas[a])
			cont+=1


	print '\nDetect '+str(cont-1)+' anomalies in asphalt pavement.'

	if max(anomalies) > 200:
		print '\n\n\t Its necessary repair asphalt with urgency.'
	elif max(anomalies) < 200 and max(anomalies) > 100:
		print '\n\n\t Its necessary repair asphalt with low priority.'
	else:
		print '\n\n\t Its not necessary repair asphalt.'


	surface = pygame.image.load('output/11. anomalies.png')
	screen = pygame.display.get_surface()

	while True:
	  for event in pygame.event.get():
	      if event.type == pygame.QUIT:
	          sys.exit()
	  screen.blit(surface, (0,0))     
	  pygame.display.update()