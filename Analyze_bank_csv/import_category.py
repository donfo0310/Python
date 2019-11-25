"""categoryマスタを更新します"""
import sqlite3
from datetime import datetime as dt
import pandas as pd

# sqlite3
CON = sqlite3.connect('mysite/db.sqlite3')

# reset（本当は取り込み時の重複だけ排除したいが複合キーがないと...）
CUR = CON.cursor()
SQL = '''DELETE FROM bankdata_category'''
CUR.execute(SQL)

# insert
COLS_OUT = ['description', 'category1', 'category2', 'bikou']
DF = pd.read_excel('import/xlsx/Category.xlsx', usecols=COLS_OUT, sheet_name='bankcredit')
DF = DF[COLS_OUT]
DF.to_sql('bankdata_category', CON, if_exists='append', index=None)

# finish
print('Congrats!')
