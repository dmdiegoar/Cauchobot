import threading
import time
import pandas as pd
import pyRofex
import ambiente

import bolsar



class Esta:
    def __init__(self, papel, cantidad, margen):
        self.papel = papel
        self.cantidad = cantidad
        self.margen = margen
        self.estado = "off"

    def imprimir_estado(self):
        print(f"Estado de {self.papel}: {self.estado}")

    def modificar_estado(self, nuevo_estado):
        print("Verificando estado " + self.papel)
        if nuevo_estado != self.estado:
            print("cambio de estado " + self.papel)
            print(" estado viejo  " + self.estado)
            print(nuevo_estado)
            if nuevo_estado == "on":
                print("arranca?")
                self.arrancar()
            elif nuevo_estado == "off":
                print("detenta")
                self.detener()
            self.estado = nuevo_estado

    def arrancar(self):
        print(f"Iniciando conexión para {self.papel}")
        print("iniciando la conección")

        pyRofex.set_default_environment(pyRofex.Environment.LIVE)

                # 10 conecta a Ecodm
        ambiente.ambiente(10)

        # Initialize Websocket Connection with the handler
        pyRofex.init_websocket_connection(
                market_data_handler=self.market_data_handler,
                error_handler=self.error_handler,
                exception_handler=self.exception_handler,
                order_report_handler=self.order_report_handler
                )
        # Subscribe Market Data
        pyRofex.market_data_subscription(
            tickers=[
                    self.papel
                ],
            entries=[
                    #pyRofex.MarketDataEntry.BIDS,
                    pyRofex.MarketDataEntry.OFFERS
                ]
                )

            # Subscribes to receive order report for the default account
        pyRofex.order_report_subscription()
    
    # Defines the handlers that will process the messages.
    def market_data_handler(self, message):
        print("mensaje recibido " + self.papel)
        print(message)

    def order_report_handler(self, order_report):
        print("novedad de orden " + self.papel)

    def error_handler(self, message):
        print("Error Message Received: {0}".format(message))


    def exception_handler(self, e):
        print("Exception Occurred: {0}".format(e.message))

    def detener(self):
        print(f"Finalizando conexión para {self.papel}")
        pyRofex.close_websocket_connection()
        print("coneccion cerrada")

class Controlador:
    def __init__(self, MORI, COME, archivo_csv):
        self.MORI = MORI
        self.COME = COME
        self.archivo_csv = archivo_csv
        self.leer_csv_actualizar_valores()

    def leer_csv_actualizar_valores(self):
        while True:
            datos = pd.read_csv(self.archivo_csv)
            print(datos)

            for index, row in datos.iterrows():
                papel = row['papel']
                estado = row['estado']
                cantidad = row['cantidad']

                print(papel)
                print(self.MORI.papel)

                if papel == self.MORI.papel:
                    if estado != self.MORI.estado:
                        self.MORI.modificar_estado(estado)

                elif papel == self.COME.papel:
                    if estado != self.COME.estado:
                        self.COME.modificar_estado(estado)

            time.sleep(8)

# Ejemplo de uso:

# Instancias de la clase Esta
MORI = Esta('MERV - XMEV - MORI - 48hs', 0, 0.5)  # Inicialmente, la cantidad se asigna como 0
COME = Esta('MERV - XMEV - COME - 48hs', 0, 0.5)  # Inicialmente, la cantidad se asigna como 0

# Instancia del controlador
controlador = Controlador(MORI, COME, "C:/Users/Administrator/manbru/o1/archive.cvs")

# Este ejemplo no imprime nada porque el bucle está en espera
