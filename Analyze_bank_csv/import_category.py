"""categoryマスタを更新します"""
import sqlite3
from datetime import datetime as dt
import pandas as pd

# sqlite3
CON = sqlite3.connect('mysite/db.sqlite3')

# insert
DF = pd.read_excel('Category.xlsx', sheet_name=['bank', 'credit'])
DF['bank'].to_sql('bankdata_category', CON, if_exists='append', index=None)
DF['credit'].to_sql('bankdata_category', CON, if_exists='append', index=None)

# check
DF = pd.read_sql_query('SELECT description, category1, category2 FROM bankdata_category GROUP BY description;', CON)
DF.to_csv('a.csv', index=False)
