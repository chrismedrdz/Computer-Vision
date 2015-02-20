#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Librerias
import Image
import math
from math import *
import time 
import sys,pygame
import ImageDraw
import random

#Marcara de Gradiente Diferencial utilizada
SobelX = [[-1,0,1],[-2,0,2],[-1,0,1]]
SobelY = [[1,2,1],[0,0,0],[-1,-2,-1]]

def gray_scale(im): #Rutina que convierte la imagen a escala de grises
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

def convolucion(imagen, mascarax, mascaray): #Metodo de convolucion discreta para 2D
    width, height = imagen.size
    x, y = imagen.size 
    pixel = imagen.load()
    
    new_image = Image.new("RGB", (width,height))
    draw = ImageDraw.Draw(new_image)

    for i in range(width):  # Se recorre la imagen por todo lo ancho
        for j in range(height): # Se recorre la imagen por todo lo alto
            sumx=0.0 # Inicializamos la sumatoria de X en cero 
            sumy = 0.0 # Inicializamos la sumatoria de Y en cero 
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
            #draw.point((i,j), 'red')
          
    return new_image


def formas(imagen):
    image = Image.open('output/2. Normalizada.png') #carca la imagen con convolucion y binarizada
    imagen = image.load()    
    ancho,alto = image.size # Obtenemos el ancho y alto de la imagen
    total = ancho*alto #Se calcula el area total de la imagen
    porcentaje = [] # Arreglo para los porcentajes de masas
    centro = [] # Arreglo para los centros de masas
    figura = 1 # Contador de numero de figuras encontradas

    #aplicamos bfs para la imagen 
    for a in range(ancho): # Se recorre la imagen por todo lo ancho
        for b in range(alto): # Se recorre la imagen por todo lo alto
          if imagen[a,b] == (0, 0, 0): # En caso de que el pixel sea negro se realiza lo siguiente
            color = random.randint(0,255),random.randint(0,255),random.randint(0,255) # Se genera un color aleatorio para BFS
            n,xs,xy= bfs(image,color,a,b) # Mandamos llamar el metodo bfs
            p = float(n)/float(total) * 100.0 #promedio maximo
            #porcentaje.append([0, (color)])
            if p > 0.5:
                centro.append((sum(xs)/len(xs),sum(xy)/len(xy))) # Se obtiene el centro de masa de la imagen
                porcentaje.append([p, (color)]) # Se agrega a la lista de promedios
                print "Figura %s"%figura
                figura +=1
            else:
                return None
    fondo_new = porcentaje.index(max(porcentaje)) # 
    max_c = porcentaje[fondo_new][1]
    for i in range(ancho): 
        for j in range(alto):
            if imagen[i,j]==max_c:
                imagen[i,j]=(255,0,0) #Pintamos en rojo la parte con mayor porcentaje de color
            
    nueva='output/5. Contornos.png'
    image.save(nueva)
    #return nueva
    print "Centro de Masa: %s"%centro
    #dibujar los centros y las etiquetas en las formas 
    draw = ImageDraw.Draw(image) 
    m=1
    for i in centro:
        draw.ellipse((i[0]-2, i[1]-2,i[0]+2,i[1]+2), fill=(0,0,0)) #dibuja los puntos en los centros de las formas
        draw.text(((i[0]+4,i[1]+4),), str(m), fill=(0,0,0)) #muestra las etiquetas cerca de los centros
        m +=1
    nueva2 = 'output/6. Final.png'
    image.save(nueva2)

    return nueva2

def bfs(imagen, simbolo, original, cola, ancho, altura):
    (fila, columna) = cola.pop(0)
    actual = imagen[fila][columna]
    if not actual == original:
        return False
    imagen[fila][columna] = simbolo
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            candidato = (fila + dy, columna + dx)
            if candidato[0] >= 0 and candidato[0] < altura and \
                    candidato[1] >= 0 and candidato[1] < ancho:
                contenido = imagen[candidato[0]][candidato[1]]
                if contenido == original:
                    cola.append(candidato)
    return True


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
    forma1 = image.save('output/4. BFS.png')
    return n, xs, ys

def main():    
    im = Image.open('input/imagen.png') # Se carga la imagen de entrada
    width, height = im.size
    grises = gray_scale(im)
    grises.save('output/1. Gris.png') # Se guarda el primer paso (Escala de grises)
    normalizada = normalizar(grises)
    normalizada.save('output/2. Normalizada.png') # Se guarda el segundo paso (Imagen binarizada)
    bordes = convolucion(normalizada, SobelX, SobelY)
    bordes.save("output/3. Bordes.png") # Se guarda el ultimo paso (Mascara en imagen)
    
    imagen_final = formas(bordes)
    if imagen_final is not None:
        pygame.init() # Se inicializa pygame para la creacion de la ventana de salida
        screen = pygame.display.set_mode((width, height)) # Se ajusta el tamaño de la ventana a las medidas de la imagen
        pygame.display.set_caption('Formas') # Le ponemos nombre a la ventana

        img = pygame.image.load(imagen_final) # Se carga la imagen final con las formas
        screen = pygame.display.get_surface() 

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            screen.blit(img, (0,0)) # Se despliega la imagen en la ventana   
            pygame.display.update()
    else:
        print 'No se encontraron figuras'

if __name__ == '__main__':
    main()