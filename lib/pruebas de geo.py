from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import csv
def mas_cerca_de_Caba(lista_1):
    geo = Nominatim(user_agent="Tp 2")
    lista:list = lista_1
    distancia_x_provincia:dict = {}
    distancia_en_km:list = []
    for i in lista:
        loc_caba = geo.geocode("CABA")
        loc_1= geo.geocode(i, timeout=1)
        lugar_1 = (loc_1.latitude,loc_1.longitude)
        lugar_2 = (loc_caba.latitude,loc_caba.longitude)
        distancia = geodesic(lugar_1,lugar_2).kilometers
        distancia_x_provincia.update({distancia:i})
        distancia_en_km.append(distancia)
    return distancia_x_provincia

def recorrido_zona_norte(list_1,list_2):
    recorrido = []
    noroeste:dict = mas_cerca_de_Caba(list_1)
    noreste:dict = mas_cerca_de_Caba(list_2) 
    distancias_noroeste = sorted(noroeste,reverse = True)
    distancias_noreste = sorted(noreste)
    distancias_total =  distancias_noreste + distancias_noroeste
    for i in distancias_total:
        if i in noroeste:
            b = noroeste[i]
            recorrido.append(b)
        if i in noreste:
            b = noreste[i]
            recorrido.append(b)
    return recorrido

def recorrdio_zonas_centro_sur(list_1):
    recorrido = []
    zona: dict = mas_cerca_de_Caba(list_1)
    distancias_zona:list = sorted(zona)
    for i in distancias_zona:
        if i in zona:
            b = zona[i]
            recorrido.append(b)
    return recorrido



def main():
    geo = Nominatim(user_agent="Tp 2")
    
    dict_zona_norte = {}
    list_zona_noreste = []
    list_zona_noroeste = []    
    list_zona_centro = []
    list_zona_sur = []
    ciudades_de_pedido = [  "Capital Federal","Catamarca","Chaco","Chubut","Córdoba Argentina","Corrientes","Entre Ríos","Jujuy",
    "La Pampa","La Rioja Argentina","Mendoza","Misiones"
    ,"Neuquén"
    ,"Río Negro"
    ,"Salta"
    ,"San Juan Argentina"
    ,"San Luis"
    ,"Santa Cruz Argentina"
    ,"Santa Fe"
    ,"Santiago del Estero"
    ,"Tierra del Fuego Argentina"
    ,"Tucumán"]
    provinciasciudades=[]
    i=0
    with open('D:/archivo csv/pedidos.csv', 'r') as f:
        next(f, None)
        for linea in f:
        # Remover salto de línea
            linea = linea.rstrip()
        # Ahora convertimos la línea a arreglo con split
            lista = linea.split(",")
        # Tenemos la lista. En la 0 tenemos el nombre, en la 1 la calificación y en la 2 el precio  
            provinciasciudades.append([])
            provinciasciudades[i] = lista[3]
            i+=1
            provinciasciudades.append([])
            provinciasciudades[i] = lista[4]
            i+=1
    print(provinciasciudades) 
    
    
    
    for i in ciudades_de_pedido:
        loc = geo.geocode(i, timeout=3)
        latitud = loc.latitude
        longitud = loc.longitude
        
        if latitud*-1<35:
            dict_zona_norte.update({latitud:i})
            if longitud*-1<63.45:
                list_zona_noreste.append(i)   
            elif longitud*-1>63.45:
                list_zona_noroeste.append(i)
        
        if latitud*-1>35 and loc.latitude*-1<40:
            list_zona_centro.append(i)

        if latitud*-1>40:
            list_zona_sur.append(i)
    
    recorrido_norte: list = recorrido_zona_norte(list_zona_noroeste,list_zona_noreste)
    recorrido_centro:list = recorrdio_zonas_centro_sur(list_zona_centro)
    recorrido_sur: list = recorrdio_zonas_centro_sur(list_zona_sur)
    
    print(recorrido_centro)
    print(recorrido_norte)
    print(recorrido_sur)
    


main()







