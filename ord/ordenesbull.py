import bolsas as b
import pyRofex
import json
import enum
import bmbiente
import time
import pytz
import datetime
import os
import sheetsfunciones
import fordenes as fo






date_time = datetime.datetime.now(
            pytz.timezone('America/Argentina/Buenos_Aires'))




print("cancelando las ordenes de la cuenta Bull")
bmbiente.ambiente(1)
ahorab = date_time.time().strftime(b.TIME_FORMAT)

semi = 'MERV - XMEV - SEMI - CI'
al30 = 'MERV - XMEV - AL30 - CI'


#fo.cancelar_todo()

fo.cancelar_lado()  #cancela solo venta por defecto. Sino hay que ingresar parámetro "BUY"

#fo.cancelar_papel(semi)