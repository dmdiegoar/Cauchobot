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

username = bolsar.ul4b  # usuario xoms
password = bolsar.pb4  # password xoms
account = bolsar.ued  # nro de cuenta xoms
api_url = bolsar.api_url  # endpoint rest xoms
ws_url = bolsar.ws_url  # endpoint ws xoms

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


""" def refresh_data(symbol, bid_size, bid, ask, ask_size, last, close, open, high, low, volume, nom_volume, last_update):
    _summary_

    Args:
        symbol (_type_): _description_
        bid_size (_type_): _description_
        bid (_type_): _description_
        ask (_type_): _description_
        ask_size (_type_): _description_
        last (_type_): _description_
        close (_type_): _description_
        open (_type_): _description_
        high (_type_): _description_
        low (_type_): _description_
        volume (_type_): _description_
        nom_volume (_type_): _description_
        last_update (_type_): _description_
    
    global df_new_quote

    if last != 0 and close != 0:
        change = last / close - 1
    else:
        change = 0.0

    df_new_quote = pd.DataFrame([{'ticker': symbol,
                                  'bidsize': bid_size,
                                  'bid': bid,
                                  'last': last,
                                  'ask': ask,
                                  'asksize': ask_size,
                                  'open': open,
                                  'high': high,
                                  'low': low,
                                  'close': close,
                                  'chg%': change,
                                  'volume': volume,
                                  'nomvolume': nom_volume,
                                  'lastupdate': time.strftime('%d/%m/%Y %H:%M:%S',
                                                              time.gmtime(last_update / 1000 - 10800.))}])
    df_new_quote = df_new_quote.set_index('ticker')

    df_quoteboard.update(df_new_quote) """


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


# def initialize_telegram(bot_id, chat_id):
#     """_summary_

#     Args:
#         bot_id (_type_): _description_
#         chat_id (_type_): _description_

#     Returns:
#         _type_: _description_
#     """
#     return Telegram(bot_id=bot_id, chat_id=chat_id)


def disconnect():
    pyRofex.close_websocket_connection()
    logger.info(f"- Finalizado: {date_time.strftime(TIME_FORMAT)}")
    telegram.notification_message('Script cerrado')
    exit(0)
#####
# Websockets handlers
#####


def market_data_handler(message):
    """ Manipulador de mensajes de Market Data.
    Extrae los valores y llama al programa para actualizar cotizaciones

    Args:
        message (dict): mensaje websocket
    """
    print("markrt data rscibido")
    symbol = message['instrumentId']['symbol']
    last = 0 if not message['marketData']['LA'] else message['marketData']['LA']['price']
    lastUpdate = 0 if not message['marketData']['LA'] else message['marketData']['LA']['date']
    bid = 0 if not message['marketData']['BI'] else message['marketData']['BI'][0]['price']
    bidSize = 0 if not message['marketData']['BI'] else message['marketData']['BI'][0]['size']
    ask = 0 if not message['marketData']['OF'] else message['marketData']['OF'][0]['price']
    askSize = 0 if not message['marketData']['OF'] else message['marketData']['OF'][0]['size']
    close = 0 if not message['marketData']['CL'] else message['marketData']['CL']['price']
    open = 0 if not message['marketData']['OP'] else message['marketData']['OP']
    high = 0 if not message['marketData']['HI'] else message['marketData']['HI']
    low = 0 if not message['marketData']['LO'] else message['marketData']['LO']
    volume = 0 if not message['marketData']['EV'] else message['marketData']['EV']
    nomVolume = 0 if not message['marketData']['NV'] else message['marketData']['NV']

    """ refresh_data(symbol, bidSize, bid, ask, askSize, last, close,
                 open, high, low, volume, nomVolume, lastUpdate) """


