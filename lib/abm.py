from os import path


class MainApp:
    local_count = 0
    pedidos = path.join(path.dirname(__file__), 'src\\pedidos.csv')

    def __init__(self):
        self.route = MainApp.pedidos

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
        with open(self.route, 'r') as f:
            formato = f.read().splitlines()

        print(formato[0])
