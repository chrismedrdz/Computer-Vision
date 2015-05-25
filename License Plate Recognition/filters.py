#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Librerias
import Image
import math
from math import *
import sys
import random
import numpy

def binarizacion(img):                    # Rutina que binariza la imagen a partir de un umbral
    ancho,alto = img.size                        # Obtenermos el tamaño de la imagen
    pixeles=img.load()                           # Apuntamos hacia los pixeles de la imagen
    umbral = 90                                 # Se define el umbral
    for i in range(ancho):                       # Se recorrre la imagen a lo ancho
        for j in range(alto):                    # Se recorrre la imagen a lo alto
            r = img.getpixel((i,j))[0]           # Se obtiene el valor de la posicion red del color
            g = img.getpixel((i,j))[1]           # Se obtiene el valor de la posicion green del color
            b = img.getpixel((i,j))[2]           # Se obtiene el valor de la posicion blue del color
            promedio=int((r+g+b)/3)              # Se obtiene un promedio de los colores
            if promedio > umbral:                # Si el promedio es mayor al umbral
                pixeles[i,j]=(255,255,255)       # Se cambia el pixel a negro
            else:                                # Si no
                pixeles[i,j]=(0,0,0)             # Se cambia el pixel a negro
    return img

def gray_scale(im):                              # Rutina que convierte la imagen a escala de grises
    imagen_grises = im.copy()                    # Se hace una copia de la imagen original
    width, height = im.size                      # Obtenermos el tamaño de la imagen
    img = imagen_grises.convert('RGB')           # Convertimos la imagen a RGB

    pixeles = imagen_grises.load()               # Cargamos los pixeles de la imagen
    for i in range(width):                       # Se recorrre la imagen a lo ancho
        for j in range(height):                  # Se recorre la imagen a lo alto
            prom = sum(pixeles[i,j])/3           # Se calcula el promedio
            pixeles[i,j] = (prom,prom,prom)      # Se agrega el nuevo valor al arreglo de pixeles
    
    return imagen_grises

def umbral(img):
    w,h = img.size                               # Obtenermos el tamaño de la imagen
    pixeles = img.load()                         # Apuntamos hacia los pixeles de la imagen
    lista_pixeles = []                           # Lista que almacenara los nuevos pixeles de la nueva imagen normalizada
    for j in range(h):                           # Se recorre la imagen por todo lo alto
        for i in range(w):                       # Se recorre la imagen por todo lo ancho
            pix = pixeles[i,j][1]
            lista_pixeles.append(pix)            # Se almacena el pixel en la lista de pixeles
    maximo = max(lista_pixeles)                  # Se obtiene el umbral mas alto de toda la lista de pixeles
    minimo = min(lista_pixeles)                  # Se obtiene el umbral mas bajo de toda la lista de pixeles
    l = 255.0/(maximo-minimo)                    # Se calcula el valor del umbral de corte para identificar las magnitudes más fuertes
   
    return minimo,maximo,l

def threshold(img):#Funcion para generar la imagen umbral
    ancho,alto = img.size
    # Valores minimo y maximo para encontrar el umbral
    minimo=30
    maximo=200
    pixeles=img.load()#cargar la imagen
    for i in range(ancho):#Se recorre los pixeles de la imagen
        for a in range(alto):
            (r,g,b)=img.getpixel((i,a))
            promedio=int((r+g+b)/3)#Obtenemos el promedio de cada pixel
            if promedio <= minimo: #Se hace la comparacion con los valores 
                promedio=0
            if promedio >= maximo:
                promedio=255
            pixeles[i,a]=(promedio,promedio,promedio)#Se sustituye el valor de rgb segun sea
    return img

def normalizar(norm):
    w,h = norm.size                              # Obtenermos el tamaño de la imagen
    pixeles = norm.load()                        # Apuntamos hacia los pixeles de la imagen
    lista_pixeles = []                           # Lista que almacenara los nuevos pixeles de la nueva imagen normalizada
    for j in range(h):                           # Se recorre la imagen por todo lo alto
        for i in range(w):                       # Se recorre la imagen por todo lo ancho
            pix = pixeles[i,j][1]
            lista_pixeles.append(pix)            # Se almacena el pixel en la lista de pixeles
    maximo = max(lista_pixeles)                  # Se obtiene el umbral mas alto de toda la lista de pixeles
    minimo = min(lista_pixeles)                  # Se obtiene el umbral mas bajo de toda la lista de pixeles
    l = 255.0/(maximo-minimo)                    # Se calcula el valor del umbral de corte para identificar las magnitudes más fuertes

    for j in range(h):                           # Se recorre la imagen por todo lo alto
        for i in range(w):                       # Se recorre la imagen por todo lo alto
            pix = pixeles[i,j][0]                # Se obtiene el pixel
            nuevo = int(floor((pix-minimo)*l))   # Nuevo pixel normalizado
            pixeles[i,j] = ((nuevo,nuevo,nuevo)) # Se almacena el nuevo valor del pixel

    return norm,minimo


