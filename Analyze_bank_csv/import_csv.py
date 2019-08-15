"""csvを取り込みます"""
import os
import sqlite3
import datetime
import pandas as pd

# sqlite3
CON = sqlite3.connect('mysite/db.sqlite3')

FILES = os.listdir('csv')
for file in FILES:

    print(file)

    # MUFG
    if file[:4] == 'MUFG':
        COLS = ['日付', '摘要', '摘要内容', '支払い金額', '預かり金額']
        COLS_NEW = ['ymd', 'description', 'description_detail', 'amount_out', 'amount_in']
        COLS_DEL = ['description_detail', 'amount_out', 'amount_in']
        COLS_OUT = ['ymd', 'bank_name', 'description', 'amount']
        CSV = pd.read_csv('csv/' + file, usecols=COLS, encoding="shift-jis")
        CSV = CSV.rename(columns=dict(zip(COLS, COLS_NEW)))
        CSV['bank_name'] = 'MUFG'
        CSV['description'] = CSV['description'] + ' ' + CSV['description_detail'].fillna('')
        CSV['description'] = CSV['description'].str.strip().str.replace('　', '')
        CSV['amount_out'] = CSV['amount_out'].fillna(0)
        CSV['amount_out'] = CSV['amount_out'].astype(str).str.replace(',', '').astype(int) * -1
        CSV['amount_in'] = CSV['amount_in'].fillna(0)
        CSV['amount_in'] = CSV['amount_in'].astype(str).str.replace(',', '').astype(int)
        CSV['amount'] = CSV['amount_out'] + CSV['amount_in']
        CSV = CSV.drop(COLS_DEL, axis=1)
        CSV = CSV[COLS_OUT]
        CSV.to_sql('bankdata_dailydata', CON, if_exists='append', index=None)

    # NAGAGIN
    if file[:4] == 'NAGA':
        COLS = ['取扱日付', '摘要', 'お支払金額', 'お預り金額']
        COLS_NEW = ['ymd', 'description', 'amount_out', 'amount_in']
        COLS_DEL = ['amount_out', 'amount_in']
        COLS_OUT = ['ymd', 'bank_name', 'description', 'amount']
        Y = file[-10:-6]   # YYYY
        M = str(int(file[-6:-4])) # MM
        CSV = pd.read_csv('csv/' + file, usecols=COLS, encoding="shift-jis")
        CSV = CSV.rename(columns=dict(zip(COLS, COLS_NEW)))
        CSV['ymd'] = [row['ymd'].split('月')[1].replace('日', '') for idx, row in CSV.iterrows()]
        CSV['ymd'] = [Y + '/' + M + '/' + row['ymd'] for idx, row in CSV.iterrows()]
        CSV['bank_name'] = 'NAGAGIN'
        CSV['amount_out'] = CSV['amount_out'].fillna(0).astype(str).str.replace(',', '')
        CSV['amount_out'] = CSV['amount_out'].str.replace('\\', '').astype(int) * -1
        CSV['amount_in'] = CSV['amount_in'].fillna(0).astype(str).str.replace(',', '')
        CSV['amount_in'] = CSV['amount_in'].str.replace('\\', '').astype(float).round(0).astype(int)
        CSV['amount'] = CSV['amount_out'] + CSV['amount_in']
        CSV = CSV.drop(COLS_DEL, axis=1)
        CSV = CSV[COLS_OUT]
        CSV.to_sql('bankdata_dailydata', CON, if_exists='append', index=None)

# log
with open('result.log', mode='a') as f:
    f.write('\n' + datetime.datetime.now().strftime("%Y/%m/%d %a %H:%M:%S ") + 'import_bank_csv.py')

# finish
print('Congrats!')
