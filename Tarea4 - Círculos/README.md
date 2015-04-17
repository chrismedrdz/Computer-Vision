# Detección de Círculos

Tarea 4: Visión Computacional V6 - ENE-JUN 2015 - FIME - UANL

## Descripción

- Acceder a los pixeles clasificados como borde y sus vectores gradiente.
- Detectar las formas que tengan un numero elevado de direcciones de gradiente
- Dentro de cada una, calcular la ecuación de recta del gradiente de cada pixel.
- Asignar un voto a cada pixel que coincide con la recta (por pixel y por forma).
- Estimar el radio del círculo y su ecuación a partir del centro seleccionado y los pixeles incluidos.
- Visualizar en una imagen de salida los círculos detectados, dibujando su ecuación, utilizando un color distinto para cada círculo.

## Requerimientos

- Python 2.7+
- Librerías NumPy, Pygame y PIL instaladas
- Folders input y output

## Autor

Christopher Medina Rodríguez - 1488028