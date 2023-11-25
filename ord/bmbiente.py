import pyRofex
import bolsar
import bolsas as b
import time
import json
import enum
import os
pyRofex._set_environment_parameter("url", "https://api.bull.xoms.com.ar/", pyRofex.Environment.LIVE)
pyRofex._set_environment_parameter("ws", "wss://api.bull.xoms.com.ar/", pyRofex.Environment.LIVE)
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

        ambb = "pyRofex datos en VIVO BULL"
        try:
            #pyRofex._set_environment_parameter("url", "https://api.eco.xoms.com.ar", pyRofex.Environment.LIVE)
            #pyRofex._set_environment_parameter("ws", "wss://api.eco.xoms.com.ar", pyRofex.Environment.LIVE)
            pyRofex.initialize(user=b.ul4b,
                    password=b.pb4,
                      account=b.ulb,
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


            pyRofex.initialize(user=bolsar.ul4b,
                    password=bolsar.pb4,
                      account=bolsar.ulb,
                    environment=pyRofex.Environment.M4)

            #pyRofex._set_environment_parameter("proprietary", "ISV_PBCP", pyRofex.Environment.LIVE)


            print("conectado  {} ".format(ambb))

        except Exception as x:
            print("error")
            print(x)
            print("no es posible conectar:  {} \n Error: {} \n Qué falló?: {} "
            .format(ambb, type(x).__name__, x))
            exit()








    else:
        ambb = "pyRofex datos de Prueba"
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


def control_de_tenencias(archivo):
    posicion =  pyRofex.get_detailed_position()
    nombre_de_archivo=archivo

    print("posiciones")

    #print(posicion)

    posicion = posicion["detailedPosition"]
    print(posicion)
    #posicion = posicion["report"]
    try:
        accion=posicion["report"]["STOCK"]
    except:
        print("no hay acciones en CI")
        accion = {}

    try:
        cedear=posicion["report"]["CEDEAR"]
    except:
        print("no hay cedear en CI")
        cedear = {}

    try:
        bono=posicion["report"]["BOND"]
    except:
        print("no hay bonos en CI")
        bono= {}

    try:
        cauciones=posicion["report"]["REPURCHASE"]
    except:
        print("no hay cauciones en CI")
        cauciones= {}






    posi = {}

    for masa in accion:
        cantidadci = "0.0"  # Mover la declaración fuera del bucle interno

        for tt in range(len(accion[masa]['detailedPositions'])):
            if accion[masa]['detailedPositions'][tt]['settlType'] == 0:
                cantidadci = str(accion[masa]['detailedPositions'][tt]['totalCurrentSize'])

        print("MERV - XMEV - " + masa + " - 48hs" + ";" + cantidadci)
        posi["MERV - XMEV - " + masa + " - 48hs"] = cantidadci

        
    for kici in cedear:
        cantidadci = "0.0"  # Mover la declaración fuera del bucle interno

        for tt in range(0, len(cedear[kici]['detailedPositions'])) :
            if cedear[kici]['detailedPositions'][tt]['settlType'] ==0:
                cantidadci = str(cedear[kici]['detailedPositions'][tt]['totalCurrentSize'])


        #print(kici+ ";" + cantidadci )
        #posi[kici] = cantidadci
        print("MERV - XMEV - "+kici+" - 48hs" +";" + cantidadci )
        posi["MERV - XMEV - "+kici+" - 48hs"] = cantidadci

    for beto in bono:
        cantidadci = "0.0"  # Mover la declaración fuera del bucle interno

        for tt in range(0, len(bono[beto]['detailedPositions'])) :
            if bono[beto]['detailedPositions'][tt]['settlType'] ==0:
                cantidadci = str(bono[beto]['detailedPositions'][tt]['totalCurrentSize'])


        print("MERV - XMEV - "+beto+" - 48hs" +";" + cantidadci )
        posi["MERV - XMEV - "+beto+" - 48hs"] = cantidadci

    print(posi)


    # Abre el archivo de texto en modo escritura
    with open(nombre_de_archivo, "w") as archivo:
        # Guarda el diccionario en el archivo de texto
        json.dump(posi, archivo)
        archivo.close()
""" 
    # Abre el archivo en modo lectura
    with open(nombre_de_archivo, 'r') as f:
        # Lee el contenido del archivo
        contenido = f.read()
        # Cierra el archivo
        f.close()

    # Convierte el contenido del archivo en un diccionario
    mi_diccionario = eval(contenido)

    # Usa el diccionario resultante
    print("levantita")
    print(mi_diccionario) """
