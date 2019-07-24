"""業種情報を取得します"""
import re
import urllib.request
import sqlite3
import datetime
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

MKT_CODE = []
SYMBOL_CODE = []
COMPANY_NAME = []
INDUSTRY1 = []
INDUSTRY2 = []
MARKET_CAP = []

def scraping(url, mkt):
    """ Market_code, Symbol, Company_name, industry1, industry2 """
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'lxml')
    for tag_td in soup.find_all('td', class_='table_list_center'):
        # Market_code, Symbol, Company_name
        tag_a = tag_td.find('a')
        if tag_a:
            MKT_CODE.append(mkt)
            SYMBOL_CODE.append(tag_a.text.strip())
            COMPANY_NAME.append(tag_a.get('title'))
        # industry1, industry2
        tag_img = tag_td.find('img')
        if tag_img:
            INDUSTRY1.append(re.sub(r'\[(.+)\]', '', tag_img.get('title')))
            INDUSTRY2.append(re.search(r'\[(.+)\]', tag_img.get('title')).group(1))

    for tag_tr in soup.find_all('tr', id=True):
        temp = tag_tr.find_all('td', class_='table_list_right')[10].text
        temp = temp.replace(',', '')
        temp = temp.replace('-', '0')
        MARKET_CAP.append(float(temp))

# ホーチミン証券取引所
print('HOSE')
scraping('https://www.viet-kabu.com/stock/hcm.html', 'HOSE')
# ハノイ証券取引所
print('HNX')
scraping('https://www.viet-kabu.com/stock/hn.html', 'HNX')

DF = pd.DataFrame({
    'Market_code':MKT_CODE,
    'Symbol':SYMBOL_CODE,
    'Company_name':COMPANY_NAME,
    'industry1':INDUSTRY1,
    'industry2':INDUSTRY2,
    'marketcap':MARKET_CAP,
    'marketcap_percentage':MARKET_CAP / np.sum(MARKET_CAP),
    'pub_date':datetime.datetime.now().strftime("%Y-%m-%d")})

# sqlite3
CON = sqlite3.connect('mysite/db.sqlite3')
CUR = CON.cursor()
SQL = '''delete from vietnam_research_industry
        where strftime("%Y%m", pub_date) = strftime("%Y%m", "now")'''
CUR.execute(SQL)
DF.to_sql('vietnam_research_industry', CON, if_exists='append', index=None)
pd.read_sql_query(sql='select * from vietnam_research_industry', con=CON)

# finish
print('Congrats!')
