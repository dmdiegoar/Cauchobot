from collections import defaultdict

from telegramfunciones import initialize_telegram

import pyRofex
import bolsar
import time
contador =0

eco = True
#eco = "no"

alertelegram = initialize_telegram(
    bolsar.telk, bolsar.telegram_group_log)

if eco== True:
    pyRofex._set_environment_parameter("url", "https://api.eco.xoms.com.ar/", pyRofex.Environment.LIVE)
    pyRofex._set_environment_parameter("ws", "wss://api.eco.xoms.com.ar/", pyRofex.Environment.LIVE)  

    pyRofex.initialize(user=bolsar.ul4b,
                   password=bolsar.pb4,
                   account=bolsar.ued,
                   environment=pyRofex.Environment.LIVE)

else:

#######bullll

    print("mameluko")

print("cone rado")

todas = pyRofex.get_all_orders_status()
#todastus = todas["status"]
#print(todastus)
tu_objeto = todas["orders"]

# Diccionario anidado para contar {symbol: {status: count}}

contador = defaultdict(lambda: defaultdict(int))

for order in tu_objeto:
     #print("####$$$###$$$$##$$")
     symbol = order["instrumentId"]["symbol"]
     status = order["status"]
     #print(symbol)
     #print(status)

     # Incrementar el contador correspondiente
     contador[symbol][status] += 1

#print(contador)

#print(tu_objeto)


def contar_ocurrencias_por_symbol_y_status(orders):
    # Diccionario anidado para contar {symbol: {status: count}}
    #contador = defaultdict(lambda: defaultdict(int))
    
    for order in orders:
        print(order)
        symbol = order['instrumentId']['symbol']
        status = order['status']
        
        
        # Incrementar el contador correspondiente
        contador[symbol][status] += 1
    
    return contador

def imprimir_tabla(contador):
    # Obtener todas las columnas (todos los status únicos)
    all_statuses = set()
    for status_dict in contador.values():
        all_statuses.update(status_dict.keys())
    
    # Convertir el set de statuses a una lista ordenada
    all_statuses = sorted(all_statuses)
    
    # Encabezados de la tabla
    header = "Symbol".ljust(30) + "".join([status.ljust(15) for status in all_statuses])
    print(header)
    alertelegram.alert_message(header)
    print("-" * len(header))
    
    # Imprimir cada fila (cada symbol)
    for symbol, status_dict in contador.items():
        row = symbol.ljust(30)
        for status in all_statuses:
            count = status_dict.get(status, 0)
            row += str(count).ljust(15)
        print(row)
        alertelegram.alert_message(row)

# Tu diccionario de órdenes


# Llamada a la función para contar las ocurrencias
#contador = contar_ocurrencias_por_symbol_y_status(tu_objeto['orders'])

# Imprimir la tabla
imprimir_tabla(contador)

  

#######bullll

pyRofex._set_environment_parameter("url", "https://api.bull.xoms.com.ar/", pyRofex.    Environment.LIVE)
pyRofex._set_environment_parameter("ws", "wss://api.bull.xoms.com.ar/", pyRofex.Environment.LIVE)  





pyRofex.initialize(user=bolsar.ul4b,
                       password=bolsar.pb4,
                       account=bolsar.ulb,
                       environment=pyRofex.Environment.LIVE)
                   
print("buuuuu")
time.sleep(12)
alertelegram.alert_message("------------------")
todas = pyRofex.get_all_orders_status()
#todastus = todas["status"]
#print(todastus)
tu_objeto = todas["orders"]

contador = defaultdict(lambda: defaultdict(int))

for order in tu_objeto:
     #print("####$$$###$$$$##$$")
     symbol = order["instrumentId"]["symbol"]
     status = order["status"]
     #print(symbol)
     #print(status)

     # Incrementar el contador correspondiente
     contador[symbol][status] += 1



imprimir_tabla(contador)




