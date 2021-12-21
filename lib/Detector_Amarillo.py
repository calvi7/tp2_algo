import cv2
import numpy as np
def dibujarContorno(contornos, color):
  for (i, c) in enumerate(contornos):
    M = cv2.moments(c)
    if (M["m00"]==0): M["m00"]==1
    x = int(M["m10"]/M["m00"])
    y = int(M["m01"]/M["m00"])
    cv2.drawContours(imagen, [c], 0, color, 2)
    cv2.putText(imagen, str(i+1), (x-10,y+10), 1, 2,(0,0,0),2)
amarilloBajo = np.array([20, 100, 20], np.uint8)
amarilloAlto = np.array([32, 255, 255], np.uint8)

imagen = cv2.imread("./Lote.JPEG/13.jpg")
imagenHSV = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

maskAmarillo = cv2.inRange(imagenHSV, amarilloBajo, amarilloAlto)


contornosAmarillo = cv2.findContours(maskAmarillo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

dibujarContorno(contornosAmarillo, (0, 255,255))


imgResumen = 255 * np.ones((210,100,3), dtype = np.uint8)
cv2.circle(imgResumen, (30,30), 15, (0,255,255), -1)
cv2.circle(imgResumen, (30,70), 15, (140,40,120), -1)
cv2.circle(imgResumen, (30,110), 15, (0,255,0), -1)
cv2.circle(imgResumen, (30,150), 15, (0,0,255), -1)
cv2.putText(imgResumen,str(len(contornosAmarillo)),(65,40), 1, 2,(0,0,0),2)

totalCnts = len(contornosAmarillo)
cv2.putText(imgResumen,str(totalCnts),(55,200), 1, 2,(0,0,0),2)
cv2.imshow('Imagen', imagen)
cv2.imwrite('conteo.png', imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()



