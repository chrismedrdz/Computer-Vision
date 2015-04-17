# Detección de Elipses

Tarea 5: Visión Computacional V6 - ENE-JUN 2015 - FIME - UANL

## Descripción

- Acceder a los pixeles clasificados como borde y sus vectores gradiente.
- Detectar las formas que tengan un numero elevado de direcciones de gradiente
- Dentro de cada forma de este tipo, calcular para cada par de pixeles la intersección de los tangentes de sus gradientes (T) y su punto intermedio (M).
- A partir de cada par (T, M) calculado, calcular la ecuación de la recta que los atraviesa.
- Asignar un voto a cada pixel de la recta definida por (T, M) desde M en la dirección que aleja de T.
- Calcular la distribución de los votos recibidos por los pixeles de la imagen (por forma).
- Seleccionar la moda de la distribución como el centro del elipse (por forma).
- Estimar la ecuación del elipse a partir del centro seleccionado y los pixeles incluidos.
- Visualizar en una imagen de salida los elipses detectados, dibujando su ecuación, utilizando un color distinto para cada elipse.

## Requerimientos

- Python 2.7+
- Librerías NumPy, Pygame y PIL instaladas
- Folders input y output

## Autor

Christopher Medina Rodríguez - 1488028