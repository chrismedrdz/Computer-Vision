#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Librerias
import Image
import math
from math import *
import sys
import random
import numpy

def gray_scale(im): # Rutina que convierte la imagen a escala de grises
    imagen_grises = im.copy() # Se hace una copia de la imagen original
    width, height = im.size # Obtenermos el tamaño de la imagen
    img = imagen_grises.convert('RGB') # Convertimos la imagen a RGB

    pixeles = imagen_grises.load() # Cargamos los pixeles de la imagen
    for i in range(width): # Se recorrre la imagen a lo ancho
        for j in range(height): # Se recorre la imagen a lo alto
            prom = sum(pixeles[i,j])/3 # Se calcula el promedio
            pixeles[i,j] = (prom,prom,prom) # Se agrega el nuevo valor al arreglo de pixeles
    
    return imagen_grises

def normalizar(norm):
    w,h = norm.size # Obtenermos el tamaño de la imagen
    pixeles = norm.load() # Cargamos los pixeles de la imagen
    lista_pixeles = [] # Lista que almacenara los nuevos pixeles de la nueva imagen normalizada
    for j in range(h): #Se recorre la imagen por todo lo alto
        for i in range(w): #Se recorre la imagen por todo lo ancho
            pix = pixeles[i,j][1]
            lista_pixeles.append(pix) # Se almacena el pixel en la lista de pixeles
    maximo = max(lista_pixeles) # Se obtiene el umbral mas alto de toda la lista de pixeles
    minimo = min(lista_pixeles) # Se obtiene el umbral mas bajo de toda la lista de pixeles
    l = 255.0/(maximo-minimo)  # Se calcula el valor del umbral de corte para identificar las magnitudes más fuertes

    for j in range(h):
        for i in range(w):
            pix = pixeles[i,j][1] #Se obtiene el pixel
            nuevo = int(floor((pix-minimo)*l)) # Nuevo pixel normalizado
            pixeles[i,j] = ((nuevo,nuevo,nuevo)) # Se almacena

    return norm

def normalize(img):
    h = len(img)
    w = len(img[0])
    minimo = min(min(img))[1]
    maximo = max(max(img))[1]
    div = maximo - minimo

    #print 'Maximo: ',maximo
    #print 'Minimo: ',minimo
    
    for y in xrange(h):
        for x in xrange(w):
            try:
                img[y][x] = (img[y][x][1] - minimo) / div
            except:
                img[y][x] = 0.0        

    return img

def euclidean(gx, gy):
    h = len(gx)
    w = len(gx[0])

    gx = numpy.array(gx)
    gy = numpy.array(gy)

    m = list()
    for y in xrange(h):
        c = list()
        for x in xrange(w):
            g1 = numpy.log10(abs(gx[y,x]))
            g2 = numpy.log10(abs(gy[y,x]))

            mag = numpy.sqrt(gx[y,x]**2 + gy[y,x]**2)
            mag = tuple([int(floor(sqrt(p))) for p in mag])
            #print mag
            c.append(mag)
        m.append(c)
    return m

def convolution(image, mask):
    resultado = list()

    n = 1.0/1.0
    mask = numpy.array(mask) * n # Mascara simetrica


    h = image["size"][1] # Se obtiene la altura de la imagen
    w = image["size"][0] # Se obtiene la anchura de la imagen

    k = len(mask[0]) # Se obtiene la altura de la mascara
    l = len(mask) # Se obtiene la anchura de la mascara

    pixels = image["pixels"]
    pixels = slicing(pixels, w)
    pixels = numpy.array(pixels)

    #F = numpy.zeros(shape=pixels.shape)

    for y in xrange(h):
        fila = list()
        for x in xrange(w):
            valor = 0.0
            for i in xrange(k):
                dx = i - (k / 2) # Se centra la mascara a lo alto
                suma = numpy.array([0.0, 0.0, 0.0])
                for j in xrange(l):
                    try:
                        val= mask[i][j] * pixels[y+i, x+j]
                    except:
                        val=0
                    valor+=val
                    #print val
                    dy = j - (l / 2) # Se centra la mascara a lo ancho

                    #try:
                     #   suma += pixels[y+dx,x+dy]*mask[i,j]
                    #except IndexError: pass    
                    
                    ix = x + dx
                    iy = y + dy
                    #if ix >= 0 and ix < w and iy >= 0 and iy < h:
                        #valor += pixels[iy][ix] * mask[j][i]
                        #valor= mask[m][h] * pixels[i+m, j+h][0]
                        #valor = log10(valor)
                    
            fila.append(valor)
            #print suma
            #F[y,x] = suma
            #print F[y,x]
        resultado.append(fila)
    return resultado

