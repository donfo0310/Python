"""ベトナム統計を取り込みます
https://www.gso.gov.vn/Default_en.aspx?tabid=766
"""
import sqlite3
import datetime
import pandas as pd

# E08.01.csv: 商品およびサービス(小売)のカテゴリー別売上高（単位: 10億ドン）
# 小売(Retail)・宿泊飲食サービス(Inn)・サービスと観光(Tourism)
COLS = []
COLS.append('Year')
COLS.append('Total')
COLS.append('Retail sale')
COLS.append('Accommodation, food and beverage service')
COLS.append('Service and tourism')
STAT = pd.read_csv('import/csv/E08.01.csv', usecols=COLS, sep=';', header=1)
COLS_NEW = ['Year', 'Total_dong_1B', 'Retail_dong_1B', 'Inn_dong_1B', 'Tourism_dong_1B']
STAT = STAT.rename(columns=dict(zip(COLS, COLS_NEW)))
STAT['Year'] = STAT['Year'].str[-4:].astype(int)
STAT['Total_jpy_tril'] = STAT['Total_dong_1B'] / 200 / 1000 # 兆円へ換算
STAT['Retail_per'] = (STAT['Retail_dong_1B'] / STAT['Total_dong_1B']).round(2)
STAT['Retail_jpy_tril'] = STAT['Retail_dong_1B'] / 200 / 1000
STAT['Inn_per'] = (STAT['Inn_dong_1B'] / STAT['Total_dong_1B']).round(2)
STAT['Inn_jpy_tril'] = STAT['Inn_dong_1B'] / 200 / 1000
STAT['Tourism_dong_1B'] = STAT['Tourism_dong_1B'].replace('..', 0)
STAT['Tourism_per'] = (STAT['Tourism_dong_1B'].astype(float) / STAT['Total_dong_1B']).round(2)
STAT['Tourism_jpy_tril'] = STAT['Tourism_dong_1B'].astype(float) / 200 / 1000
COLS_OUT = []
COLS_OUT.append('Year')
COLS_OUT.append('Total_dong_1B')
COLS_OUT.append('Total_jpy_tril')
COLS_OUT.append('Retail_dong_1B')
COLS_OUT.append('Retail_per')
COLS_OUT.append('Retail_jpy_tril')
COLS_OUT.append('Inn_dong_1B')
COLS_OUT.append('Inn_per')
COLS_OUT.append('Inn_jpy_tril')
COLS_OUT.append('Tourism_dong_1B')
COLS_OUT.append('Tourism_per')
COLS_OUT.append('Tourism_jpy_tril')
STAT = STAT[COLS_OUT]
print(STAT)

# E08.06.csv: 商品の輸出入（Mill.USD）
# (*) 輸出 - 輸入
# (**) 2015年以降は航空会社が外国の空港で購入した燃料の価値が含まれる
COLS = []
COLS.append('Year')
COLS.append('Total')
COLS.append('Exports')
COLS.append('Imports (**)')
COLS.append('Balance(*)')
STAT = pd.read_csv('import/csv/E08.06.csv', usecols=COLS, sep=';', header=1)
COLS_NEW = ['Year', 'Total_usd_1M', 'Exports_usd_1M', 'Imports_usd_1M', 'Balance_usd_1M']
STAT = STAT.rename(columns=dict(zip(COLS, COLS_NEW)))
STAT['Year'] = STAT['Year'].str[-4:].astype(int)
STAT['Total_jpy_100M'] = STAT['Total_usd_1M'] / 100
STAT['Exports_jpy_100M'] = STAT['Exports_usd_1M'] / 100
STAT['Imports_jpy_100M'] = STAT['Imports_usd_1M'] / 100
STAT['Balance_jpy_100M'] = STAT['Balance_usd_1M'] / 100
COLS_OUT = []
COLS_OUT.append('Year')
COLS_OUT.append('Total_usd_1M')
COLS_OUT.append('Total_jpy_100M')
COLS_OUT.append('Exports_usd_1M')
COLS_OUT.append('Exports_jpy_100M')
COLS_OUT.append('Imports_usd_1M')
COLS_OUT.append('Imports_jpy_100M')
COLS_OUT.append('Balance_usd_1M')
COLS_OUT.append('Balance_jpy_100M')
STAT = STAT[COLS_OUT]
print(STAT)

# E08.11.csv: 国グループ、国および地域による商品の輸出（Mill. USD）
COLS = []
COLS.append('Country and territory')
COLS.append('Year')
COLS.append('Exports of goods by country group, country and territory')
STAT = pd.read_csv('import/csv/E08.11.csv', usecols=COLS, sep=';', header=1)
COLS_NEW = ['Country', 'Year', 'Exports_usd_1M']
STAT = STAT.rename(columns=dict(zip(COLS, COLS_NEW)))
STAT['Year'] = STAT['Year'].str[-4:].astype(int)
STAT['Exports_usd_1M'] = STAT['Exports_usd_1M'].replace('..', 0).astype(float)
STAT['Exports_jpy_100M'] = STAT['Exports_usd_1M'] / 100
COLS_OUT = []
COLS_OUT.append('Country')
COLS_OUT.append('Year')
COLS_OUT.append('Exports_usd_1M')
COLS_OUT.append('Exports_jpy_100M')
STAT = STAT[COLS_OUT]
print(STAT)

# E08.12.csv: 輸出用の主な商品
COLS = []
COLS.append('Main goods')
COLS.append('Year')
COLS.append('Some main goods for exportation')
STAT = pd.read_csv('import/csv/E08.12.csv', usecols=COLS, sep=';', header=1)
COLS_NEW = ['goods', 'Year', 'amount']
STAT = STAT.rename(columns=dict(zip(COLS, COLS_NEW)))
STAT['Year'] = STAT['Year'].str[-4:].astype(int)
STAT['amount'] = STAT['amount'].replace('..', 0).astype(float)
STAT = STAT[COLS_NEW]
print(STAT)

# # sqlite3
# CON = sqlite3.connect('mysite/db.sqlite3')
# CUR = CON.cursor()
# SQL = '''DELETE FROM vietnam_research_vnindex'''
# CUR.execute(SQL)
# STAT.to_sql('vietnam_research_vnindex', CON, if_exists='append', index=None)

# # log
# with open('result.log', mode='a') as f:
#     f.write('\n' + datetime.datetime.now().strftime("%Y/%m/%d %a %H:%M:%S ") + 'stat.py')

# # finish
# print('Congrats!')
