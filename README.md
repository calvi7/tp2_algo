 - Trabajo Practico 2 de ALGO 1 - Catedra COSTA - 

SOFTWARE: // requerimientos para el software
 - CRUD / ABM
 - Determinar recorrido optimo listando las ciudades
 - "botellas.txt" -> Verde: n, Azul: m


DEPENDENCIAS: // librerias necesarias
 - geopy
 - opencv
 - numpy
 - os
 - csv


DOCS: // documentacion y tutoriales de algunas dependencias
Opencv 
 -  https://opencv-tutorial.readthedocs.io/en/latest/index.html 
 -  https://www.youtube.com/watch?v=oXlwWbU8l2o 
 -  https://www.youtube.com/watch?v=WQeoO7MI0Bs&t=137s 

YOLO + Opencv 
 - https://towardsdatascience.com/object-detection-using-yolov3-and-opencv-
 - 19ee0792a420 
 - https://opencv-tutorial.readthedocs.io/en/latest/yolo/yolo.html#sources 
 - https://learnopencv.com/deep-learning-based-object-detection-using-yolov3-with-opencv-python-c/ 

RGB-HSV colors 
 - http://learn.leighcotnoir.com/artspeak/elements-color/hue-value-saturation/ 
 - https://cvexplained.wordpress.com/2020/04/28/color-detection-hsv/ 


ORGANIZACION REPO: // como esta organizado el repositorio
 - El repo esta organizado por carpetas
 - lib -> la carpeta principal, donde se guarda la mayoria del codigo
 - src -> se divide en 'ai' y 'geo' para las partes de Inteligencia Artificial y Geolocalizacion
 - assets -> se guardan cosas como imagenes, por ahora no sirve

INSTALAR DEPENDENCIAS: // como instalar las dependencias
1. Instalar pip
 - abrir CMD y correr 'python -m ensurepip --upgrade'

2. Instalar OpenCV
 - abrir CMD y correr 'pip install opencv-python'

3. Instalar GeoPy
 - abrir CMD y correr 'pip install geopy'

4. Instalar NumPy
 - abrir CMD y correr 'pip install geopy'

5. OS y CSV vienen con Python

6. Una vez que esta todo instalado, se deberia poder correr /lib/src/dependencies_test.py sin error.