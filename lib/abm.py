from os import path
from time import strptime
from csv import DictReader

PATH: str = "src\\pedidos.csv"
ROUTE = path.join(path.dirname(__file__), PATH)


class Pedidos:
    """El listado de pedidos del archivo csv. Valida que los valores
    sean ingresados correctamente.
    """
    lista: list[str] = []

    def __init__(self, pedidos: list[str]) -> None:
        lista: list[str] = [x.split(",") for x in pedidos]

        for i, p in enumerate(lista):

            fecha, codigo = p[1], p[5]
            cantidad, descuento = p[7], p[8]

            self.lista.append(",".join(p))
            if not self.__validar_fecha(fecha):
                print(f"El pedido {i+1} tiene errores de formato en la fecha.")
            if not self.__validar_codigo(codigo):
                print(f"El pedido {i+1} tiene un codigo de producto invalido.")
            if not self.__validar_numerico(cantidad, descuento):
                print(f"El pedido {i+1} tiene valores no numericos ingresados donde deberian"
                      " ser numericos.")

    def __validar_fecha(self, fecha: str) -> bool:
        """Valida que la fecha ingresada sea valida para evitar errores en comparaciones y otras funciones.

        Args:
            fecha (str)

        Returns:
            bool
        """
        try:
            strptime(fecha, "%d/%m/%Y")
        except ValueError:
            return False
        else:
            d, m, y = fecha.split("/")
            return len(d) == 2 and len(m) == 2 and len(y) == 4

    def __validar_numerico(self, *args) -> bool:
        """Valida que los valores ingresados sean numericos.
        """
        for arg in args:
            try:
                int(arg)
            except ValueError:
                return False

        return True

    def __validar_codigo(self, codigo: str) -> bool:
        """Prueba si el codigo sea un int y sea igual a 1334 o 568

        Args:
            codigo (str): el codigo de producto

        Returns:
            bool: si es un codigo valido o no
        """
        return codigo in ["1334", "568"] if self.__validar_numerico(codigo) else False


class Titulos(str):
    """Los titulos del csv. Verifica que tenga el largo adecuado.
    """

    def __init__(self, entrada: str) -> None:
        self.titulos: str = entrada.replace(', ', ',')


class Controlador:
    """El encargado principal del ABM
    """

    def __init__(self, route) -> None:
        self.route = route

        with open(self.route, 'r') as f:
            self.raw_pedidos: list[str] = f.read().splitlines()

        tmp_titulos = Titulos(self.raw_pedidos[0])
        tmp_pedidos = Pedidos(self.raw_pedidos[1:])

        self.titulos = tmp_titulos.titulos
        self.pedidos = tmp_pedidos.lista

        self.__actualizar()

    def ver_pedidos(self) -> None:
        print(self.titulos)
        for i, pedido in enumerate(self.pedidos):
            print(f'{str(i+1).zfill(3)} - {pedido}')

    def dict_data(self) -> list[dict[any]]:
        """Devuelve la informacion del archivo pedidos.csv en una lista de diccionarios, parecido a un json

        Returns:
            list[dict[any]]: 
        """

        lista = []

        with open(self.route, 'r') as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                l = {x: row[x] for x in self.titulos.split(',')}
                lista.append(l)

        return lista

    def __actualizar(self) -> None:
        """Actualiza el archivo csv
        """

        # fix curita que puede traer otros problemas
        self.pedidos = list(set(self.pedidos))

        with open(self.route, 'w') as f:
            f.writelines(self.titulos + '\n')
            for line in self.pedidos:
                f.writelines(line + '\n')

    def cargar(self, pedido: str) -> None:
        """Sirve para cargar pedidos al archivo pedidos.csv agregandolos al final del mismo.  

        Args:
            linea (str): el pedido a cargar. El formato deberia ser de acuerdo a la primera linea del archivo .csv
            propuesto en el metodo verificar_formato().
        """
        self.pedidos.append(pedido)
        self.__actualizar()

    def borrar(self, index: int) -> None:
        """Borra el pedido pasado como parametro del lista

        Args:
            index (int): indice del pedido que se quiere borrar
        """
        self.pedidos.pop(index)
        self.__actualizar()

    def modificar(self, index: int, key: str, valor: str) -> None:
        """Modifica un atributo dado de un pedido dado.

        Args:
            index (int): El indice en la lista del pedido dado. (numero de pedido - 1)
            key (str): El atributo que se quiere cambiar del pedido.
            valor (str): El nuevo valor que se le va a asignar al atributo.
        """
        valores_dict = self.dict_data().copy()
        valores_dict[index][key] = valor

        list(self.pedidos)[index] = ','.join(valores_dict[index].values())
        self.__actualizar()

    def __date_conversor(self, date: str) -> int:
        """Convierte una fecha de tipo dd/mm/yyyy a yyyymmdd para comparar mas facilmente

        Args:
            date (str): la fecha que se quiere cambiar. Formato dd/mm/yyyy

        Returns:
            int: fecha como un numero entero.
        """
        d, m, y = date.split('/')
        return int(y+m+d)

    def ordenar_por_antiguedad(self, ascendiente: bool = True) -> list[dict]:
        """Devuelve los pedidos ordenados en orden ascendiente segun la fecha en la que se entrego.

        Args:
            ascendiente (bool, optional): Define si el diccionario se devuelve ascendiendo o descendiendo. Defaults to True.

        Returns:
            list[dict]: Los pedidos ordenados segun su fecha
        """
        lista: list[dict] = self.dict_data().copy()
        return sorted(lista, key=lambda x: self.__date_conversor(x['Fecha']), reverse=not ascendiente)

    def articulo_mas_pedido(self) -> tuple[int, str]:
        """Devuelve el articulo mas pedido, junto con su color y la cantidad

        Returns:
            tuple[tuple[str, int], str]: ((color, cantidad), codigo)
        """
        listado = self.dict_data().copy()

        botellas, vasos = {}, {}

        for elemento in listado:
            try:
                # botellas
                if elemento["Cod. Articulo"] == '1334':
                    if elemento["Color"] not in botellas.keys():
                        botellas[elemento["Color"]] = int(elemento["Cantidad"])
                    else:
                        botellas[elemento["Color"]
                                 ] += int(elemento["Cantidad"])

                # vasos
                elif elemento["Cod. Articulo"] == '568':
                    if elemento["Color"] not in vasos.keys():
                        vasos[elemento["Color"]] = int(elemento["Cantidad"])
                    else:
                        vasos[elemento["Color"]] += int(elemento["Cantidad"])
            except ValueError:
                print("Hay un valor no-numerico ingresado en las cantidades.")

        # dos tuplas[max, codigo]
        max_botellas = max(botellas.items(), key=lambda x: x[1]), "1334"
        max_vasos = max(vasos.items(), key=lambda x: x[1]), "568"

        maximo_total = max([max_vasos, max_botellas], key=lambda x: x[0][1])

        return maximo_total


