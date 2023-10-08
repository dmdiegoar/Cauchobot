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

colgadas=0

sheets_credentials = bolsar.sheets_credentials  # json credenciales sheets
sheets_workbook = bolsar.sheets_workbook1  # url de la planilla
sheets_worksheet = bolsar.sheets_worksheet1  # nombre de la solapa
sheets_ranges = bolsar.sheets_ranges1  # lista de rangos a limpiar
# url de la planilla de pruebas
sheets_test_workbook = bolsar.sheets_workbook_test1


# pickle filenames
all_instruments_pickle = f'{datetime.date.fromtimestamp(time.time()).isoformat()}_all_instruments.pkl'
detailed_instruments_pickle = f'{datetime.date.fromtimestamp(time.time()).isoformat()}_detailed_instruments.pkl'

# Create an empty DataFrame to hold the trade report data
_trade_report_columns = ['orderId', 'ticker', 'Tipo', 'Precio', 'Cant', 'Status', 'Cant Acum', 'Cant Rest', 'Px Prom',
                         'Fecha', 'error', 'Cta', 'wsClOrdId']
df_trade_report = pd.DataFrame(columns=_trade_report_columns)
#print("dataf creado")
#print(df_trade_report)
#time.sleep(3)


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

def read_pickle(filename):
    """Lee pickle y devuelve datos

    Args:
        filename (str): nombre del archivo pickle

    Returns:
        object: contenido del pickle
    """
    with open(filename, 'rb') as handle:
        _ = pickle.load(handle)
    return _


def write_pickle(filename, object):
    """Graba pickle

    Args:
        filename (str): nombre del archivo pickle
        object (object): contenido del pickle
    """
    with open(filename, 'wb') as handle:
        pickle.dump(object, handle)


def initialize_google_sheets():
    """_summary_

    Returns:
        _type_: _description_
    """
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        sheets_credentials, scope)

    client = gspread.authorize(creds)
    workbook = client.open_by_key(sheets_workbook)
    sheet = workbook.worksheet(sheets_worksheet)
    return sheet


def update_range_from_df_google_sheets(sheet, df):
    """_summary_

    Args:
        sheet (_type_): _description_
        df (_type_): _description_
    """
    set_with_dataframe(sheet, df, include_index=False)


def update_cell_google_sheets(sheet, cell, value):
    """_summary_

    Args:
        sheets (_type_): _description_
        cell (_type_): _description_
    """
    sheet.update(cell, value)

def disconnect():
    pyRofex.close_websocket_connection()
    logger.info(f"- Finalizado: {date_time.strftime(TIME_FORMAT)}")
    telegram.notification_message('Script cerrado')
    exit(0)


#####
# Conexion xOMS
#####

logger.info('[*] Inicializando pyRofex')

# 1-Initialize the environment
bmbiente.ambiente(1)

#####
# Websockets handlers
#####

# 2-Defines the handlers that will process the messages and exceptions.
def order_report_handler(message):
    #print("Order Report Message Received")

    global df_trade_report
    global colgadas

    #print("glon")
    #print(df_trade_report)
    #time.sleep(3)
    if "df_trade_report" not in globals():
        df_trade_report = pd.DataFrame(columns=_trade_report_columns)


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
    #print(ticker)
    #print("fin del msg")
    try:
        #print("mandando alertas a telegram " + ticker)
        if status in ("FILLED", "PARTIALLY_FILLED"):
            telegramlibro.notification_message( ticker +" \n"+ 
            tipo +" " + tipo + " " + tipo +   tipo +" " + tipo + " " + 

            "\n Precio: "+ str(max(precio, precio_promedio))
            +"\n Cantidad : "+ str(cantidad)
            +"\n operado: "+ str(cant_acumulada)
            +"\n resta: "+ str(cant_restante)
            +"\n "+ status
            +"\n "+ comentario      )
        

    except:
        print("falló el alerta de la orden " + ticker)

    # Check if orderId already exists in the DataFrame
    #print("arde df")

    if status=="REJECTED":
        telegram.alert_message( ticker +" \n"+ 
            tipo +" " + tipo + " " + tipo +  tipo +" " + tipo + " " + 

            "\n Precio: "+ str(max(precio, precio_promedio))
            +"\n Cantidad: "+ str(cantidad)
            +"\n operado: "+ str(cant_acumulada)
            +"\n resta: "+ str(cant_restante)
            +"\n "+ status
            +"\n "+ comentario      )
        if tipo=="BUY":
            telegram.alert_message("ORDEN DE COMORA RECHAZADA, VERRR")

    else:
        if clOrdId in df_trade_report['orderId'].values:
            
        #print("actuañizo orden")
        # Update the existing row with the matching orderId
            df_trade_report.loc[df_trade_report['orderId'] == clOrdId] = [clOrdId, ticker, tipo, precio, cantidad, status, cant_acumulada,
                 cant_restante, precio_promedio, time.strftime('%d/%m/%Y %H:%M:%S', time.gmtime(hora / 1000 - 10800.)),
                 comentario, cuenta, wsClOrdId]
            #print(f"Se actualizó el registro con orderId {clOrdId}.")
        else:
            #print("nueva orden")
            # Append the new order data to df_trade_report
            new_order_data = {
                'orderId': clOrdId,
                'ticker': ticker,
                'Tipo': tipo,
                'Precio': precio,
                'Cant': cantidad,
                'Status': status,
                'Cant Acum': cant_acumulada,
                'Cant Rest': cant_restante,
                'Px Prom': precio_promedio,
                'Fecha': time.strftime('%d/%m/%Y %H:%M:%S', time.gmtime(hora / 1000 - 10800.)),
                'error': comentario,
                'Cta': cuenta,
                'wsClOrdId': wsClOrdId
            }

            #print(new_order_data)
            try:
                df_trade_report = df_trade_report._append(new_order_data, ignore_index=True)
            #print(f"Se agregó un nuevo registro con orderId {clOrdId}.")
            except Exception as e:
                print("no se pudo actualizar")
                print(e)
        #BORRO LAS ORDENS CANCELADAS QUE NO FUERON OPERADO PARCIAL
        df_trade_report = df_trade_report[(df_trade_report['Status'] != 'CANCELLED') | (df_trade_report['Cant Acum'] != 0)]


        # Verifica si alguna fila tiene "buy" en la columna "Tipo"
        for index, row in df_trade_report.iterrows():
            if row["Tipo"] == "BUY" and row["Status"] == "FILLED":
                colgadas= colgadas+1
                if colgadas >16066:
                    telegram.alert_message("Hay ordenes de compra colgadas. verrr" + cuenta )
                    colgadas=0    


