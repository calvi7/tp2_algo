from abm import MainApp
from os import path

# path
local_path = path.join(path.dirname(__file__), "src\\pedidos.csv")

# init
app = MainApp(local_path)

# dict de pedidos
pedidos = app.dict_data()

# inicializo
total_vasos = 0
total_botellas = 0

# itero el diccionario de pedidos
for pedido in pedidos:
    # botellas
    if pedido['Cod. Articulo'] == '1334':
        total_botellas += int(pedido['Cantidad'])
    # vasos
    elif pedido['Cod. Articulo'] == '568':
        total_vasos += int(pedido['Cantidad'])

# en gramos
peso_vasos = total_vasos * 450
peso_botellas = total_botellas * 350
print(peso_vasos, peso_botellas)
