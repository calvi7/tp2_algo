from os import path
from sys import platform

import distribucion_pesos as dp

from abm import MainApp

from el_contador import counter

# Para que distintos sistemas operativos puedan operar
# sin cambiar el archivo


def slash_gen() -> str:
    """Genera la barra del medio para los path"""
    if platform == "linux" or platform == "linux2":
        return "/"
    elif platform == "darwin":
        return "/"
    elif platform == "win32":
        return "\\"


# ruta al csv
SLASH = slash_gen()
CSV_ROUTE = f'src{SLASH}pedidos.csv'
ROUTE = path.join(path.dirname(__file__), CSV_ROUTE)


def date_conversor(date: str) -> int:
    """Convierte una fecha de tipo dd/mm/yyyy a yyyymmdd para comparar mas facilmente

    Args:
        date (str): la fecha que se quiere cambiar. Formato dd/mm/yyyy

    Returns:
        int: fecha como un numero entero.
    """
    d, m, y = date.split('/')
    return int(y+m+d)


def ordenar_por_antiguedad(pedidos, ascendiente: bool = True) -> list[dict]:
    """Devuelve los pedidos ordenados en orden ascendiente segun la fecha en la que se entrego.

    Args:
        ascendiente (bool, optional): Define si el diccionario se devuelve ascendiendo o descendiendo. Defaults to True.

    Returns:
        list[dict]: Los pedidos ordenados segun su fecha
    """
    return sorted(pedidos, key=lambda x: (date_conversor(x['Fecha']), x['Nro. Pedido']), reverse=not ascendiente)


def ver_completados() -> None:
    """Imprime los pedidos completados por orden de antiguedad
    """
    pedidos = dp.run()
    pedidos = ordenar_por_antiguedad(pedidos)
    for pedido in pedidos:
        print(",".join(pedido.values()))


def generar_menu() -> tuple:
    """Genera el menu con sus opciones

    Returns:
        tuple: devuelve la opcion elegida junto con el valor correspondiente a la opcion de salir
    """
    # declaro las opciones del menu
    menu = {
        1: "cargar pedido",
        2: "borrar pedido",
        3: "modificar pedido",
        4: "comprobar validez del lote y escribir archivos de vasos y botellas",
        5: "procesar los pedidos y generar archivo de salida",
        6: "ver los pedidos realizados ordenados segun su antiguedad",
        7: "ver articulo mas pedido",
    }

    # me aseguro que la ultima opcion sea salir
    menu[len(menu.keys())+1] = "salir"
    for opc, valor in menu.items():
        print(f"{opc}. {valor.capitalize()}")

    try:
        rta = int(input())
    except ValueError:
        print("Ingrese un valor numerico.")
    else:
        if rta in menu.keys():
            return rta, list(menu.keys())[-1]
        else:
            print("Esa opcion no existe.")
            return generar_menu(), list(menu.keys())[-1]


def main():
    # inicializo variable para el loop
    val = True
    
    # Inicializo la app
    APP = MainApp(ROUTE)

    # Inicializo el matcher
    matcher = counter.Matcher()
    
    # loop
    while val:
        opc, salir = generar_menu()

        # salir
        if opc == salir:
            print("Adios!")
            val = False

        if opc == 1:
            APP.cargar()

        elif opc == 2:
            APP.borrar()

        elif opc == 3:
            APP.modificar()

        elif opc == 4:
            matcher.contador()
            print("Listo!")

        elif opc == 5:
            dp.run()

        elif opc == 6:
            ver_completados()

        elif opc == 7:
            APP.maximo_pedido()


if __name__ == "__main__":
    main()
