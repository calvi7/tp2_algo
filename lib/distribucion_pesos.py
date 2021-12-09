from abm import MainApp
from os import path


CAPACIDAD_C1: int = 600
CAPACIDAD_C2: int = 1000
CAPACIDAD_C3: int = 500
CAPACIDAD_C4: int = 2000


def camiones(peso_caba: int, peso_zn: int, peso_zc: int, peso_zs: int) -> dict[str, str]:
    contador: int = -1
    camiones_ocupados: list[int] = []
    distribucion_camiones: dict[str, str] = {}
    zonas: list[str] = ["caba", "norte", "centro", "sur"]

    for peso_pedido in [peso_caba, peso_zn, peso_zc, peso_zs]:
        contador += 1
        if (peso_pedido < CAPACIDAD_C3) and (CAPACIDAD_C3 not in camiones_ocupados):
            distribucion_camiones[zonas[contador]] = "Utilitario 003"
            camiones_ocupados.append(CAPACIDAD_C3)
        elif (peso_pedido < CAPACIDAD_C1) and (CAPACIDAD_C1 not in camiones_ocupados):
            distribucion_camiones[zonas[contador]] = "Utilitario 001"
            camiones_ocupados.append(CAPACIDAD_C1)
        elif (peso_pedido < CAPACIDAD_C2) and (CAPACIDAD_C2 not in camiones_ocupados):
            distribucion_camiones[zonas[contador]] = "Utilitario 002"
            camiones_ocupados.append(CAPACIDAD_C2)
        elif (peso_pedido < CAPACIDAD_C4) and (CAPACIDAD_C4 not in camiones_ocupados):
            distribucion_camiones[zonas[contador]] = "Utilitario 004"
            camiones_ocupados.append(CAPACIDAD_C4)
        else:
            print(":(")
        return distribucion_camiones


def calcular_peso(codigo_articulo: str, cantidad: str) -> int:
    peso: int = 0

    if codigo_articulo == "1334":
        peso = int(cantidad) * 450
    elif codigo_articulo == "568":
        peso = int(cantidad) * 350
    return peso


def pesos_por_zona(lista_zn: list[str], lista_zc: list[str], lista_zs: list[str]) -> None:
    local_path = path.join(path.dirname(__file__), "src\\pedidos.csv")
    app = MainApp(local_path)
    pedidos = app.dict_data()
    peso_caba: int = 0
    peso_zn: int = 0
    peso_zc: int = 0
    peso_zs: int = 0

    for pedido in pedidos:
        if pedido["Ciudad"] == "CABA":
            peso_caba += calcular_peso(pedido["Cod. Articulo"], pedido["Cantidad"])

        # cambiar a provincia dependiendo de la lista
        elif pedido["Ciudad"] in lista_zn:
            peso_zn += calcular_peso(pedido["Cod. Articulo"], pedido["Cantidad"])
        elif pedido["Ciudad"] in lista_zc:
            peso_zc += calcular_peso(pedido["Cod. Articulo"], pedido["Cantidad"])
        elif pedido["Ciudad"] in lista_zs:
            peso_zs += calcular_peso(pedido["Cod. Articulo"], pedido["Cantidad"])

