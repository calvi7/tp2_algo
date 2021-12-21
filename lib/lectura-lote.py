import cv2
import glob

path = glob.glob('Lote0001.JPEG/*jpg')
for file in path:
    img = cv2.imread(file)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

