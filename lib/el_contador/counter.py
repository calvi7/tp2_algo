import numpy as np
import cv2 as cv
import glob
import os


class Matcher:
    def __init__(self) -> None:
        self.path = os.path.dirname(__file__)
        
    def es_slice(self, img, template) -> bool:
        img = cv.imread(img)
        template = cv.imread(template)
        
        result_try = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
        _, mVal, _, _ = cv.minMaxLoc(result_try)
        
        return mVal > .9
   
    def contador(self):
        _lote = os.path.join(self.path, "Lote0001")
        lote = os.listdir(_lote)

        
        vasos = {
            'negro': 0,
            'azul': 0,
        }
        
        botellas = {
            'roja': 0,
            'azul': 0,
            'verde': 0,
            'negra': 0,
            'amarilla': 0
        }
        
        slice_vaso = "slices\\vaso_###.jpg"
  
        slice_bot = "slices\\bot_###.jpg"
        
        print("Analizando lote . . .")
        for img in lote:
            img = os.path.join(self.path, "Lote0001", img)

            errMsg = "Se detuvo el proceso. En un minuto se reanuda."
            try:
                for color in vasos.keys():
                    slice_vaso = slice_vaso.replace("###", color)
                    comp = os.path.join(self.path, slice_vaso)
                    
                    if self.es_slice(img, comp):
                        vasos[color] += 1

                for color in botellas.keys():
                    slice_bot = slice_bot.replace("###", color)
                    comp = os.path.join(self.path, slice_bot)
                    
                    if self.es_slice(img, comp):
                        botellas[color] += 1
            except:
                print(errMsg)

        self.write(("vasos", vasos), ("botellas", botellas))
        
        
    def write(self, *args):
        """los args tendrian que ser pasados como tupla, con el nombre siendo el primer 
        elemento de la tupla y el diccionario [color, numero] siendo el segundo
        """
        for el in args:
            name, elements = el
            listado = "\n".join(f"{color.capitalize()}: {count}" for color, count in elements.items())
            with open(f"{name}.txt", "w") as f:
                f.writelines(listado)
    
    
def main():
    # para debuguear nada mas
    matcher = Matcher()
    
    path = os.path.dirname(__file__)
    vaso_azul = os.path.join(path, "Lote0001\\11.jpg")
    slice_v_a = os.path.join(path, "slices\\bot_roja.jpg")
    
    es = matcher.es_slice(vaso_azul, slice_v_a)

    matcher.contador()
    
    try:
        assert es == True
    except:
        print("Esta mal")


if __name__ == "__main__":
    main()

