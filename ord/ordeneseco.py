
import bolsas as b
import pyRofex
import json
import enum
import ambiente
import time
import pytz
import datetime
import os
import sheetsfunciones
import fordenes as fo





# print("descargando la tenencia de la cuenta Laisa ECO")
# ambiente.ambiente(1)
# bolsar.control_de_tenencias("cartetaralaisa.txt")

# time.sleep(3)

print("Cancelando las ordenes de la cuenta DM ECO")
ambiente.ambiente(10)
date_time = datetime.datetime.now(
            pytz.timezone('America/Argentina/Buenos_Aires'))

semi = 'MERV - XMEV - SEMI - CI'
al30 = 'MERV - XMEV - AL30 - CI'


#fo.cancelar_todo()

fo.cancelar_lado()  #cancela solo venta por defecto. Sino hay que ingresar parámetro "BUY"

#fo.cancelar_papel(semi)



