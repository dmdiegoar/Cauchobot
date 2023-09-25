#!/usr/bin/env python3

import datetime
import logging
import os
import os.path
import pickle
import sys
import time
from logging.handlers import RotatingFileHandler

import gspread
import pandas as pd
import pyRofex
import pytz
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials

#import parameters
import bmbiente
import bolsar
from telegramfunciones import initialize_telegram
import warnings

warnings.simplefilter("ignore")



DRY_RUN = bolsar.DRY_RUN
if sys.argv[-1] == 'test':
    DRY_RUN = True


WAIT_TIME = bolsar.WAIT_TIME  # frecuencia de actualizacion
TIME_FORMAT = '%Y/%m/%d - %H:%M:%S'

inicio = datetime.time.fromisoformat(
    bolsar.HORA_INICIO)  # inicio horario de actualizacion
fin = datetime.time.fromisoformat(
    bolsar.HORA_FIN)  # fin horario de actualizacion


sheets_credentials = bolsar.sheets_credentials  # json credenciales sheets
sheets_workbook = bolsar.sheets_workbook1  # url de la planilla
sheets_worksheet = bolsar.sheets_worksheet1  # nombre de la solapa
sheets_ranges = bolsar.sheets_ranges1  # lista de rangos a limpiar
# url de la planilla de pruebas
sheets_test_workbook = bolsar.sheets_workbook_test1


# pickle filenames
all_instruments_pickle = f'{datetime.date.fromtimestamp(time.time()).isoformat()}_all_instruments.pkl'
detailed_instruments_pickle = f'{datetime.date.fromtimestamp(time.time()).isoformat()}_detailed_instruments.pkl'


my_tickers = [
    {'stock': 'GGAL', 'options': 'GFG'}
]


#####
# logger parameters
#####

logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')

log_file = bolsar.log_file

if os.name == 'nt':
    log_file = '.' + log_file

if bolsar.log_rotation:
    log_file_handler = RotatingFileHandler(
        filename=log_file, maxBytes=bolsar.log_rotation_size, backupCount=bolsar.log_rotation_backups)
else:
    log_file_handler = logging.FileHandler(filename=log_file)

log_file_handler.setFormatter(log_formatter)
logger.addHandler(log_file_handler)

if DRY_RUN:
    # anula horarios -- reemplazar
    inicio = datetime.time.fromisoformat(
        "00:00:00")  # inicio horario de actualizacion
    fin = datetime.time.fromisoformat(
        "23:59:59")  # fin horario de actualizacion
    # modifica planilla a escribir
    sheets_workbook = sheets_test_workbook

    # parametros logger debug stdout
    logger.setLevel(logging.DEBUG)
    log_stdout_handler = logging.StreamHandler(sys.stdout)
    log_stdout_handler.setFormatter(log_formatter)
    logger.addHandler(log_stdout_handler)


#####
# Funciones
#####


# 1-Initialize the environment
bmbiente.ambiente(1)


# 2-Defines the handlers that will process the messages and exceptions.
def order_report_handler(message):
    print("Order Report Message Received")
    global df_trade_report

    # logger.info(message)
    clOrdId = 0 if not 'clOrdId' in message['orderReport'] else message['orderReport']['clOrdId']
    ticker = message['orderReport']['instrumentId']['symbol']
    tipo = "indefinido" if not 'side' in message['orderReport'] else message['orderReport']['side']
    precio = 0.0 if not 'price' in message['orderReport'] else message['orderReport']['price']
    cantidad = 0 if not 'orderQty' in message['orderReport'] else message['orderReport']['orderQty']
    status = "indefinido" if not 'status' in message['orderReport'] else message['orderReport']['status']
    cant_acumulada = 0 if not 'cumQty' in message['orderReport'] else message['orderReport']['cumQty']
    cant_restante = 0 if not 'leavesQty' in message['orderReport'] else message['orderReport']['leavesQty']
    precio_promedio = 0.0 if not 'avgPx' in message['orderReport'] else message['orderReport']['avgPx']
    hora = 0 if not 'timestamp' in message['orderReport'] else message['orderReport']['timestamp']
    comentario = "indefinido" if not 'text' in message['orderReport'] else message['orderReport']['text']
    cuenta = 0 if (not 'accountId' in message['orderReport'] or not 'id' in message['orderReport']['accountId'])  else message['orderReport']['accountId']['id']
    wsClOrdId = "indefinido" if not 'wsClOrdId' in message['orderReport'] else message['orderReport']['wsClOrdId']
    print(ticker)
    print("fin del msg")


def error_handler(message):
    print("Error Message Received: {0}".format(message))


def exception_handler(e):
    print("Exception Occurred: {0}".format(e.msg))


# 3-Initialize Websocket Connection with the handlers
pyRofex.init_websocket_connection(order_report_handler=order_report_handler,
                                  error_handler=error_handler,
                                  exception_handler=exception_handler)


# 4-Subscribes to receive order report for the default account
pyRofex.order_report_subscription()
