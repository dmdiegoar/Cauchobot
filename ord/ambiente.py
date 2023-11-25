import pyRofex
import bolsar
import time
import json
import enum
import os
import bolsas as b


pyRofex._set_environment_parameter("url", "https://api.eco.xoms.com.ar/", pyRofex.Environment.LIVE)
pyRofex._set_environment_parameter("ws", "wss://api.eco.xoms.com.ar/", pyRofex.Environment.LIVE)
#ambiente

def ambiente(ambienteactivo):

#qmbiente = 0
    if ambienteactivo == 1:

        print("hoy")
        ahora = time.strftime("%c")
        print(ahora)
        print("hora")
        hora = time.strftime('%H:%M:%S', time.localtime())
        print(hora)

##        if hora > "23:00:00":
##            print("son mas de las 4, cierro todo")
##            exit()
##        elif hora < "11:00:00":
##            print("no son las 11, cierro todo")
##            exit()
##        else:
##            print("mercado abierto")

        ambb = "pyRofex datos en VIVO ecoLaisa"
        try:
            #pyRofex._set_environment_parameter("url", "https://api.eco.xoms.com.ar", pyRofex.Environment.LIVE)
            #pyRofex._set_environment_parameter("ws", "wss://api.eco.xoms.com.ar", pyRofex.Environment.LIVE)
            pyRofex.initialize(user=bolsar.ul4,
                    password=bolsar.pl4,
                      account=bolsar.ul,
                    environment=pyRofex.Environment.LIVE)

            pyRofex._set_environment_parameter("proprietary", "ISV_PBCP", pyRofex.Environment.LIVE)
            #pyRofex._set_environment_parameter("url", "https://api.eco.xoms.com.ar", pyRofex.Environment.LIVE)
            #pyRofex._set_environment_parameter("ws", "wss://api.eco.xoms.com.ar", pyRofex.Environment.LIVE)

            print("conectado  {} ".format(ambb))

        except Exception as x:
            print("no es posible conectar:  {} \n Error: {} \n Qué falló?: {} "
            .format(ambb, type(x).__name__, x))
            exit()

    elif ambienteactivo == 4:

        print("hoy")
        ahora = time.strftime("%c")
        print(ahora)
        print("hora")
        hora = time.strftime('%H:%M:%S', time.localtime())
        print(hora)

        if hora > "23:00:00":
            print("son mas de las 4, cierro todo")
            exit()
        elif hora < "11:00:00":
            print("no son las 11, cierro todo")
            exit()
        else:
            print("mercado abierto")

        ambb = "pyRofex datos en M4"
        try:


            pyRofex.initialize(user=bolsar.ul4,
                    password=bolsar.pl4,
                      account=bolsar.ul,
                    environment=pyRofex.Environment.M4)

            #pyRofex._set_environment_parameter("proprietary", "ISV_PBCP", pyRofex.Environment.LIVE)


            print("conectado  {} ".format(ambb))

        except Exception as x:
            print("error")
            print(x)
            print("no es posible conectar:  {} \n Error: {} \n Qué falló?: {} "
            .format(ambb, type(x).__name__, x))
            exit()

    elif ambienteactivo == 5:

            print("hoy")
            ahora = time.strftime("%c")
            print(ahora)
            print("hora")
            ambb = "pyRofex datos de Prueba BBQ"
            try:
                pyRofex.initialize(user=bolsar.upbb,
                        password=bolsar.ppbb,
                        account=bolsar.cpbb,
                        environment=pyRofex.Environment.REMARKET)

                print("conectado  {} ".format(ambb))

            except Exception as x:
                print("no es posible conectar:  {} \n Error: {} \n Qué falló?: {} "
                .format(ambb, type(x).__name__, x))
                exit()
    elif ambienteactivo == 10:

        print("hoy")
        ahora = time.strftime("%c")
        print(ahora)
        print("hora")
        hora = time.strftime('%H:%M:%S', time.localtime())
        print(hora)

##        if hora > "23:00:00":
##            print("son mas de las 4, cierro todo")
##            exit()
##        elif hora < "11:00:00":
##            print("no son las 11, cierro todo")
##            exit()
##        else:
##            print("mercado abierto")

        ambb = "pyRofex datos en VIVO ecoDS"
        try:
            #pyRofex._set_environment_parameter("url", "https://api.eco.xoms.com.ar", pyRofex.Environment.LIVE)
            #pyRofex._set_environment_parameter("ws", "wss://api.eco.xoms.com.ar", pyRofex.Environment.LIVE)
            pyRofex.initialize(user=b.ul4b,
                    password=b.pb4,
                      account=b.ued,
                    environment=pyRofex.Environment.LIVE)

            pyRofex._set_environment_parameter("proprietary", "ISV_PBCP", pyRofex.Environment.LIVE)
            #pyRofex._set_environment_parameter("url", "https://api.eco.xoms.com.ar", pyRofex.Environment.LIVE)
            #pyRofex._set_environment_parameter("ws", "wss://api.eco.xoms.com.ar", pyRofex.Environment.LIVE)

            print("conectado  {} ".format(ambb))

        except Exception as x:
            print("no es posible conectar:  {} \n Error: {} \n Qué falló?: {} "
            .format(ambb, type(x).__name__, x))
            exit()





    else:
        ambb = "pyRofex datos de Prueba DMD"
        try:
            pyRofex.initialize(user=bolsar.up,
                       password=bolsar.pp,
                      account=bolsar.cp,
                       environment=pyRofex.Environment.REMARKET)

            print("conectado  {} ".format(ambb))

        except Exception as x:
            print("no es posible conectar:  {} \n Error: {} \n Qué falló?: {} "
            .format(ambb, type(x).__name__, x))
            exit()











def get_total_size_by_settl_type(detailed_positions, settl_type=0):
    for position in detailed_positions:
        if position['settlType'] == settl_type:
            return str(position['totalCurrentSize'])
    return "0.0"

def process_positions(pos_dict, positions):
    for instrument, data in positions.items():
        detailed_positions = data.get('detailedPositions', [])
        for position in detailed_positions:
            cantidadci = get_total_size_by_settl_type(detailed_positions)
            trading_symbol = position.get('tradingSymbol', '')
            if trading_symbol:
                key = f"MERV - XMEV - {trading_symbol} - 48hs"
                print(key + ";" + cantidadci)
                pos_dict[key] = cantidadci

def control_de_tenenciasGTP():
    posicion = pyRofex.get_detailed_position()
    print("posiciones")
    print(posicion)

    accion = posicion.get("report", {}).get("STOCK", {})
    cedear = posicion.get("report", {}).get("CEDEAR", {})
    bono = posicion.get("report", {}).get("BOND", {})

    posi = {}

    process_positions(posi, accion)
    process_positions(posi, cedear)
    process_positions(posi, bono)

    print(posi)

    # Abre el archivo de texto en modo escritura
    with open('carteta.txt', "w") as archivo:
        # Guarda el diccionario en el archivo de texto
        json.dump(posi, archivo)

    # Abre el archivo en modo lectura
    with open('carteta.txt', 'r') as f:
        # Lee el contenido del archivo
        contenido = f.read()

    # Convierte el contenido del archivo en un diccionario
    mi_diccionario = json.loads(contenido)

    # Usa el diccionario resultante
    print("levantita")
    print(mi_diccionario)
