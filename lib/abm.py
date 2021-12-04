from os import path


class MainApp:

    def __init__(self) -> None:
        # el archivo con los pedidos
        self.route: str = path.join(path.dirname(__file__), 'src\\pedidos.csv')
        # los pedidos en una lista
        with open(self.route, 'r') as f:
            self.info_pedidos: list[str] = f.read().splitlines()

    def menu(self) -> None:
        """Genera las opciones del menu y hace que dirigan a lo que se pide. 
        El while loop NO esta incluido en la funcion, se debe envolver a la funcion en uno si se necesita
        """
        opciones = {
            1: 'cargar',
            2: 'borrar',
            3: 'ver pedidos',
        }
        # se agrega la opcion de salir afuera para que siempre sea la ultima
        # asi se pueden agregar mas opciones antes sin tener que cambiar todo
        opciones[len(opciones) + 1] = 'salir'
        n_opciones = list(opciones.keys())
        print("Opciones:")
        for key, value in opciones.items():
            print(f"{key}. {value.capitalize()}")
        try:
            rta = int(input(""))
        except ValueError:
            print("El valor ingresado debe ser numerico.")
        else:
            if rta in n_opciones:
                if rta == 1:
                    return self.cargar()
                elif rta == 2:
                    return self.borrar()
                elif rta == 3:
                    return self.ver_pedidos()

    def cargar(self, linea: str) -> None:
        """Sirve para cargar pedidos al archivo pedidos.csv agregandolos al final del mismo.  

        Args:
            linea (str): el pedido a cargar. El formato deberia ser de acuerdo a la primera linea del archivo .csv
            propuesto en el metodo verificar_formato().
        """
        with open(self.route, "a") as f:
            f.writelines(linea + '\n')

    def verificar_formato(self) -> None:
        """Simplemente dice como se deberia cargar cada pedido.
        """
        print(self.info_pedidos[0])

    def ver_pedidos(self) -> None:
        """Ver los pedidos cargados hasta el momento.
        """
        print(self.info_pedidos[0])
        for i, pedido in enumerate(self.info_pedidos[1:]):
            print(f'{str(i+1).zfill(2)} - {pedido}')

    def borrar(self) -> None:
        """Borra un pedido del archivo pedidos.csv
        """
        self.ver_pedidos()
        print("Que pedido desea borrar?")
        try:
            rta = int(input(""))
        except ValueError:
            print("Ingrese un valor numerico.")
        else:
            if 1 <= rta <= len(self.info_pedidos)-1:
                self.info_pedidos.pop(rta-1)
                with open(self.route, 'w') as f:
                    for line in self.info_pedidos:
                        f.writelines(line + '\n')
                print(f"Se borró el pedido {rta}!")
            else:
                print("El valor no esta incluido")