def error_handler(message):
    print("Error Message Received: {0}".format(message))


def exception_handler(e):
    print("Exception Occurred: {0}".format(e.msg))





#####
# Conexion Websocket
#####

logger.info('[*] Conectando al websocket')


# 3-Initialize Websocket Connection with the handlers
pyRofex.init_websocket_connection(order_report_handler=order_report_handler,
                                  error_handler=error_handler,
                                  exception_handler=exception_handler)


# 4-Subscribes to receive order report for the default account
pyRofex.order_report_subscription()

#####
# Conexion google sheets
#####

logger.info('[*] Conectando a google sheets')
g_sheet = initialize_google_sheets()

#####
# Conexion telegram
#####
telegram = initialize_telegram(
    bolsar.telk, bolsar.telegram_group_log)

telegramlibro = initialize_telegram(
    bolsar.telk, bolsar.telegram_group_libro)

alertelegram = initialize_telegram(
    bolsar.telk, bolsar.telaid)


#####
# Loop
#####

logger.info('>> Sistema inicializado... recibiendo informacion')
telegram.notification_message('Script iniciado')

if DRY_RUN:
    logger.info('### MODO DE PRUEBAS ###')
else:
    g_sheet.batch_clear(sheets_ranges)

notificado_1, notificado_2 = False, False

while True:
    try:
        date_time = datetime.datetime.now(
            pytz.timezone('America/Argentina/Buenos_Aires'))
        ahora = date_time.time()

        if ahora <= inicio:
            if not notificado_1:
                logger.info('Espera')
                telegram.notification_message('En espera')
                notificado_1 = True


        if ahora > inicio and ahora <= fin:
            if not notificado_2:
                logger.info('Ejecucion')
                telegram.notification_message('Funcionando')
                notificado_2 = True

            # reescribe panel cotizaciones
            try:
                update_range_from_df_google_sheets(g_sheet, df_trade_report)
            except Exception as e:
                telegram.error_message('Error al actualizar google sheets..')

                print(e)

            time.sleep(0.6)

            # reescribe ultima actualizacion
            try:
                update_cell_google_sheets(
                g_sheet, sheets_ranges[1], date_time.strftime(TIME_FORMAT))
            
                print(f"- Ultima actualizacion: {date_time.strftime(TIME_FORMAT)}")
            except Exception as e:
                telegram.error_message('Error al actualizar google sheets..')

                print(e)


            if DRY_RUN:
                print(
                    f"- Ultima actualizacion: {date_time.strftime(TIME_FORMAT)}")
                print(df_trade_report)
            
            time.sleep(WAIT_TIME)

        if ahora > fin:
            
            logger.info('Finalizado')
            logger.info(">> Fuera de horario.")
            disconnect()

        time.sleep(WAIT_TIME)

    except gspread.exceptions.APIError:
        time.sleep(WAIT_TIME * 2)
        g_sheet = initialize_google_sheets()
        telegram.error_message('Error con google sheets. Reiniciando')

    except KeyboardInterrupt:
        disconnect()

    except Exception as e:
        logger.warning(e)
        telegram.alert_message(e)
        disconnect()