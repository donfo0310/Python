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
DF = pd.read_excel('import/xlsx/Category.xlsx', sheet_name=['bank', 'credit'])
DF['bank'].to_sql('bankdata_category', CON, if_exists='append', index=None)
DF['credit'].to_sql('bankdata_category', CON, if_exists='append', index=None)

# check
SQL = 'SELECT description, category1, category2 FROM bankdata_category GROUP BY description;'
DF = pd.read_sql_query(SQL, CON)
