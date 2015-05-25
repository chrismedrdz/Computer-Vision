#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Librerias
import tesseract
import numpy as np
import cv2
import cv2.cv as cv
import Image, ImageDraw, ImageFont

# Tesseract config
api = tesseract.TessBaseAPI()
api.Init(".","eng",tesseract.OEM_DEFAULT)
whitelist = '-ABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890'
api.SetVariable("tessedit_char_whitelist", whitelist)
api.SetPageSegMode(tesseract.PSM_AUTO)

#---------------------------------------------------------------------
# Rutinas Principales
#---------------------------------------------------------------------

def PrepareImage(img_path):
    im2 = Image.open(img_path)

    # Se escala la imagen a 100px de Altura para una mejor deteccion de los caracteres
    baseheight = 100
    hpercent = (baseheight / float(im2.size[1]))
    wsize = int((float(im2.size[0]) * float(hpercent)))
    escaled_plate = im2.resize((wsize, baseheight), Image.ANTIALIAS)
    str_path = 'output/15. Placa Escalada100px.png'
    escaled_plate.save(str_path)

    display = cv2.imread(str_path)
    height, width, depth = display.shape
    channel = 1
    display = cv2.cvtColor(display, cv2.COLOR_BGR2GRAY)
    thresh = 10
    #display = cv2.threshold(display, thresh, 255, cv2.THRESH_BINARY)[1]
    kernel = np.ones((5,5),np.uint8)
    erosion_iters = 0  
    display = cv2.erode(display,kernel, iterations = erosion_iters)


    imageRec = cv.CreateImageHeader((width,height), cv.IPL_DEPTH_8U, channel)
    cv.SetData(imageRec, display.tostring(),display.dtype.itemsize * channel * (width))

    return imageRec

def Recognize(image):
    tesseract.SetCvImage(image,api)
    full_text = ""
    full_text = api.GetUTF8Text()
    return str(full_text[0:9])