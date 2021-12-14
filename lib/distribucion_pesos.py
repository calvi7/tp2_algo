from abm import MainApp
from os import path


CAMINO_PARA_EL_CSV: str = "src\\pedidos.csv"
CAPACIDAD_C1: int = 600
CAPACIDAD_C2: int = 1000
CAPACIDAD_C3: int = 500
CAPACIDAD_C4: int = 2000
CODIGO_BOTELLAS: str = "1334"
CODIGO_VASOS: str = "568"
PESO_BOTELLAS: int = 450
PESO_VASOS: int = 350


def escritura_archivo(distribucion: dict[str, str]) -> None:
    """Le paso un diccionario diciendole a que zona va que camion y cuanto peso hay por zona,
     con eso me escribe un archivo salida.txt donde se puede encontrar la informacion que se le paso"""
    utilitario_caba: str = distribucion["caba"]
    utilitario_norte: str = distribucion["norte"]
    utilitario_centro: str = distribucion["centro"]
    utilitario_sur: str = distribucion["sur"]
    pesos: list = [distribucion["peso caba"], distribucion["peso norte"], distribucion["peso centro"],
                   distribucion["peso sur"]]
    with open("salida.txt", "w") as salida:
        salida.writelines(f"CABA:\n{utilitario_caba}\n{pesos[0]} Kg\n Recorrido\n\n"
                          f"Zona norte:\n{utilitario_norte}\n{pesos[1]} Kg\n Recorrido\n\n"
                          f"Zona centro:\n{utilitario_centro}\n{pesos[2]} Kg\n Recorrido\n\n"
                          f"Zona sur:\n{utilitario_sur}\n{pesos[3]} Kg\n Recorrido")


def calcular_peso(codigo_articulo: str, cantidad: str) -> int:
    """Le paso el codigo de articulo y la cantidad de un pedido para que me devuelva el peso de ese pedido"""
    peso: int = 0

    if codigo_articulo == CODIGO_BOTELLAS:
        peso = int(cantidad) * PESO_BOTELLAS
    elif codigo_articulo == CODIGO_VASOS:
        peso = int(cantidad) * PESO_VASOS
    return peso


def ajuste(pedidos: list[dict[str, str]], pedidos_no_completados: list[dict[str, str]]) -> float:
    """Le paso una lista con diccionarios de los pedidos de una zona en especifico y quita pedidos para reducir el
    peso total que se debe enviar a esa zona por falta de camiones capacitados para llevar tanto peso"""
    peso: float = 0

    eliminado: dict[str, str] = pedidos.pop()
    pedidos_no_completados.append(eliminado)
    for pedido in pedidos:
        peso += calcular_peso(pedido["Cod. Articulo"], pedido["Cantidad"])
    peso = peso / 1000
    return peso


def camiones(peso_caba: float, peso_zn: float, peso_zc: float, peso_zs: float, pedidos: list[list[dict]],
             pedidos_no_completados: list[dict]) -> dict[any]:
    """Le paso el peso total que se tiene que entregar a cada zona y los diccionarios de pedidos por zona y pedidos que
     no se pudieron completar para que quite los pedidos de uno y los ponga en no entregar de ser necesario.
     Tambien distribuye en los distintos camiones,intenta darle el camion mas chico que satisface el peso necesario.
      Me devuelve un diccionario con llave la zona y valor que utilitario fue designado a esa zona"""
    contador: int = -1
    camiones_ocupados: list[int] = []
    distribucion_camiones: dict[any] = {}
    zonas: list[str] = ["caba", "norte", "centro", "sur"]

    for peso_pedido in [peso_caba, peso_zn, peso_zc, peso_zs]:
        contador += 1
        resuelto: bool = False
        while not resuelto:
            resuelto = True
            if (peso_pedido < CAPACIDAD_C3) and (CAPACIDAD_C3 not in camiones_ocupados):
                distribucion_camiones[zonas[contador]] = "Utilitario 003"
                distribucion_camiones["peso " + zonas[contador]] = peso_pedido
                camiones_ocupados.append(CAPACIDAD_C3)
            elif (peso_pedido < CAPACIDAD_C1) and (CAPACIDAD_C1 not in camiones_ocupados):
                distribucion_camiones[zonas[contador]] = "Utilitario 001"
                distribucion_camiones["peso " + zonas[contador]] = peso_pedido
                camiones_ocupados.append(CAPACIDAD_C1)
            elif (peso_pedido < CAPACIDAD_C2) and (CAPACIDAD_C2 not in camiones_ocupados):
                distribucion_camiones[zonas[contador]] = "Utilitario 002"
                distribucion_camiones["peso " + zonas[contador]] = peso_pedido
                camiones_ocupados.append(CAPACIDAD_C2)
            elif (peso_pedido < CAPACIDAD_C4) and (CAPACIDAD_C4 not in camiones_ocupados):
                distribucion_camiones[zonas[contador]] = "Utilitario 004"
                distribucion_camiones["peso " + zonas[contador]] = peso_pedido
                camiones_ocupados.append(CAPACIDAD_C4)
            else:
                peso_pedido = ajuste(pedidos[contador], pedidos_no_completados)
                resuelto = False
    return distribucion_camiones


