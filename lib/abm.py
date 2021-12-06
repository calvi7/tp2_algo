import csv


class MainApp:

    def __init__(self, _path: str) -> None:
        """Constructor de la clase MainApp

        Args:
            _path str: la direccion al archivo pedidos.csv
        """
        # el archivo con los pedidos
        self.route: str = _path
        # los pedidos en una lista
        with open(self.route, 'r') as f:
            self.info_pedidos: list[str] = f.read().splitlines()
        self.titulos = self.info_pedidos[0]
        self.pedidos_totales = self.info_pedidos[1:]

    def menu(self) -> None:
        """Genera las opciones del menu y hace que dirigan a lo que se pide. 
        El while loop NO esta incluido en la funcion, se debe envolver a la funcion en uno si se necesita
        """
        opciones = {
            1: 'cargar',
            2: 'borrar',
            3: 'modificar pedido',
            4: 'ver pedidos',
            5: 'ver pedidos ordenados por antiguedad',
        }
        # se agrega la opcion de salir afuera para que siempre sea la ultima
        # asi se pueden agregar mas opciones antes sin tener que cambiar todo
        opciones[len(opciones) + 1] = 'salir'
        print("Opciones:")
        for key, value in opciones.items():
            print(f"{key}. {value.capitalize()}")
        try:
            rta = int(input(""))
        except ValueError:
            print("El valor ingresado debe ser numerico.")
        else:
            if rta in list(opciones.keys()):
                if rta == 1:
                    # return self.cargar() TODO
                    print("FALTA")
                elif rta == 2:
                    return self.borrar()
                elif rta == 3:
                    return self.modificar_pedido()
                elif rta == 4:
                    return self.ver_pedidos()
                elif rta == len(opciones) + 1:
                    print('Adios!')
                    # quit()
            else:
                print("Esa opcion no esta incluida.")

    def cargar_por_parametros(self, linea: str) -> None:
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
        for i, pedido in enumerate(self.pedidos_totales):
            print(f'{str(i+1).zfill(3)} - {pedido}')

    def actualizar_pedidos(self):
        with open(self.route, 'w') as f:
            f.writelines(self.titulos + '\n')
            for line in self.pedidos_totales:
                f.writelines(line + '\n')

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
                self.actualizar_pedidos()
                print(f"Se borró el pedido {rta}!")
            else:
                print("El valor no esta incluido")

    def dict_data(self) -> list[dict[any]]:
        """Devuelve la informacion del archivo pedidos.csv en una lista de diccionarios, parecido a un json

        Returns:
            list[dict[any]]: 
        """
        titulos = self.titulos.split(',')
        lista = []
        with open(self.route, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                l = {x: row[x] for x in titulos}
                lista.append(l)

        return lista

    def date_conversor_(self, date: str) -> int:
        """Convierte una fecha de tipo dd/mm/yyyy a yyyymmdd para comparar mas facilmente

        Args:
            date (str): la fecha que se quiere cambiar. Formato dd/mm/yyyy

        Returns:
            int: fecha como un numero entero.
        """
        d, m, y = date.split('/')
        return int(y+m+d)

    def ordenado_por_antiguedad(self, ascendiente: bool = True) -> list[dict]:
        """Devuelve los pedidos ordenados en orden ascendiente segun la fecha en la que se entrego.

        Args:
            ascendiente (bool, optional): Define si el diccionario se devuelve ascendiendo o descendiendo. Defaults to True.

        Returns:
            list[dict]: Los pedidos ordenados segun su fecha
        """
        listado: list[dict] = self.dict_data()
        return sorted(listado, key=lambda x: self.date_conversor_(x['Fecha']), reverse=not ascendiente)

    def modificar_pedido(self):  # TODO
        self.ver_pedidos()
        print("El formato debe ser el siguiente:")
        self.verificar_formato()
        titulos = self.info_pedidos[0].split(',')
        try:
            pedido = int(input('Que numero de pedido desea modificar?'))
        except ValueError:
            print('Ingrese un valor numerico.')
        else:
            if 1 <= pedido <= len(self.pedidos_totales):
                self.pedidos_totales[pedido-1] = {}
                for title in titulos:
                    print(f'{title}: ')
                    self.pedidos_totales[pedido-1][title] = input()
