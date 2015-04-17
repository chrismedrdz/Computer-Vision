#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import sys
import os
import Image, ImageDraw, ImageFont
import random
import filters
import pygame

def chord_tangent(imagen, puntosDeBorde, vector):
    ie = Image.new('L', imagen.size, (0))
    x = len(puntosDeBorde)
    PL = filters.Vector(ie)

    for i in range(x):
        bp = len(puntosDeBorde[i])-1
        for j in range(len(puntosDeBorde[i])):

            pr = random.randint(0, bp/2)
            p1 = puntosDeBorde[i][pr]

            pr2 = random.randint(bp/2, bp)
            p2 = puntosDeBorde[i][pr2]

            if vector[p1] != vector[p2]:
                tan1 = [vector[p1], p1[1]-(vector[p1]*p1[0])] 
                tan2 = [vector[p2], p2[1]-(vector[p2]*p2[0])]
                x = float(tan2[1]-tan1[1]) / (tan1[0]-tan2[0])
                y = (tan1[0] * x )+ tan1[1]
                centroCuerda = ( (p1[0]+p2[0])/2, (p1[1]+p2[1])/2 )
                union = (x, y)
                if (union[0]-centroCuerda[0]) != 0:
                    M = (union[1]-centroCuerda[1] ) / (union[0]-centroCuerda[0])
                else:
                    M = 1
                b = centroCuerda[1] - (M*centroCuerda[0])
                centro = [M, b]
                if (union[0]-centroCuerda[0]) < 0.0:
                    sent = 1
                else:
                    sent = -1
                PL.pintar(centro, centroCuerda[0], sent)
    return ie

def encuentra_centros(imagen):
    ovalos = list()
    px = imagen.load()
    i, j = imagen.size
    for x in range(i):
        for y in range(j):
            if px[x,y] == 255:
                ovalos.append((x,y))
    
    ovalos = filters.BFS(ovalos)
    centros = list()
    for e in ovalos:
        x, y = (0, 0)
        for j in e:
            x += j[0]
            y += j[1]
        x = int(float(x)/len(e))
        y = int(float(y)/len(e))
        centros.append((x, y))
    return centros

if __name__ == "__main__":

    pygame.init() # Se inicializa pygame para la creacion de la ventana de salida
    
    # Mascaras de convolucion utilizadas
    SobelX = [[-1.0, 0.0, 1.0], [-2.0, 0.0, 2.0], [-1.0, 0.0, 1.0]]
    SobelY = [[1.0, 2.0, 1.0], [0.0, 0.0, 0.0], [-1.0, -2.0, -1.0]]

    pclave = (255,255,255)

    imagen = Image.open('input/input.png') # Se carga la imagen de entrada
    width, height = imagen.size
    screen = pygame.display.set_mode((width, height)) # Se ajusta el tamaño de la ventana a las medidas de la imagen
    original = imagen.copy()
    pygame.display.set_caption('Elipses') # Le ponemos nombre a la ventana   

       
    vector_gradiente = filters.vector_gradiente(imagen,SobelX,SobelY)

    umbral = 120
    puntos_borde = filters.puntos_borde(imagen, umbral=umbral)
    puntos_borde = filters.BFS(puntos_borde)

    ie = chord_tangent(imagen, puntos_borde, vector_gradiente)
    posiblesCentros = encuentra_centros(ie)

    px = imagen.load()
    d = list()
    for c in posiblesCentros:
        actual = list()
        actual.append(c[0])
        actual.append(c[1])
        horizontal = 0
        while px[tuple(actual)] != pclave:
            actual[0] += 1
            horizontal += 1
            if horizontal > width:
                break
        
        actual = list()
        actual.append(c[0])
        actual.append(c[1])
        vertical = 0
        while  px[tuple(actual)] != pclave:
            actual[1] += 1
            vertical += 1
            if vertical > height:
                break
        d.append((horizontal, vertical))

    tam = list(imagen.size)
    imagen = original
    ix, iy = imagen.size
    tam[0] = float(ix) / tam[0]
    tam[1] = float(iy) / tam[1]
    draw = ImageDraw.Draw(imagen)
    radio = 2
    for i in range(len(posiblesCentros)):
        x = int(posiblesCentros[i][0]*tam[0])
        y = int(posiblesCentros[i][1]*tam[1])
        draw.text((x, y+(radio*2)), str(i+1), fill=(255, 255, 255))
        draw.ellipse((x-d[i][0]*tam[0], y-d[i][1]*tam[1], x+d[i][0]*tam[0], y+d[i][1]*tam[1]), outline = (255, random.randint(0,150), random.randint(0, 100)))
        draw.ellipse((x-radio, y-radio, x+radio, y+radio), fill=(0, 255, 0))
        print "Elipse detectado. ID: ",i+1, " Centro: ",(x,y)

    imagen.save("output/Elipses.png")

    img = pygame.image.load('output/Elipses.png') # Se despliega la imagen en la ventana
    screen = pygame.display.get_surface() 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.blit(img, (0,0))     
        pygame.display.update()