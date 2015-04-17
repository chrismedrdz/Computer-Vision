# Detección de Agujeros

Tarea 6: Visión Computacional V6 - ENE-JUN 2015 - FIME - UANL

## Descripción

- Acceder a los pixeles clasificados como borde y sus vectores gradiente.
- Determinar el histograma de colores de la imagen.
- dentificar el color dominante y reemplazar el rango coherente de este color con blanco, llevando los demás colores a tonos oscuros en escala de grises.
- Calcular el histograma de promedios normalizados de cada renglón y cada columna de la imagen procesada.
- Calcular las posiciones en los cuales ambos histogramas tienen picos.
- Detectar componentes conexos de tono coherente en estas posiciones.
- Con la distribución de tamaños de estos componentes, rechazar los demasiado pequeños.
- Calcular la caja envolvente de cada componente que no se rechaza (éstos son los agujeros).
- Visualizar en una imagen de salida los agujeros, dibujando su caja envolvente, utilizando un color distinto para cada agujero.

## Requerimientos

- Python 2.7+
- Librerías NumPy, Pygame y PIL instaladas
- Folders input y output

## Autor

Christopher Medina Rodríguez - 1488028