def order_report_handler(message):
    print("orden recibida")
    print(message)
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

    if status in ("FILLED", "PARTIALLY_FILLED"):
        telegram.notification_message( ticker +" \n"+ 
          tipo +
          "\n Precio: "+ str(max(precio, precio_promedio))
          +"\n Cantidad: "+ str(cantidad)
          +"\n resta: "+ str(cant_restante)
          +"\n "+ status
          +"\n "+ comentario      )
    
    elif status=="REJECTED":
        telegram.alert_message( ticker +" \n"+ 
          tipo +
          "\n Precio: "+ str(max(precio, precio_promedio))
          +"\n Cantidad: "+ str(cantidad)
          +"\n resta: "+ str(cant_restante)
          +"\n "+ status
          +"\n "+ comentario      )

    # Check if orderId already exists in the DataFrame
    if clOrdId in df_trade_report['orderId'].values:
        # Update the existing row with the matching orderId
        df_trade_report.loc[df_trade_report['orderId'] == clOrdId] = [clOrdId, ticker, tipo, precio, cantidad, status, cant_acumulada,
                 cant_restante, precio_promedio, time.strftime('%d/%m/%Y %H:%M:%S', time.gmtime(hora / 1000 - 10800.)),
                 comentario, cuenta, wsClOrdId]
        print(f"Se actualizó el registro con orderId {clOrdId}.")
    else:
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
        df_trade_report = df_trade_report.append(new_order_data, ignore_index=True)
        print(f"Se agregó un nuevo registro con orderId {clOrdId}.")
        
        #BORRO LAS ORDENS CANCELADAS QUE NO FUERON OPERADO PARCIAL
        df_trade_report = df_trade_report[(df_trade_report['Status'] != 'CANCELLED') | (df_trade_report['Cant Acum'] != 0)]


def error_handler(message):
    """Manipulador de mensajes de error del websocket
    - no implementado -

    Args:
        message (dict): mensaje websocket
    """
    logger.info('[>] Error en pyRofex: ' + message)


def exception_handler(message):
    """Manipulador de mensajes por excepciones
    - no implementado -

    Args:
        message (dict): mensaje websocket
    """
    logger.info('[>] Excepcion en pyRofex: ' + message)


#####
# Conexion xOMS
#####

logger.info('[*] Inicializando pyRofex')
pyRofex._set_environment_parameter("url", api_url, pyRofex.Environment.LIVE)
pyRofex._set_environment_parameter("ws", ws_url, pyRofex.Environment.LIVE)

pyRofex.initialize(user=username, password=password,
                   account=account, environment=pyRofex.Environment.LIVE)
try:
    print("intentando conectar")
    pyRofex.init_websocket_connection(market_data_handler=market_data_handler,
                                  error_handler=error_handler,
                                  exception_handler=exception_handler,
                                  order_report_handler=order_report_handler)
    print("websok conectado")
except:
    print("no coneca websoke")
