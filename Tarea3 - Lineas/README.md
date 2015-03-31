# Detección de formas

Tarea 2: Visión Computacional V6 - ENE-JUN 2015 - FIME - UANL

## Descripción

- Se acceden a los pixeles clasificados como borde y sus vectores gradiente.
- Se agrupan los pixeles de borde a componentes conexos.
- Se calcula la caja envolvente de cada componente conexo.
- Dentro de cada componente, agrupa a subcomponentes conexos según el ángulo de gradiente.
- Clasifica los componentes según el número de subcomponentes a clases de formas.
- Se visualiza en una imagen de salida las formas detectadas, dibujando su caja envolvente en un color de tal manera que cada clase de forma tiene un color distinto.

## Requerimientos

- Python 2.7+
- Librerías NumPy, Pygame y Image instaladas
- Folders input y output

## Autor

Christopher Medina Rodríguez - 1488028