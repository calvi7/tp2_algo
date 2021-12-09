from abm import MainApp
from os import path


CAPACIDAD_C1: int = 600
CAPACIDAD_C2: int = 1000
CAPACIDAD_C3: int = 500
CAPACIDAD_C4: int = 2000


def camiones(peso_caba: float, peso_zn: float, peso_zc: float, peso_zs: float) -> dict[str, str]:
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


def pesos_por_zona(lista_zn: list[str], lista_zc: list[str], lista_zs: list[str]) -> list[float]:
    local_path = path.join(path.dirname(__file__), "src\\pedidos.csv")
    app = MainApp(local_path)
    pedidos = app.dict_data()
    peso_caba: float = 0
    peso_zn: float = 0
    peso_zc: float = 0
    peso_zs: float = 0
    lista_pesos: list[float] = []

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
    peso_caba = peso_caba / 1000
    peso_zn = peso_zn / 1000
    peso_zc = peso_zc / 1000
    peso_zs = peso_zs / 1000
    lista_pesos = [peso_caba, peso_zn, peso_zc, peso_zs]
    return lista_pesos


def escritura_archivo(distribucion: dict[str, str], pesos: list[float]) -> None:
    utilitario_caba: str = distribucion["caba"]
    utilitario_norte: str = distribucion["norte"]
    utilitario_centro: str = distribucion["centro"]
    utilitario_sur: str = distribucion["sur"]
    with open("salida.txt", "w") as salida:
        salida.writelines(f"CABA:\n{utilitario_caba}\n{pesos[0]} Kg\n Recorrido\n\n"
                          f"Zona norte:\n{utilitario_norte}\n{pesos[1]} Kg\n Recorrido\n\n"
                          f"Zona centro:\n{utilitario_centro}\n{pesos[2]} Kg\n Recorrido\n\n"
                          f"Zona sur:\n{utilitario_sur}\n{pesos[3]} Kg\n Recorrido")


def main() -> None:
    pesos = pesos_por_zona(["Parana"], ["Villa María"], ["Santa Rosa"])
    distribucion_camiones = camiones(pesos[0], pesos[1], pesos[2], pesos[3])
    escritura_archivo(distribucion_camiones, pesos)


main()