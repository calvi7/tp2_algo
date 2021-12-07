import csv


class MainApp:

    # constructor
    def __init__(self, __path: str) -> None:
        """Constructor de la clase MainApp

        Args:
            _path str: la direccion al archivo pedidos.csv
        """
        # el archivo con los pedidos
        self.route: str = __path
        # los pedidos en una lista
        with open(self.route, 'r') as f:
            self.info_pedidos: list[str] = f.read().splitlines()
        self.titulos = self.info_pedidos[0].replace(', ', ',')
        self.pedidos_totales = self.info_pedidos[1:]
        
        self.actualizar_pedidos()


    # metodos de visualizacion de datos
    def verificar_formato(self, linea) -> bool:
        """Valida que el formato de un pedido ingresado

        Args:
            linea (str): el pedido que se va a validar
            
        Returns:
            bool: True si el formato es valido, False si no
        """
        linea = linea.split(',')
        col1 = isinstance (linea[0], int)
        col2 = True # TODO
        col6 = isinstance (linea[5], int)
        col8 = isinstance (linea[7], int)
        col9 = isinstance (linea[8], int)
        return col1 and col2 and col6 and col8 and col9

    def ver_pedidos(self) -> None:
        """Ver los pedidos cargados hasta el momento con un formato mas legible
        """
        print(self.titulos)
        for i, pedido in enumerate(self.pedidos_totales):
            print(f'{str(i+1).zfill(3)} - {pedido}')
            
    def dict_data(self) -> list[dict[any]]:
        """Devuelve la informacion del archivo pedidos.csv en una lista de diccionarios, parecido a un json

        Returns:
            list[dict[any]]: 
        """
        lista = []
        with open(self.route, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                l = {x: row[x] for x in self.titulos.split(',')}
                lista.append(l)

        return lista

    def __date_conversor(self, date: str) -> int:
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
        return sorted(listado, key=lambda x: self.__date_conversor(x['Fecha']), reverse=not ascendiente)


    # metodos de abm
    def actualizar_pedidos(self):
        with open(self.route, 'w') as f:
            f.writelines(self.titulos + '\n')
            for line in self.pedidos_totales:
                f.writelines(line + '\n')
                
    def cargar_por_parametros(self, linea: str) -> None:
        """Sirve para cargar pedidos al archivo pedidos.csv agregandolos al final del mismo.  

        Args:
            linea (str): el pedido a cargar. El formato deberia ser de acuerdo a la primera linea del archivo .csv
            propuesto en el metodo verificar_formato().
        """
        with open(self.route, "a") as f:
            f.writelines(linea + '\n')

    def cargar(self) -> None:
        """Cargar un pedido al archivo .csv
        """
        req: dict[any] = {}
        titulos = self.titulos.split(',')
        add = ""
        for titulo in titulos:
            if titulo == 'Fecha':
                add = ' (dd/mm/yyyy)'
            req[titulo] = input(f"{titulo}{add}: ")
            add = ""
        self.pedidos_totales.append(','.join(list(req.values())))
        self.actualizar_pedidos()
    
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
            if 1 <= rta <= len(self.pedidos_totales)+1:
                self.pedidos_totales.pop(rta-1)
                self.actualizar_pedidos()
                print(f"Se borró el pedido {rta}!")
            else:
                print("El valor no esta incluido")

    def modificar_pedido(self):  # TODO
        self.ver_pedidos()
        print("El formato debe ser el siguiente:")
        self.verificar_formato()
        titulos = self.titulos.split(',')
        try:
            rta = int(input('Que numero de pedido desea modificar?'))
        except ValueError:
            print('Ingrese un valor numerico.')
        else:
            pass

    
    # menu
    def menu(self) -> bool:
        """Genera un menu en el se incluyen funcionalidades de ABM para el archivo .csv
        El loop NO esta incluido, pero devuelve un booleano para saber si continua o no

        Returns:
            bool: Define si sigue el loop o no
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
                    self.cargar()
                elif rta == 2:
                    self.borrar()
                elif rta == 3:
                    self.modificar_pedido()
                elif rta == 4:
                    self.ver_pedidos()
                elif rta == 5:
                    print("TODO")
                elif opciones[rta] == 'salir':
                    print('Adios!')
                    return False
                return True
            else:
                print("Esa opcion no esta incluida.")