class User:
    def __init__(self, route) -> None:
        """Inicializa la clase con la ruta al archivo csv

        Args:
            route ([type]): Ruta al archvio csv
        """
        # abm
        self.ctrl: Controlador = Controlador(route)

        # titulos
        self.titulos = self.ctrl.titulos

    def cargar(self) -> None:
        """Cargar un pedido al archivo .csv
        """
        print("A continuacion se le pedira que ingrese los siguientes valores: ")
        print(self.titulos)

        req: dict[any] = {}
        titulos = self.titulos.split(',')

        for titulo in titulos:
            add = ""
            if titulo == 'Fecha':
                add = ' (dd/mm/yyyy)'
            req[titulo] = input(f"{titulo}{add}: ")

        self.ctrl.cargar(','.join(list(req.values())))

    def borrar(self) -> None:
        """Borra un pedido del archivo pedidos.csv
        """
        self.ctrl.ver_pedidos()
        print("Que pedido desea borrar?")
        try:
            rta = int(input(""))
        except ValueError:
            print("Ingrese un valor numerico.")
        else:
            if 1 <= rta <= len(list(self.ctrl.pedidos))+1:
                self.ctrl.borrar(rta-1)
                print(f"Se borró el pedido {rta}!")
            else:
                print("El valor no esta incluido")

    def modificar(self):  # TODO
        self.ctrl.ver_pedidos()
        titulos = self.titulos.split(',')
        try:
            print("Que numero de pedido desea modificar?")
            rta = int(input())
        except ValueError:
            print('Ingrese un valor numerico.')
        else:
            if 1 <= rta <= len(list(self.ctrl.pedidos)):

                print("Se pueden modificar los siguientes atributos del pedido:")
                print(", ".join(x for x in titulos))
                print("Cual desea cambiar?")
                atr: str = input("").title()
                if atr in titulos:
                    nuevo = input(f"Ingrese el nuevo valor de {atr}: ")
                    self.ctrl.modificar(rta-1, atr, nuevo)
                else:
                    print("Ese atributo no existe o esta mal escrito.")
            else:
                print("Ese pedido no existe.")

    def ordenado(self) -> None:
        """Imprime la lista ordenada por antiguedad
        """
        print("Quiere ver la lista")
        lista: list[dict] = self.ctrl.ordenar_por_antiguedad()
        print(self.titulos)
        for i, x in enumerate(lista):
            print(f"{str(i+1).zfill(2)} - {', '.join(list(x.values()))}")

    def dict_data(self) -> list[dict[any]]:
        return self.ctrl.dict_data()

    def maximo_pedido(self):
        maximo, codigo = self.ctrl.articulo_mas_pedido()

        print(f"El articulo mas pedido fue:")
        if codigo == "1334":
            print("Botella")
        else:
            print("Vaso")
        print(maximo[0])
        print(f"con {maximo[1]} pedidos.")


class MainApp(User):
    def __init__(self, route) -> None:
        super().__init__(route)