def normalize(img):
    h = len(img)
    w = len(img[0])
    minimo = min(min(img))[1]
    maximo = max(max(img))[1]
    div = maximo - minimo
    
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
                    dy = j - (l / 2) # Se centra la mascara a lo ancho
                    
                    ix = x + dx
                    iy = y + dy
                    
            fila.append(valor)
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

def convolucion(imagen,Gx,Gy):
    gx=[]
    gy=[]
    magnitud=[]
    ancho,alto = imagen.size
    #Gx=([-1,0,1],[-2,0,2],[-1,0,1])
    #Gy=([1,2,1],[0,0,0],[-1,-2,-1])
    pixeles=imagen.load()
    for i in range(alto):
        gx.append([])
        gy.append([])
        for j in range(ancho):
            sumx=0
            sumy=0
            for x in range(len(Gx[0])):
                for y in range(len(Gy[0])):
                    try:
                        sumx +=(pixeles[j+y,i+x][0]*Gx[x][y])
                        sumy +=(pixeles[j+y,i+x][0]*Gy[x][y])
                    except:
                        pass
                    Gradiente_Horizontal=pow(sumx,2)#Formulas para obtener el gradiente
                    Gradiente_Vertical=pow(sumy,2)
                    Magnitud=int(math.sqrt(Gradiente_Horizontal+Gradiente_Vertical))
                    gx[i].append(sumx)
                    gy[i].append(sumy)
                    pixeles[j,i]=(Magnitud,Magnitud,Magnitud)
    return imagen

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

def bfs(imagen,actual,color):
    pixeles=imagen.load()
    ancho,alto = imagen.size
    con=0
    con2=0
    cola=[]#Se crea la cola
    cordenadas=[]
    centro_i=[]
    centro_j=[]
    puntos=[]
    cola.append(actual)#Se agrega el valor actual a la cola
    act=actual
    partida=pixeles[actual] # punto de partida
    while len(cola)>0: # Mientras existan valores en la cola hacer...
        (x,y)=cola.pop(0) # Removemos el valor de la cola
        actual=pixeles[x,y] # actual toma el valor de la cola
        if actual==partida or actual ==color:#Si el pixel actual es igual al punto de partida o color 
            
            try:
                if (pixeles[x-1,y]):#Revisar vecino izq
                    if (pixeles[x-1,y]==partida):#Si rgb de vecino izq es igual a punto de partida
                        pixeles[x-1,y]=color#Pintar pixel de color
                        cola.append((x-1,y))#Y agregar a cola
                        con+=1
                        centro_i.append((x-1))#Agregar a lista para obtener los centros
                        centro_j.append((y))
                        cordenadas.append((x-1,y))
            except:
                pass

            try:
                if (pixeles[x+1,y]):#Revisar vecino der                                                
                    if (pixeles[x+1,y]==partida):#Lo mismo vecino der
                        pixeles[x+1,y]=color
                        cola.append((x+1,y))
                        con+=1
                        centro_i.append((x+1))
                        centro_j.append((y))
                        cordenadas.append((x+1,y))
            except:
                pass
            try:
                if (pixeles[x,y-1]):#Revisar vecino abajo                                              
                    if (pixeles[x,y-1]==partida):#Lo mismo vecino abajo
                        pixeles[x,y-1]=color
                        cola.append((x,y-1))
                        con+=1
                        centro_i.append((x))
                        centro_j.append((y-1))
                        cordenadas.append((x,y-1))
                                    
            except:
                pass

            try:
                if (pixeles[x,y+1]):#Revisar vecino arriba                                              
                    if (pixeles[x,y+1]==partida):#Lo mismo vecino arriba
                        pixeles[x,y+1]=color
                        cola.append((x,y+1))
                        con+=1
                        centro_i.append((x))
                        centro_j.append((y+1))
                        cordenadas.append((x,y+1))
            except:
                pass
    return con,color,cordenadas,imagen

def bfs2(img,ancho,alto):
    cola = []
    cola2 = []
    pixeles = img.load()
    for i in range (ancho):
        for j in range(alto):
            (r,g,b) = img.getpixel((i,j))
            if ((r,g,b,)==(255,255,255)):
                cola.append((i,j))
            else:
                cola2.append((i,j))
    return cola,cola2

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
    return image

