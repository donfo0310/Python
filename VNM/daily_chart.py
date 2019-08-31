"""
指定銘柄のチャートをpngで取得します
top5も取得します
step1: 1企業あたり毎月1行しかないものを group集計 する(per >1)
step2: top 5 by group
"""
import time
import urllib.request
import datetime
import sqlite3
from bs4 import BeautifulSoup
import pandas as pd

def scraping(mkt, symbol):
    """ symbol をリストで受け入れてガリマワシもいいと思う。市場名はそのうちdbアクセスして抜き出そう（引数1つで良くなる） """
    dic = {"HOSE": 'hcm', "HNX": 'hn'}
    url = 'https://www.viet-kabu.com/{0}/{1}.html'.format(dic[mkt], symbol)
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'lxml')
    tag_img = soup.find(id='chart_search_left').find('img')
    if tag_img:
        path = 'mysite/vietnam_research/static/vietnam_research/chart/{0}.png'.format(symbol)
        urllib.request.urlretrieve(tag_img['src'], path)
        print(symbol)
    time.sleep(4)

SYMBOLS = ['SAB', 'GAS', 'PPC', 'VNM', 'VHC', 'PHR', 'FMC', 'VHM', 'VRE']
for i in SYMBOLS:
    scraping('HOSE', i)

# top5
print('top5')
CON = sqlite3.connect('mysite/db.sqlite3')
SQL = '''DELETE FROM vietnam_research_dailytop5'''
CUR = CON.cursor()
CUR.execute(SQL)
AGG_BY_INDNAME = pd.read_sql(
    '''
    SELECT
          c.industry_class || '|' || i.industry1 AS ind_name
        , i.market_code
        , i.symbol
        , AVG(i.closing_price * volume) AS marketcap
        , AVG(i.per) AS per
    FROM vietnam_research_industry i INNER JOIN vietnam_research_industryclassification c
    ON i.industry1 = c.industry1
    GROUP BY ind_name, i.symbol
    HAVING per >1;
    '''
    , CON)
SORT_CRITERIA = [['marketcap', 'per'], ['ind_name', 'marketcap', 'per']]
ORDER_CRITERIA = [False, [True, False, False]]
AGG_BY_INDNAME = AGG_BY_INDNAME.sort_values(by=SORT_CRITERIA[0], ascending=ORDER_CRITERIA[0])
AGG_BY_INDNAME = AGG_BY_INDNAME.groupby('ind_name').head()
AGG_BY_INDNAME = AGG_BY_INDNAME.sort_values(by=SORT_CRITERIA[1], ascending=ORDER_CRITERIA[1])
AGG_BY_INDNAME.to_sql('vietnam_research_dailytop5', CON, if_exists='append', index=None)
for i, row in AGG_BY_INDNAME.iterrows():
    scraping(row['market_code'], row['symbol'])

# log
with open('result.log', mode='a') as f:
    f.write('\n' + datetime.datetime.now().strftime("%Y/%m/%d %a %H:%M:%S ") + 'stock_chart.py')

# Output
print('Congrats!')
