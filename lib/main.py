# import pruebas_geo

from abm import MainApp
from os import path


# la ruta al csv. Funciona para sistemas operativos Windows
CSV_ROUTE = 'src\\pedidos.csv'
ROUTE = path.join(path.dirname(__file__), CSV_ROUTE)

# inicializo la MainApp
APP = MainApp(ROUTE)


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
            return rta, list(menu.keys())[-1]
        else:
            print("Esa opcion no existe.")
            return generar_menu(), list(menu.keys())[-1]


def main():
    # inicializo variable para el loop
    val = True

    # loop
    while val:
        opc, salir = generar_menu()

        if opc == salir:
            print("Adios!")
            val = False

        if opc == 1:
            APP.cargar()
        if opc == 2:
            APP.borrar()
        if opc == 3:
            APP.modificar()


main()