def array2list(a):
    h = len(a)
    w = len(a[0])

    newPixels = list()
    for y in xrange(h):
        for x in xrange(w):
            newPixels.append(tuple([int(v) for v in a[y,x]]))
    return newPixels

def dilatar(imagen,cola):
    width, height = imagen.size
    pixeles = imagen.load()
    x=0
    while x<len(cola):
        (i,j) = cola[x]
        try:
            if(pixeles[i+1,j]): 
                pixeles[i+1,j] = (255,255,255)
        except:
            pass
        try:
            if(pixeles[i-1,j]):
                   pixeles[i-1,j] =(255,255,255)
        except:
            pass
        try:
            if(pixeles[i,j+1]):
                pixeles[i,j+1]=(255,255,255)
        except:
            pass
        try: 
            if(pixeles[i,j-1]):
                pixeles[i,j-1] = (255,255,255)
        except:
            pass
        try: 
            if(pixeles[i+1,j+1]):
                pixeles[i+1,j+1]=(255,255,255)
        except:
            pass
        try: 
            if(pixeles[i-1,j+1]):
                pixeles[i-1,j+1] = (255,255,255)
        except:
            pass
        try:
            if(pixeles[i+1,j-1]):
                pixeles[i+1,j-1] = (255,255,255)
        except:
            pass
        try: 
            if(pixeles[i-1,j-1]):
                pixeles[i-1,j-1] = (255,255,255)
        except:
            pass
        x+=1
    return imagen

def erosionar(imagen,cola):
    pixeles = imagen.load()
    x=0
    while x<len(cola):
        (i,j) = cola[x]
        try:                
            if(pixeles[i+1,j]):
                pixeles[i+1,j] = (0,0,0)
        except:
            pass
        try:   
            if(pixeles[i-1,j]):
                   pixeles[i-1,j] =(0,0,0)
        except:
            pass
        try:                                                                                                 
            if(pixeles[i,j+1]):
                pixeles[i,j+1]=(0,0,0)
        except:
            pass
        try:                                                                
            if(pixeles[i,j-1]):
                pixeles[i,j-1] = (0,0,0)
        except:
            pass
        try:                                                                       
            if(pixeles[i+1,j+1]):
                pixeles[i+1,j+1]=(0,0,0)
        except:
            pass
        try:                 
            if(pixeles[i-1,j+1]):
                pixeles[i-1,j+1] = (0,0,0)
        except:
            pass
        try:         
            if(pixeles[i+1,j-1]):
                pixeles[i+1,j-1] = (0,0,0)
        except:
            pass
        try:   
            if(pixeles[i-1,j-1]):
                pixeles[i-1,j-1] = (0,0,0)
        except:
            pass
        x+=1
    return imagen

def zeros(n, m):
    matrix = []
    for i in range(n):
        tmp = []
        for j in range(m):
            tmp.append(0)
        matrix.append(tmp)
    return matrix

def is_neighbor(p1, p2, (w, h)):
  for i in [-1, 0, 1]:
    for j in [-1, 0, 1]:
      print ""

def distance(p1, p2):
  x1, y1 = p1
  x2, y2 = p2
  return math.sqrt( math.pow((x2 - x1) , 2) +  math.pow((y2 - y1) , 2))

def convolucion2(im, mask):
  w, h = im.size
  pix = im.load()
  out_im = Image.new("RGB", (w, h))
  out = out_im.load()
  for i in xrange(1, w):
    for j in xrange(h-1):
      suma1, suma2, suma3 = 0, 0, 0
      for n in xrange(i-1, i+2):
        for m in xrange(j-1, j+2):
            if n >= 0 and m >= 0 and n < w and m < h:
              suma1 += mask[n - (i - 1)][ m - (j - 1)] * pix[n, m][0]
              suma2 += mask[n - (i - 1)][ m - (j - 1)] * pix[n, m][1]
              suma3 += mask[n - (i - 1)][ m - (j - 1)] * pix[n, m][2]
      out[i, j] = suma1, suma2, suma3
  return out_im

def vector_gradiente(imagen, maskX, maskY):

    px_copia = (imagen.copy()).load()
    px = imagen.load()
    x,y = imagen.size
    valores = {}
    for i in range(x):
        for j in range(y):
            gx,gy = 0,0
            pos = 0
            for h in range(i-1, i+2):
                for l in range(j-1, j+2):
                    if h >= 0 and l >= 0 and h < x and l < y:
                        punto = px_copia[h, l]
                        su = 0
                        for e in punto:
                            su += e
                        punto  = su / 3
                        gx += punto*maskX[int(pos/3)][pos%3]
                        gy += punto*maskY[int(pos/3)][pos%3]
                        pos += 1
            gr = int(math.sqrt(math.pow(gx, 2) + math.pow(gy, 2)))
            px[i, j] = tuple([gr]*3)
            if gx != 0.0:
                valores[i, j] = gy / gx
            else:
                valores[i, j] = 1
    return valores

