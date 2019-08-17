"""マスタをインポートします"""
import sqlite3
import pandas as pd

# sqlite3
CON = sqlite3.connect('mysite/db.sqlite3')

# reset
CUR = CON.cursor()
SQL = '''DELETE FROM vietnam_research_industryclassification'''
CUR.execute(SQL)
SQL = '''DELETE FROM vietnam_research_watchlist'''
CUR.execute(SQL)
SQL = '''DELETE FROM vietnam_research_basicinformation'''
CUR.execute(SQL)

# insert
SH = ['IndClass', 'WatchList', 'BasicInfo']
TABLE = []
TABLE.append('vietnam_research_industryclassification')
TABLE.append('vietnam_research_watchlist')
TABLE.append('vietnam_research_basicinformation')
DF = pd.read_excel('import/xlsx/mst.xlsx', sheet_name=SH)
DF[SH[0]].to_sql(TABLE[0], CON, if_exists='append', index=None)
DF[SH[1]].to_sql(TABLE[1], CON, if_exists='append', index=None)
DF[SH[2]].to_sql(TABLE[2], CON, if_exists='append', index=None)
