#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Librerias
from PIL import Image, ImageTk
import numpy as np
import math
import random
import ImageDraw
from time import *

import filters

def DetectShapes(ProcessImage):
	centro=[]
	centro2=[]
	contador=[]
	colores=[]
	rec=[]
	pixeles=ProcessImage.load()#Cargar imagen
	ancho,alto = ProcessImage.size 
	for i in range(ancho):#Recorrer imagen
	    for j in range (alto):
	            if pixeles[i,j]==(255,255,255):#Si el pixel actual es negro
	                col1=random.randint(0,255)
	                col2=random.randint(0,255)#Se genera un color random
	                col3=random.randint(0,255)
	                r,g,b=(col1,col2,col3)
	                cont,color,centro1,centro2,cordenadas,ProcessImage=filters.bfs(ProcessImage,(i,j),(r,g,b))#Se aplica BFS 
	                contador.append(cont)#Se agrega a la cadena contador el numero de pixeles sumados en el recorrido anterior
	                colores.append(color)#Se agrega el color que se uso en el recorrido pasado
	                try:
	                    centro.append=((sum(centro1)/float(len(centro1)),sum(centro2)/float(len(centro2))))#Formula para obtener los centros
	                except:
	                    pass
	maximo=contador.index(max(contador))#Se obtiene el valor mas alto de la cadena contador
	gris=colores[maximo]#Se obtiene el color usado en el valor mas alto del contador
    
	for i in range(ancho):#Recorrer imagen para repintar el area mas grande por gris
		for j in range(alto):
				if pixeles[i,j]==gris:
					rec.append((i,j))
					pixeles[i,j]=(81,81,81) # Se pintan en gris los pixeles encontrados dentro de la forma
	medio=((len(rec)/2))
	x,y=rec[medio]
	ProcessImage.save('output/08. Formas.png')

	return ProcessImage,x,y

def FramePlate(ProcessImage,x,y):
	draw= ImageDraw.Draw(ProcessImage)
	draw.rectangle((x-60,y-40,x+60,y+40),outline="red")
	nueva = 'output/09. Placa Detectada.png'
	ProcessImage.save(nueva)
	return nueva

def GetRegion(ProcessImage,x,y):
	caja_envolvente=(x-60,y-40,x+60,y+40)
	region=ProcessImage.crop(caja_envolvente)
	nueva = 'output/10. Region Placa.png'
	region.save(nueva)
	return region