def puntos_borde(imagen, umbral):
    if umbral == 0:
        umbral = 123
    x,y = imagen.size
    pbordes = []
    px = imagen.load()
    for i in range(x):
        for j in range(y):
            if type(px[i, j]) == type(0):
                if px[i, j] < umbral:
                    px[i, j] = 0
                else:
                    px[i, j] = 255
                continue    
            lc = list(px[i,j])
            if lc[0] < umbral:
                lc[0] = 0
            else:
                pbordes.append((i, j))
    return pbordes


# Mejora la imagen haciendo una limpieza de ruido a nivel medio
# Esto pudiera empezarse a notar una imagen con partes borrosas
def filtro_medio(imagen):
    pixeles=imagen.load()
    ancho,alto = imagen.size
    for i in range(ancho):
        for j in range(alto):
            (r,g,b)=imagen.getpixel((i,j))
            cola=[]
            try:
                if(pixeles[i+1,j]):# Vecino Derecho
                    pix=pixeles[i+1,j][0]
                    cola.append((pix))
            except:
                pass
            try:
                if(pixeles[i-1,j]):# Vecino Izquierdo
                    pix=pixeles[i-1,j][0]
                    cola.append((pix))
            except:
                pass
            try:
                if(pixeles[i,j+1]):# Vecino Arriba
                    pix=pixeles[i,j+1][0]
                    cola.append((pix))
            except:
                pass
            try:
                if(pixeles[i,j-1]):# Vecino Abajo
                    pix=pixeles[i,j-1][0]
                    cola.append((pix))
            except:
                pass                        
            try:
                if(pixeles[i+1,j+1]):# Vecino Esquina Derecha Arriba
                    pix=pixeles[i+1,j+1][0]
                    cola.append((pix))
            except:
                pass
            try:
                if(pixeles[i-1,j+1]):# Vecino Esquina Izquierda Arriba
                    pix=pixeles[i-1,j+1][0]
                    cola.append((pix))
            except:
                pass
            try:
                if(pixeles[i+1,j-1]):# Vecino Esquina Derecha Abajo
                    pix=pixeles[i+1,j-1][0]
                    cola.append((pix))
            except:
                pass
            try:
                if(pixeles[i-1,j-1]):# Vecino Esquina Izquierda Abajo
                    pix=pixeles[i-1,j-1][0]
                    cola.append((pix))
            except:
                pass

            cola.sort()
            mediano=int(numpy.median(cola))
            pixeles[i,j]=(mediano,mediano,mediano)
    return imagen

# El filtro de diferencia es una forma de hallar bordes en imágenes.
# Resta de imagen Escala de grises - Filtro Medio
def filtro_diferencia(grises,medio):
    img=Image.open('output/01. Grises.png')
    pixeles=img.load()
    pixeles2=medio.load()
    ancho,alto = img.size
    for i in range(ancho):
        for j in range(alto):
            (r,g,b)=grises.getpixel((i,j))
            (r,g,b)=medio.getpixel((i,j))
            nueva=pixeles2[i,j][0]
            original=pixeles[i,j][0]
            dif=(nueva-original)
            pixeles[i,j]=(dif,dif,dif)
    return img

def filtro_diferencia_plate(grises,medio):
    img=Image.open('output/11. Placa Grises.png')
    pixeles=img.load()
    pixeles2=medio.load()
    ancho,alto = img.size
    for i in range(ancho):
        for j in range(alto):
            (r,g,b)=grises.getpixel((i,j))
            (r,g,b)=medio.getpixel((i,j))
            nueva=pixeles2[i,j][0]
            original=pixeles[i,j][0]
            dif=(nueva-original)
            pixeles[i,j]=(dif,dif,dif)
    return img
# Se agregan todos los pixeles blancos encontrados para despues realizar dilatacion
def pixeles_blancos(img):
    blancos=[] # En esta cola se almacentaran los pixeles blancos encontrados
    otros=[] # En esta cola se almacentaran todos los demas pixeles
    pixeles=img.load()
    ancho,alto = img.size
    for i in range(ancho):
        for j in range(alto):
            (r,g,b)=img.getpixel((i,j))
            if ((r,g,b)==(255,255,255)):
                blancos.append((i,j))
            else:
                otros.append((i,j))
    
    return blancos,otros