def convolucion(imagen, mascarax, mascaray): # Metodo de convolucion discreta para 2D
    width, height = imagen.size
    x, y = imagen.size 
    pixel = imagen.load()
    
    new_image = Image.new("RGB", (width,height))

    for i in range(width):  # Se recorre la imagen por todo lo ancho
        for j in range(height): # Se recorre la imagen por todo lo alto
            sumx=0.0 # Inicializamos la sumatoria de X en cero 
            sumy=0.0 # Inicializamos la sumatoria de Y en cero 
            for m in range(len(mascarax[0])): # Recorremos la mascara en X a lo alto
                for h in range(len(mascaray[0])):# Recorremos la mascara en Y a lo alto
                    try:
                        mul_x= mascarax[m][h] * pixel[i+m, j+h][0]
                        mul_y= mascaray[m][h] * pixel[i+m, j+h][0]
                    except:
                        mul_x=0
                        mul_y=0
                    sumx+=mul_x # Se realiza la sumatoria de los valores en X
                    sumy+=mul_y # Se realiza la sumatoria de los valores en Y
            valorx = pow(sumx,2)
            valory = pow(sumy,2)
            grad = int(math.sqrt(valorx + valory)) # Se calcula el gradiente en RGB
            if grad <= 0:
                grad = 0
            elif grad >= 255:
                grad = 255
            pixel[i,j] = (grad, grad, grad) # Agregamos el nuevo valor al arreglo de la gradiente
            new_image.putpixel((i, j), (grad, grad, grad))
          
    return new_image


def bfs(image,color,a,b): 
    imagen=image.load()
    ancho,alto=image.size
    original = imagen[a,b]
    c=[]
    xs=[]
    ys=[]
    c.append((a,b))
    n = 1
    while len(c) > 0:
        (x, y) = c.pop(0)
        actual = imagen[x, y]
        if actual == original or actual == color:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    i, j = (x + dy, y + dx)
                    if i >= 0 and i < ancho and j >= 0 and j < alto:
                        contiene = imagen[i, j]
                        if contiene == original:
                            imagen[i, j] = color
        
                            xs.append(i)
                            ys.append(j)
                            n += 1
                            c.append((i, j))
    return n, xs, ys

def frecuentes(histo, cantidad):
    frec = list()
    for valor in histo:
        if valor is None:
            continue
        frecuencia = histo[valor]
        acepta = False
        if len(frec) <= cantidad:
            acepta = True
        if not acepta:
            for (v, f) in frec:
                if frecuencia > f:
                    acepta = True
                    break
        if acepta:
            frec.append((valor, frecuencia))
            frec = sorted(frec, key = lambda tupla: tupla[1])
            if len(frec) > cantidad:
                frec.pop(0)
    incluidos = list()
    for (valor, frecuencia) in frec:
        incluidos.append(valor)
        #print frecuencia
    return incluidos


def slicing(pixels, width):
    return [pixels[a:a+width] for a in xrange(0, len(pixels), width)]

def de_slicing(p):
    pixels = list()
    for a in p:
        pixels += a
    return pixels

def valorDeVecinos(imagen, x, y, w, h):
    resultado = list()
    for deltax in [-1, 0, 1]:
        posx = x + deltax
        if posx >= 0 and posx < w:
            for deltay in [-1, 0, 1]:
                posy = y + deltay
                if posy >= 0 and posy < h:
                    resultado.append(imagen[posy][posx])
    return resultado

def imageToPixels(inputImage):
    image = dict()
    #i = Image.open(inputImage)

    pixels = inputImage.load()
    w, h = inputImage.size
    pixelsRGB = list()
    for x in xrange(h):
        for y in xrange(w):
            pixel = pixels[y,x]
            pixelsRGB.append(pixel)
    image["instance"] = inputImage
    image["size"] = tuple([w, h])
    image["pixels"] = pixelsRGB
    #print len(pixelsRGB)
    return image

def array2list(a):
    h = len(a)
    w = len(a[0])

    newPixels = list()
    for y in xrange(h):
        for x in xrange(w):
            newPixels.append(tuple([int(v) for v in a[y,x]]))
    return newPixels