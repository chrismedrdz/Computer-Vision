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

# Mascaras de convolucion utilizadas
SobelX = [[-1.0, 0.0, 1.0], [-2.0, 0.0, 2.0], [-1.0, 0.0, 1.0]]
SobelY = [[1.0, 2.0, 1.0], [0.0, 0.0, 0.0], [-1.0, -2.0, -1.0]]


def GrayScale(ProcessImage):
	grises = filters.gray_scale(ProcessImage)
	grises.save('output/01. Grises.png')

	return grises

def MiddleFilter(ProcessImage):
	medio = filters.filtro_medio(ProcessImage)
	medio.save('output/02. Filtro Medio.png')

	return medio

def Difference(GrayScale,MiddleFilter):
	diferencia = filters.filtro_diferencia(GrayScale,MiddleFilter)
	diferencia.save('output/03. Filtro Diferencia.png')

	return diferencia

def Convolution(ProcessImage,MaskX,MaskY):
	convolution = filters.convolucion(ProcessImage,MaskX,MaskY)
	convolution.save('output/04. Bordes.png')

	return convolution

def Thresholding(ProcessImage):
	threshold = filters.threshold(ProcessImage)
	threshold.save('output/05. Umbralizada.png')

	return threshold

def Binarization(ProcessImage):
	binarize = filters.binarizacion(ProcessImage)
	binarize.save('output/06. Binarizada.png')

	return binarize

def PossiblePixels(ProcessImage):
	whites,others = filters.pixeles_blancos(ProcessImage)

	return whites

def Dilatation(ProcessImage,pixels):
	dilated = filters.dilatar(ProcessImage,pixels)
	dilated.save('output/07. Dilatada.png')

	return dilated

# Rutinas para la region de la Placa Detectada
def GrayScalePlate(ProcessImage):
	grises = filters.gray_scale(ProcessImage)
	grises.save('output/11. Placa Grises.png')

	return grises

def BinarizationPlate(ProcessImage):
	binarize = filters.binarizacion(ProcessImage)
	binarize.save('output/12. Placa Binarizada.png')

	return binarize


def MiddleFilterPlate(ProcessImage):
	medio = filters.filtro_medio(ProcessImage)
	medio.save('output/12. Placa Filtro Medio.png')

	return medio

def DifferencePlate(GrayScale,MiddleFilter):
	diferencia = filters.filtro_diferencia_plate(GrayScale,MiddleFilter)
	diferencia.save('output/13. Placa Filtro Diferencia.png')

	return diferencia