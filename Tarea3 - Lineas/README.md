# Detección de líneas

Tarea 3: Visión Computacional V6 - ENE-JUN 2015 - FIME - UANL

## Descripción

- Acceder a los pixeles clasificados como borde y sus vectores gradiente.
- Agrupar los pixeles de borde según el ángulo de gradiente con una discretización adecuada.
- Dentro de cada grupo, calcular los componentes conexos que respeten el ángulo de aquel grupo en su continuidad.
- Con la distribución de tamaños, determinar un umbral para descartar los demasiado chicos.
- Para cada componente que no se descarta, estimar la ecuación de recta de mejor ajuste a los pixeles incluidos en ese componente conexo con regresión lineal.
- Visualizar en una imagen de salida las líneas detectadas, dibujando su recta de regresión, se marcan las líneas detectadas.
- Se marcan las líneas horizontales en azul, las verticales en rojo y las diagonales en verde.
## Requerimientos

- Python 2.7+
- Librerías NumPy, Pygame y PIL instaladas
- Folders input y output

## Autor

Christopher Medina Rodríguez - 1488028