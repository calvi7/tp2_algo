from os import path


class MainApp:
    pedidos: str = path.join(path.dirname(__file__), 'src\\pedidos.csv')

    def __init__(self):
        self.route: str = self.pedidos
        with open(self.route, 'r') as f:
            self.info_pedidos = f.read().splitlines()

    def cargar(self, linea: str):
        """Sirve para cargar pedidos al archivo pedidos.csv agregandolos al final del mismo.  

        Args:
            linea (str): el pedido a cargar. El formato deberia ser de acuerdo a la primera linea del archivo .csv
            propuesto en el metodo verificar_formato().
        """
        with open(self.route, "a") as f:
            f.writelines(linea + '\n')

    def verificar_formato(self):
        """Simplemente dice como se deberia cargar cada pedido.
        """
        print(self.info_pedidos[0])

    def ver_pedidos(self):
        """Ver los pedidos cargados hasta el momento.
        """
        print(self.info_pedidos[0])
        for i, pedido in enumerate(self.info_pedidos[1:]):
            print(f'{str(i+1).zfill(2)} - {pedido}')

    def borrar(self):
        """Borra un pedido del archivo pedidos.csv
        """
        print("NICE")
        self.ver_pedidos()
        print("Que pedido desea borrar?")
        try:
            rta = int(input(""))
        except ValueError:
            print("Ingrese un valor numerico.")
        else:
            if 0 > rta > len(self.info_pedidos) - 1:
                print("El valor no esta incluido")
                # TODO no se tiene que romper cuando se ingresa un valor no valido
            else:
                self.info_pedidos.pop(rta-1)
                with open(self.route, 'w') as f:
                    for line in self.info_pedidos:
                        f.writelines(line + '\n')
