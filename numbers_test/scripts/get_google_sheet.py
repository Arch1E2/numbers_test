from __future__ import print_function

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

import requests
import xml.etree.ElementTree as ET
import datetime
import psycopg2
import threading
import os


DB_NAME = os.environ.get('POSTGRES_NAME')
DB_USER = os.environ.get('POSTGRES_USER')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DB_HOST = 'postgres'
DB_PORT = '5432'

TG_BOT_TOKEN = os.environ.get('TG_BOT_TOKEN')
TG_BOT_CHAT_ID = os.environ.get('TG_BOT_CHAT_ID')

last_currency_check_date = None
last_currencies = None

polling_interval = 1

def send_message(orders):
    text = "Истек срок поставки по заказам:\n"
    for order in orders:
        text += f'- {order[1]}\n'
    try:
        r = requests.post(f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage', data={'chat_id': TG_BOT_CHAT_ID, 'text': text})

        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("UPDATE app_botmessage SET message_send_date = %s WHERE order_id_id IN %s", (datetime.datetime.now(), orders))
    except:
        print("Error sending message")


def get_bot_message_from_base(order):
    # connect to db
    conn = None
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    except:
        return "Error connecting to DB"

    # get order from db
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM app_botmessage WHERE order_id_id = %s", (order[1],))
        order = cur.fetchone()
    except:
        print("Error getting message from DB")
        return False
    # close connection
    conn.close()

    # return order
    return order
    


def get_currency_rates(currency_ISO="USD"):
    # date today format DD/MM/YYYY
    today = datetime.date.today()
    today_str = today.strftime("%d/%m/%Y")
    #get xml from CB api
    try:
        cb_url = requests.get(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={today_str}')
    except:
        return "Error getting currency rates"

    #parse xml
    root = ET.fromstring(cb_url.text)

    currencies = {}

    for child in root:
        if child.tag == 'Valute':
            currencies[child.find('CharCode').text] = (child.find('Value').text, child.find('Nominal').text)

    #return tuple with currency rate and currency nominal
    return currencies[currency_ISO]


def get_google_sheet():
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '17dPebsgAEgaAHIGKbORvbbI_y1o1A1i8ZJxj6_jAzrM'
    SAMPLE_RANGE_NAME = 'Лист1'

    # create credentials for google sheets
    SERVICE_ACCOUNT_FILE = 'keys.json'
    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Build the service object.
    creds = None
    try:
        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            return "Table is empty"

        return values
    except HttpError as err:
        return 'API returned error'
        

def check_order_in_base(order_id):
    # connect to db
    conn = None
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    except:
        return "Error connecting to DB"

    # get order from db
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM app_order WHERE order_id = %s", (order_id,))
        order = cur.fetchone()
    except:
        print("Error getting order from DB")
        return False
    # close connection
    conn.close()

    # return order
    return order

def add_order_to_base(index_in_table, order_id, incoming_date, total_cost_in_dollars, total_cost_in_rubles, total_cost_in_rubles_after_comma):
    # connect to db
    conn = None
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    except:
        return "Error connecting to DB"

    # add order to db
    cur = conn.cursor()
    cur.execute("""INSERT INTO app_order (index_in_table, order_id, incoming_date, total_cost_in_dollars, total_cost_in_rubles, total_cost_in_rubles_after_comma)
                VALUES (%s, %s, %s, %s, %s, %s);""",
                (index_in_table, order_id, incoming_date, total_cost_in_dollars, total_cost_in_rubles, total_cost_in_rubles_after_comma))
    
    #add bot message to db
    cur.execute("""INSERT INTO app_botmessage (order_id_id, message_send_date)
                VALUES (%s, %s);""",
                (order_id, None))
    #conn commit
    conn.commit()
    # cursor close
    cur.close()
    # close connection
    conn.close()  

def update_order_in_base(index_in_table, order_id, incoming_date, total_cost_in_dollars, total_cost_in_rubles, total_cost_in_rubles_after_comma):
    # connect to db
    conn = None
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    except:
        return "Error connecting to DB"

    # update order in db
    cur = conn.cursor()
    cur.execute("""UPDATE app_order SET incoming_date = %s,
                total_cost_in_dollars = %s, total_cost_in_rubles = %s, total_cost_in_rubles_after_comma = %s, index_in_table = %s WHERE order_id = %s;""",
                (incoming_date, total_cost_in_dollars, total_cost_in_rubles, total_cost_in_rubles_after_comma, index_in_table, order_id))

    #connection commit
    conn.commit()
    # cursor close
    cur.close()
    # close connection
    conn.close()

def check_order_data(order, row):
    if (order[-2] != int(row[0]) or
        datetime.datetime.strptime(row[3], '%d.%m.%Y').date() != order[2] or
        order[3] != int(row[2]) or
        order[4] != int(row[-2]) or
        order[-1] != int(row[-1])):
        return False
    else: 
        return True


def delete_rows(order_ids):
    # connect to db
    conn = None
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    except:
        return "Error connecting to DB"

    sql_ids_string = ", ".join(order_ids)
    # delete rows from db
    cur = conn.cursor()
    cur.execute("""DELETE FROM app_order WHERE order_id NOT IN %s;""", (tuple(order_ids),))
    cur.execute("""DELETE FROM app_botmessage WHERE order_id_id NOT IN %s;""", (tuple(order_ids),))
    #connection commit
    conn.commit()
    # cursor close
    cur.close()
    # close connection
    conn.close()


#set interval for checking google sheet
e = threading.Event()
while not e.wait(polling_interval):
    #get currency rates from CB if dont have
    if last_currency_check_date != datetime.date.today():
        dollar_rate = get_currency_rates()
        last_currency_check_date = datetime.date.today()
        last_currencies = dollar_rate
    else:
        dollar_rate = last_currencies

    #get google sheet
    sheet_values = get_google_sheet()

    new_orders_count = 0
    updated_orders_count = 0

    expired_orders = []
    sheet_order_ids = []

    #check sheet for new orders
    for row in sheet_values[1: len(sheet_values)]:
        sheet_order_ids.append(row[1])
        #create total cost in rubles rate * total cost in dollars / nominal
        float_first_part = int(dollar_rate[0].split(',')[0])
        float_second_part = int(dollar_rate[0].split(',')[1])
        valute_nominal = int(dollar_rate[1])
        total_cost_in_valute = int(row[2])
        total_cost_in_rubles = (float_first_part * total_cost_in_valute / valute_nominal)
        total_cost_in_rubles_after_comma = (float_second_part * total_cost_in_valute / valute_nominal)
                               
        row.append(total_cost_in_rubles)
        row.append(total_cost_in_rubles_after_comma)

        #create date from string
        incoming_date = datetime.datetime.strptime(row[3], '%d.%m.%Y').date()
        today = datetime.date.today()

        #check if order is expired and add to list
        if incoming_date < today:
            expired_orders.append(row[1])

        order = check_order_in_base(row[1])
        if order:
            if check_order_data(order, row):
                pass
            else:
                update_order_in_base(row[0], row[1], incoming_date, row[2], row[4], row[5])
                updated_orders_count += 1
        else:
            add_order_to_base(int(row[0]), int(row[1]), incoming_date, int(row[2]), row[4], row[5])
            new_orders_count += 1

    #delete killled orders from db
    print(sheet_order_ids)
    delete_rows(sheet_order_ids)
    
    orders_for_message = []

    #check if message not sent yet
    for order in expired_orders:
        if get_bot_message_from_base(order) and get_bot_message_from_base(order)[1] != None:
            pass
        else:
            orders_for_message.append(int(order[1]))

    print("New orders: " + str(new_orders_count))
    print("Updated orders: " + str(updated_orders_count))





    

