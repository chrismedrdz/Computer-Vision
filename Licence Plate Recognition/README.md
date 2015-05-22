# Reconocimiento de Placas

Proyecto Final: Visión Computacional V6 - ENE-JUN 2015 - FIME - UANL

## Descripción del Proyecto

- Se obtiene la imagen a procesar directamente de una carpeta previamente alimentada
- Se binariza la imagen con un umbral determinado.
- Se aplica la Transformada de Hough para detectar todas las lineas de la imagen
- Se localiza la placa identificando la ubicación de caracateres envueltos en un rectángulo.
- Eliminamos los demás pixeles y agrupamos la región de la placa.
- Segmentamos los caracteres de la Placa que ocupen mas del 60% de la altura de la misma.
- Identificamos mediante OCR las letras de la Placa.
- Se visualiza el número de matrícula detectada.

## Proceso de Reconocimiento de Placas

![Alt text](http://www.camera-sdk.com/attachments/89/number_plate_recognition_process.jpg "Proceso de Reconocimiento de Placas")

## Requerimientos

- Python 2.7+
- Paquete OpenCV > 2.4.7
- Librerías NumPy, Pygame y PIL instaladas
- Librería Pytesser
- Imágenes de carros matriculados colocadas en folder 'input'


## Requerimientos

- 
## Autor

Christopher Medina Rodríguez - 1488028