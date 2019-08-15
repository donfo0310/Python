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
CLOSING_PRICE = []
VOLUME = []
PER = []
DATE = []

def scraping(url, mkt):
    """ Market_code, Symbol, Company_name, industry1, industry2 """

    # soup
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'lxml')

    # date
    ymdhms = soup.find('th', class_='table_list_left').text.strip().split('（')[1][:16] + ':00'
    ymdhms = ymdhms.replace('/', '-')

    # data1
    for tag_td in soup.find_all('td', class_='table_list_center'):
        # Market_code, Symbol, Company_name
        tag_a = tag_td.find('a')
        if tag_a:
            MKT_CODE.append(mkt)
            SYMBOL_CODE.append(tag_a.text.strip())
            COMPANY_NAME.append(tag_a.get('title'))
            DATE.append(ymdhms)
        # industry1, industry2
        tag_img = tag_td.find('img')
        if tag_img:
            INDUSTRY1.append(re.sub(r'\[(.+)\]', '', tag_img.get('title')))
            INDUSTRY2.append(re.search(r'\[(.+)\]', tag_img.get('title')).group(1))

    # data2
    for tag_tr in soup.find_all('tr', id=True):
        # closing_price	終値
        temp = tag_tr.find_all('td', class_='table_list_right')[1].text
        CLOSING_PRICE.append(float(temp))
        # Volume 出来高
        temp = tag_tr.find_all('td', class_='table_list_right')[7].text
        temp = temp.replace(',', '')
        temp = temp.replace('-', '0')
        VOLUME.append(float(temp))
        # MARKET_CAP 時価総額（億円）
        temp = tag_tr.find_all('td', class_='table_list_right')[10].text
        temp = temp.replace(',', '')
        temp = temp.replace('-', '0')
        MARKET_CAP.append(float(temp))
        # PER 15倍以下が割安
        temp = tag_tr.find_all('td', class_='table_list_right')[11].text
        temp = temp.replace('-', '0')
        PER.append(float(temp))

# ホーチミン証券取引所
print('HOSE')
scraping('https://www.viet-kabu.com/stock/hcm.html', 'HOSE')
# ハノイ証券取引所
print('HNX')
scraping('https://www.viet-kabu.com/stock/hn.html', 'HNX')

# sqlite3
CON = sqlite3.connect('mysite/db.sqlite3')
CUR = CON.cursor()

# data1 summary data
DF = pd.DataFrame({
    'Market_code': MKT_CODE,
    'Symbol': SYMBOL_CODE,
    'Company_name': COMPANY_NAME,
    'industry1': INDUSTRY1,
    'industry2': INDUSTRY2,
    'count_per': 1/len(INDUSTRY1),
    'marketcap': MARKET_CAP,
    'marketcap_per': MARKET_CAP/np.sum(MARKET_CAP),
    'pub_date': DATE
})
SQL = '''DELETE FROM vietnam_research_industry
        WHERE date(datetime(pub_date)) = strftime("%Y%m", "now")'''
CUR.execute(SQL)
DF.to_sql('vietnam_research_industry', CON, if_exists='append', index=None)

# data2 transaction data
DF = pd.DataFrame({
    'Market_code': MKT_CODE,
    'Symbol': SYMBOL_CODE,
    'closing_price': CLOSING_PRICE,
    'volume': VOLUME,
    'marketcap': MARKET_CAP,
    'per': PER,
    'pub_date': DATE
})
SQL = '''DELETE FROM vietnam_research_dailydata
        WHERE strftime("%Y%m%d", pub_date) = strftime("%Y%m%d", "now")'''
CUR.execute(SQL)
DF.to_sql('vietnam_research_dailydata', CON, if_exists='append', index=None)

# log
with open('result.log', mode='a') as f:
    f.write('\n' + datetime.datetime.now().strftime("%Y/%m/%d %a %H:%M:%S ") + 'industry.py')

# finish
print('Congrats!')
