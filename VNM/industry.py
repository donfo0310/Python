"""業種情報を取得します"""
import re
import urllib.request
import sqlite3
import datetime
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

def scraping(url, mkt):
    """ Market_code, Symbol, company_name, industry1, industry2 """

    symbol_code = []
    company_name = []
    industry1 = []
    industry2 = []
    market_cap = []
    closing_price = []
    volume = []
    per = []
    date = []

    # soup
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'lxml')

    # date
    # e.g. 'ホーチミン証取株価（2019/08/16 15:00VNT）' => '2019-08-16 15:00:00'
    ymdhms = soup.find('th', class_='table_list_left').text.strip()
    ymdhms = ymdhms.split('（')[1][:16].replace('/', '-') + ':00'

    # data
    for tag_tr in soup.find_all('tr', id=True):
        # Symbol, company_name, date
        temp = tag_tr.find_all('td', class_='table_list_center')[0]
        symbol_code.append(temp.text.strip())       # AAA
        company_name.append(temp.a.get('title'))    # アンファット・バイオプラスチック
        date.append(ymdhms)                         # 2019-08-16 15:00:00
        # industry1, industry2
        temp = tag_tr.find_all('td', class_='table_list_center')[1]
        industry1.append(re.sub(r'\[(.+)\]', '', temp.img.get('title')))
        industry2.append(re.search(r'\[(.+)\]', temp.img.get('title')).group(1))
        # closing_price	終値
        temp = tag_tr.find_all('td', class_='table_list_right')[1].text
        closing_price.append(float(temp))
        # volume 出来高
        temp = tag_tr.find_all('td', class_='table_list_right')[7].text
        temp = temp.replace('-', '0').replace(',', '')
        volume.append(float(temp))
        # market_cap 時価総額（億円）
        temp = tag_tr.find_all('td', class_='table_list_right')[10].text
        temp = temp.replace('-', '0').replace(',', '')
        market_cap.append(float(temp))
        # per 15倍以下が割安
        temp = tag_tr.find_all('td', class_='table_list_right')[11].text
        temp = temp.replace('-', '0')
        per.append(float(temp))

    # sqlite3
    con = sqlite3.connect('mysite/db.sqlite3')
    cur = con.cursor()

    # data1 summary data（毎月末のデータが蓄積する）
    df_summary = pd.DataFrame({
        'market_code': mkt,
        'symbol': symbol_code,
        'company_name': company_name,
        'industry1': industry1,
        'industry2': industry2,
        'count_per': 1/len(industry1),
        'closing_price': closing_price,
        'volume': volume,
        'marketcap': market_cap,
        'marketcap_per': market_cap/np.sum(market_cap),
        'per': per,
        'pub_date': date
    })
    sql = '''
            DELETE FROM vietnam_research_industry
            WHERE market_code = {quote}{market_code}{quote} AND
            SUBSTR(pub_date, 1, 7) = {quote}{ym}{quote}'''
    sql = sql.format(market_code=mkt, quote='\'', ym=ymdhms[:7])
    cur.execute(sql)
    df_summary.to_sql('vietnam_research_industry', con, if_exists='append', index=None)

# ホーチミン証券取引所
print('HOSE')
scraping('https://www.viet-kabu.com/stock/hcm.html', 'HOSE')
# ハノイ証券取引所
print('HNX')
scraping('https://www.viet-kabu.com/stock/hn.html', 'HNX')

# log
with open('result.log', mode='a') as f:
    f.write('\n' + datetime.datetime.now().strftime("%Y/%m/%d %a %H:%M:%S ") + 'industry.py')

# finish
print('congrats!')
