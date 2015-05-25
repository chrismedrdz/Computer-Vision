#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Librerias
from PIL import Image
import numpy as np
import math
import filters
from scipy.signal import wiener
import operator

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

# http://effbot.org/zone/pil-histogram-equalization.htm
# Se obtienen las crestas del histograma de la imagen se erosionan y los valles de dilatan
def equalize(histo):
    table = []

    for b in range(0, len(histo), 256):
        step = reduce(operator.add, histo[b:b+256]) / 255
        n = 0
        for i in range(256):
            table.append(n / step)
            n = n + histo[i+b]

    return table

def EqualizePlate(ProcessImage):
	lut = equalize(ProcessImage.histogram())
	im = ProcessImage.point(lut)

	im.save('output/12. Placa Equalizada.png')

	return wiener(ProcessImage)
