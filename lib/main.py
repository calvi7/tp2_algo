import pruebas_geo

from abm import MainApp
from os import path


# la ruta al csv. Funciona para sistemas operativos Windows
CSV_ROUTE = 'src\\pedidos.csv'
ROUTE = path.join(path.dirname(__file__), CSV_ROUTE)

# inicializo la MainApp
APP = MainApp(ROUTE)


def generar_menu() -> int:
    # declaro las opciones del menu
    menu = {
        1: "cargar pedido",
        2: "borrar pedido",
        3: "modificar pedido",
        4: "comprobar validez del lote",
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
            return rta
        else:
            print("Esa opcion no existe.")
            return generar_menu()


generar_menu()
