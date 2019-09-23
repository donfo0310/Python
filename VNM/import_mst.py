"""マスタをインポートします"""
import datetime
from sqlalchemy import create_engine
import pandas as pd

# mysql
CON_STR = 'mysql+mysqldb://python:python123@127.0.0.1/pythondb?charset=utf8&use_unicode=1'
CON = create_engine(CON_STR, echo=False).connect()

# reset
CON.execute('DELETE FROM vietnam_research_industryclassification')
CON.execute('DELETE FROM vietnam_research_watchlist')
CON.execute('DELETE FROM vietnam_research_basicinformation')

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

# log
with open('result.log', mode='a') as f:
    f.write('\n' + datetime.datetime.now().strftime("%Y/%m/%d %a %H:%M:%S ") + 'vn_index.py')

# finish
print('Congrats!')
