import os
import json
from http.client import responses

import requests
import pandas as pd
import os


trader_subdomain = os.environ["FOOD_SUBDOMAIN"]
trader_usr = os.environ["FOOD_USERNAME"]
trader_pw = os.environ["FOOD_PASSWORD"]


bar_subdomain = os.environ["BAR_SUBDOMAIN"]
bar_usr = os.environ["BAR_USERNAME"]
bar_pw = os.environ["BAR_PASSWORD"]


dl_subdomain = os.environ["DREAMLAND_SUBDOMAIN"]
dl_usr = os.environ["DREAMLAND_USERNAME"]
dl_pw = os.environ["DREAMLAND_PASSWORD"]


def generate_token(subdomain,usr,pw):
    response = requests.post(
        'https://api.thegoodtill.com/api/login',
        data = {
            'subdomain': subdomain,
            'username': usr,
            'password': pw
        }
    )
    response.raise_for_status()
    data = response.json()

    token = data["token"]

    if not token:
        raise RuntimeError(f'Failed to login to Goodtill API, response: {data}')
    return token


def get_registers(token,outlet):

    url = "https://api.thegoodtill.com/api/registers"

    headers = {'Authorization':f'Bearer {token}',
               'Outlet-Id':outlet}

    response = requests.get(url,
                            headers=headers
    )

    return response.json()['data']


def get_outlets(token):
    url = "https://api.thegoodtill.com/api/outlets"

    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(url, headers=headers)

    return response.json()['data']

if __name__ == '__main__':

    trader_registers = []
    bar_registers = []
    dl_registers = []

    trader_token = generate_token(trader_subdomain,trader_usr,trader_pw)
    bar_token = generate_token(bar_subdomain,bar_usr,bar_pw)
    dl_token = generate_token(dl_subdomain,dl_usr,dl_pw)

    trader_outlets = get_outlets(trader_token)
    trader_outlets_df = pd.DataFrame(trader_outlets)
    trader_outlets_df['Area'] = "Trader"

    trader_outlet_ids = [item['id'] for item in trader_outlets]

    bar_outlets = get_outlets(bar_token)
    bar_outlets_df = pd.DataFrame(bar_outlets)
    bar_outlets_df['Area'] = "Bar"

    bar_outlet_ids = [item['id'] for item in bar_outlets]

    dl_outlets = get_outlets(dl_token)
    dl_outlets_df = pd.DataFrame(dl_outlets)
    dl_outlets_df['Area'] = "Dreamland"

    dl_outlet_ids = [item['id'] for item in dl_outlets]

    for id in trader_outlet_ids:
        trader_registers.extend(get_registers(trader_token, id))

    for id in bar_outlet_ids:
        bar_registers.extend(get_registers(bar_token, id))

    for id in dl_outlet_ids:
        dl_registers.extend(get_registers(dl_token, id))

    trader_registers_df = pd.DataFrame(trader_registers)
    trader_registers_df['Area'] = "Trader"

    bar_registers_df = pd.DataFrame(bar_registers)
    bar_registers_df['Area'] = "Bar"

    dl_registers_df = pd.DataFrame(dl_registers)
    dl_registers_df['Area'] = "Dreamland"

    reg_drop_cols = ["quick_keys_id","table_quick_keys_id","receipt_template_id","printer_id,reg_order_from","reg_order_to","reg_display_no","cash_float","print_settings"]

    outlets = pd.concat([trader_outlets_df,bar_outlets_df,dl_outlets_df],ignore_index=True)
    registers = pd.concat([trader_registers_df,bar_registers_df,dl_registers_df],ignore_index=True)
    registers.drop(reg_drop_cols,axis=1,inplace=True)

    filename = 'outlets.csv'
    outlets.to_csv(filename,index=False)

    filename = 'registers.csv'
    registers.to_csv(filename,index=False)