#####
# Instrumentos
#####
""" 
logger.info('[*] Obteniendo instrumentos')
if os.path.isfile(all_instruments_pickle):
    all_instruments = read_pickle(all_instruments_pickle)
else:
    all_instruments = pyRofex.get_all_instruments()
    write_pickle(all_instruments_pickle, all_instruments)

if os.path.isfile(detailed_instruments_pickle):
    detailed_instruments = read_pickle(detailed_instruments_pickle)
else:
    detailed_instruments = pyRofex.get_detailed_instruments()
    write_pickle(detailed_instruments_pickle, detailed_instruments)


acciones, cauciones, opciones = [], [], []
_settlement_map = [('48hs', ''), ('CI', ' - CI'), ('24hs', ' - 24')]
_byma_preffix = "MERV - XMEV"

logger.info('[*] Armando listado de instrumentos')
for ticker in my_tickers:
    ## acciones 
    for settlement in _settlement_map:
        acciones.append(
            {'symbol': f"{_byma_preffix} - {ticker['stock']} - {settlement[0]}",
             'ticker': f"{ticker['stock'] + settlement[1]}",
             'maturityDate': ''}
        )
        
    for instrument in all_instruments['instruments']:
        ## caucion a 1 dia habil
        if 'PESOS' in instrument['instrumentId']['symbol'] and 'RPXXXX' in instrument['cficode']:
            _symbol = instrument['instrumentId']['symbol']
            _ticker = instrument['instrumentId']['symbol'].replace('MERV - XMEV - ', '')
            _expiration = instrument['instrumentId']['symbol'].split(' - ')[3][:-1]
            cauciones.append({'symbol': _symbol, 'ticker': _ticker, 'maturityDate': '', 'expiration': _expiration})
        
        ## opciones
        if ticker['options'] in instrument['instrumentId']['symbol'] and ('OCASPS' in instrument['cficode'] or 'OPASPS' in instrument['cficode']):
            _symbol = instrument['instrumentId']['symbol']
            _ticker = _symbol.split(' - ')[2]
            opciones.append(
                {'symbol': _symbol, 'ticker': _ticker})


## Busca caucion al plazo mas corto disponible.
short_repo = cauciones[0]
for caucion in cauciones:
    if caucion['expiration'] < short_repo['expiration']:
        short_repo = caucion
short_repo.pop('expiration')

acciones.append(short_repo)

#####
# Dataframe instrumentos
#####

today = pd.to_datetime(datetime.datetime.today().date())
df_acciones = pd.DataFrame.from_dict(acciones)
df_opciones = pd.DataFrame.from_dict(opciones)

# arma dataframe de instrumentos detallados
df_detailed_instruments = pd.DataFrame.from_dict(
    detailed_instruments['instruments'])

# genera fecha de expiracion y dias a esa fecha en un nuevo dataframe
df_maturity = df_detailed_instruments[[
    'maturityDate', 'securityDescription']].set_index('securityDescription')
df_maturity['maturityDate'] = pd.to_datetime(
    df_maturity['maturityDate'], format='%Y%m%d').fillna(today)
df_maturity['daysToMaturity'] = (df_maturity['maturityDate'] - today).dt.days

# mergea lista de opciones con sus fechas de expiracion
df_opciones = pd.merge(df_opciones, df_maturity, left_on='symbol',
                       right_on='securityDescription', how='left')

# filtra instrumentos vencidos
df_opciones = df_opciones[df_opciones['daysToMaturity'] >= 0]

# ordena tickers
df_opciones.sort_values(by=['maturityDate', 'ticker'], inplace=True)

# merge para unica lista suscripcion
df_suscripcion = pd.concat([df_acciones, df_opciones], axis=0)

#####
# Dataframes market data
#####

logger.info('[*] Generando paneles')
_quoteboard_columns = ['symbol', 'ticker', 'bidsize', 'bid', 'last', 'ask', 'asksize',
                       'open', 'high', 'low', 'close', 'chg%', 'volume', 'nomvolume', 'lastupdate']

df_new_quote = pd.DataFrame(columns=_quoteboard_columns)

df_quoteboard = pd.DataFrame({'symbol': df_suscripcion['symbol'].to_list(
), 'ticker': df_suscripcion['ticker'].to_list()}, columns=_quoteboard_columns)
df_quoteboard = df_quoteboard.set_index('symbol')

 """


# Create an empty DataFrame to hold the trade report data
_trade_report_columns = ['orderId', 'ticker', 'Tipo', 'Precio', 'Cant', 'Status', 'Cant Acum', 'Cant Rest', 'Px Prom',
                         'Fecha', 'error', 'Cta', 'wsClOrdId']
df_trade_report = pd.DataFrame(columns=_trade_report_columns)


#####
# Conexion Websocket
#####


# sin uso
logger.info('[*] Conectando al websocket')
entries = [pyRofex.MarketDataEntry.BIDS,
           pyRofex.MarketDataEntry.OFFERS,
           pyRofex.MarketDataEntry.LAST,
           pyRofex.MarketDataEntry.OPENING_PRICE,
           pyRofex.MarketDataEntry.CLOSING_PRICE,
           pyRofex.MarketDataEntry.HIGH_PRICE,
           pyRofex.MarketDataEntry.LOW_PRICE,
           pyRofex.MarketDataEntry.TRADE_VOLUME,
           pyRofex.MarketDataEntry.NOMINAL_VOLUME,
           pyRofex.MarketDataEntry.TRADE_EFFECTIVE_VOLUME] 

pyRofex.market_data_subscription(
    tickers=['MERV - XMEV - GGAL - CI'], entries=entries, depth=1)

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
            update_range_from_df_google_sheets(g_sheet, df_trade_report)

            # reescribe ultima actualizacion
            update_cell_google_sheets(
                g_sheet, sheets_ranges[1], date_time.strftime(TIME_FORMAT))

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