def pesos_por_zona(pedidos: list[list[dict]]) -> list[float]:
    """Le paso una lista con las listas de diccionario de cada pedido separadas por zona y me devuelve una lista
    con los pesos a entregar en cada zona"""
    peso_caba: float = 0
    peso_zn: float = 0
    peso_zc: float = 0
    peso_zs: float = 0
    lista_pesos: list[float]
    contador: int = -1

    for pedido in pedidos[0]:
        peso_caba += calcular_peso(pedido["Cod. Articulo"], pedido["Cantidad"])
    for pedido in pedidos[1]:
        peso_zn += calcular_peso(pedido["Cod. Articulo"], pedido["Cantidad"])
    for pedido in pedidos[2]:
        peso_zc += calcular_peso(pedido["Cod. Articulo"], pedido["Cantidad"])
    for pedido in pedidos[3]:
        peso_zs += calcular_peso(pedido["Cod. Articulo"], pedido["Cantidad"])

    # Paso de gramos a kilogramos
    peso_caba = peso_caba / 1000
    peso_zn = peso_zn / 1000
    peso_zc = peso_zc / 1000
    peso_zs = peso_zs / 1000
    lista_pesos = [peso_caba, peso_zn, peso_zc, peso_zs]
    return lista_pesos


def zona_de_pedidos(pedidos: list[dict[str, str]], lista_zn: list, lista_zc: list, lista_zs) -> list[list[dict]]:
    """Le paso los diccionarios de pedidos y las listas de las ciudades por zona para separar los pedidos por zona"""
    pedidos_caba: list[dict] = []
    pedidos_zn: list[dict] = []
    pedidos_zc: list[dict] = []
    pedidos_zs: list[dict] = []

    for pedido in pedidos:
        if pedido["Ciudad"] == "CABA":
            pedidos_caba.append(pedido)
        elif pedido["Ciudad"] in lista_zn:
            pedidos_zn.append(pedido)
        elif pedido["Ciudad"] in lista_zc:
            pedidos_zc.append(pedido)
        elif pedido["Ciudad"] in lista_zs:
            pedidos_zs.append(pedido)
    return [pedidos_caba, pedidos_zn, pedidos_zc, pedidos_zs]


def main() -> None:
    local_path = path.join(path.dirname(__file__), CAMINO_PARA_EL_CSV)
    app = MainApp(local_path)
    pedidos = app.dict_data()
    pedidos_no_completados: list[dict[str, str]] = []

    pedidos_por_zona: list[list[dict]] = zona_de_pedidos(pedidos, ["Parana"], ["Villa María"], ["Santa Rosa"])
    pesos: list[float] = pesos_por_zona(pedidos_por_zona)
    distribucion_camiones = camiones(pesos[0], pesos[1], pesos[2], pesos[3], pedidos_por_zona, pedidos_no_completados)
    escritura_archivo(distribucion_camiones)


main()
