# antes era pruebas de geo.py, cambie el nombre para importarlo facil

import csv

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

from abm import MainApp
from os import path

ROUTE = path.join(path.dirname(__file__), "src\\pedidos.csv")

myApp = MainApp(ROUTE)


def mas_cerca_de_Caba(lista_1):
    geo: Nominatim = Nominatim(user_agent="Tp 2")
    lista: list = lista_1
    distancia_x_provincia: dict = {}
    distancia_en_km: list = []
    for i in lista:
        loc_caba = geo.geocode("CABA")
        loc_1 = geo.geocode(i, timeout=1)
        lugar_1 = (loc_1.latitude, loc_1.longitude)
        lugar_2 = (loc_caba.latitude, loc_caba.longitude)
        distancia = geodesic(lugar_1, lugar_2).kilometers
        distancia_x_provincia.update({distancia: i})
        distancia_en_km.append(distancia)
    return distancia_x_provincia


def recorrido_zona_norte(list_1, list_2):
    recorrido = []
    noroeste: dict = mas_cerca_de_Caba(list_1)
    noreste: dict = mas_cerca_de_Caba(list_2)
    distancias_noroeste = sorted(noroeste, reverse=True)
    distancias_noreste = sorted(noreste)
    distancias_total = distancias_noreste + distancias_noroeste
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
    distancias_zona: list = sorted(zona)
    for i in distancias_zona:
        if i in zona:
            b = zona[i]
            recorrido.append(b)
    return recorrido


def run():
    geo = Nominatim(user_agent="Tp 2")

    dict_zona_norte = {}
    list_zona_noreste = []
    list_zona_noroeste = []
    list_zona_centro = []
    list_zona_sur = []

    datos = myApp.dict_data()

    # casteo los datos a set para que sean unicos.
    provincias = set()
    ciudades = set()

    for pedido in datos:
        provincias.add(pedido['Provincia'])
        ciudades.add(pedido['Ciudad'])

    # los vuelvo a castear a lista para que sea mas facil trabajar
    provincias = list(provincias)
    ciudades = list(ciudades)

    for ciudad in ciudades:
        loc = geo.geocode(ciudad, timeout=3)
        latitud = loc.latitude
        longitud = loc.longitude

        if latitud*-1 < 35:
            dict_zona_norte.update({latitud: ciudad})
            if longitud*-1 < 63.45:
                list_zona_noreste.append(ciudad)
            elif longitud*-1 > 63.45:
                list_zona_noroeste.append(ciudad)

        if latitud*-1 > 35 and loc.latitude*-1 < 40:
            list_zona_centro.append(ciudad)

        if latitud*-1 > 40:
            list_zona_sur.append(ciudad)

    recorrido_norte: list = recorrido_zona_norte(
        list_zona_noroeste, list_zona_noreste)
    recorrido_centro: list = recorrdio_zonas_centro_sur(list_zona_centro)
    recorrido_sur: list = recorrdio_zonas_centro_sur(list_zona_sur)

    return recorrido_norte, recorrido_centro, recorrido_sur
