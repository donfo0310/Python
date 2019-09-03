"""
指定銘柄のチャートをpngで取得します
top5のチャートをpngで取得します
step1: 1企業あたり毎日1明細しかないものを group集計する
step2: pandasでtop5を抽出し、top5テーブルにinsertしたあとにスクレイピング

improvement(top5):
    trade_price_of_a_day が「平均値」として潰れてしまうため、本当は「傾斜」を出すのが良い

    Using Pandas groupby to calculate many slopes:
    https://stackoverflow.com/questions/29907133/using-pandas-groupby-to-calculate-many-slopes
    どうも日付だったから（数字じゃないから）できなかったようだ？

    having句の表現:
    https://qiita.com/iowanman/items/174d5cb3088fafc82962
    df.groupby(by=["symbol"]).mean().loc[lambda x: x["per"]> 1]
"""
import time
import urllib.request
import datetime
import sqlite3
from bs4 import BeautifulSoup
import pandas as pd

def scraping(mkt, symbol):
    """
    url先の <div id="chart_search_left"> の <img> を取得する。
    1つ処理するごとに4秒ほど休むのは、スクレイピングルールです。
    """
    dic = {"HOSE": 'hcm', "HNX": 'hn'}
    url = 'https://www.viet-kabu.com/{0}/{1}.html'.format(dic[mkt], symbol)
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'lxml')
    tag_img = soup.find(id='chart_search_left').find('img')
    if tag_img:
        path = 'mysite/vietnam_research/static/vietnam_research/chart/{0}.png'.format(symbol)
        urllib.request.urlretrieve(tag_img['src'], path)
        print(symbol)
    time.sleep(4)

# chart1: specified
print('specified list')
SYMBOLS = ['SAB', 'GAS', 'PPC', 'VNM', 'VHC', 'PHR', 'FMC', 'VHM', 'VRE']
for i in SYMBOLS:
    scraping('HOSE', i)

# chart2: top 5 by industry
print('\n' + 'top 5')
CON = sqlite3.connect('mysite/db.sqlite3')
SQL = '''DELETE FROM vietnam_research_dailytop5'''
CUR = CON.cursor()
CUR.execute(SQL)
AGG = pd.read_sql(
    '''
    SELECT
          c.industry_class || '|' || i.industry1 AS ind_name
        , i.market_code
        , i.symbol
        , AVG(trade_price_of_a_day) AS trade_price_of_a_day
        , AVG(i.per) AS per
    FROM vietnam_research_industry i INNER JOIN vietnam_research_industryclassification c
    ON i.industry1 = c.industry1
    GROUP BY ind_name, i.market_code, i.symbol
    HAVING per >1;
    '''
    , CON)
# criteria
CRITERIA = []
CRITERIA.append({"by": ['trade_price_of_a_day', 'per'], "order": False})
CRITERIA.append({"by": ['ind_name', 'trade_price_of_a_day', 'per'], "order": [True, False, False]})
# Sort descending and get top 5
AGG = AGG.sort_values(by=CRITERIA[0]["by"], ascending=CRITERIA[0]["order"])
AGG = AGG.groupby('ind_name').head()
# Sort descending and insert table
AGG = AGG.sort_values(by=CRITERIA[1]["by"], ascending=CRITERIA[1]["order"])
AGG.to_sql('vietnam_research_dailytop5', CON, if_exists='append', index=None)
# scraping from top 5 list
for i, row in AGG.iterrows():
    scraping(row['market_code'], row['symbol'])

# log
with open('result.log', mode='a') as f:
    f.write('\n' + datetime.datetime.now().strftime("%Y/%m/%d %a %H:%M:%S ") + 'stock_chart.py')

# Output
print('Congrats!')