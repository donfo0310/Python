"""vn-indexを取り込みます（終値を取り込みます。基本的にappendでスタック）
https://jp.investing.com/indices/vn-historical-data
"""
import sqlite3
import datetime
import pandas as pd

VN_INDEX = pd.read_csv('import/VN 過去データ.csv', usecols=['日付け', '終値'])
VN_INDEX['Y'] = VN_INDEX['日付け'].str[-4:].astype(str)
VN_INDEX['M'] = VN_INDEX['日付け'].str.split('月').str[0].astype(int).astype(str).str.zfill(2)
VN_INDEX = VN_INDEX.drop(['日付け'], axis=1)
VN_INDEX['終値'] = VN_INDEX['終値'].str.replace(',', '').astype(float)
VN_INDEX = VN_INDEX.rename(columns={'終値': 'closing_price'})
VN_INDEX['pub_date'] = datetime.datetime.now().strftime("%Y-%m-%d")

# sqlite3
CON = sqlite3.connect('mysite/db.sqlite3')
CUR = CON.cursor()
SQL = '''DELETE FROM vietnam_research_vnindex'''
CUR.execute(SQL)
VN_INDEX.to_sql('vietnam_research_vnindex', CON, if_exists='append', index=None)

# log
with open('result.log', mode='a') as f:
    f.write('\n' + datetime.datetime.now().strftime("%Y/%m/%d %a %H:%M:%S ") + 'vn_index.py')

# finish
print('Congrats!')
