"""
指定銘柄のチャートをpngで取得します
top5のチャートをpngで取得します
step1: 1企業あたり毎日1明細しかないものを group集計する
step2: pandasでtop5を抽出し、top5テーブルにinsertしたあとにスクレイピング
step3: 傾斜を出して、uptrendを抽出
"""
from os.path import dirname
from os.path import abspath
import time
import urllib.request
import datetime
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image

def scraping(mkt, symbol_):
    """
    url先の <div id="chart_search_left"> の <img> を取得する。
    1つ処理するごとに4秒ほど休むのは、スクレイピングルールです。
    """
    dic = {"HOSE": 'hcm', "HNX": 'hn'}
    url = 'https://www.viet-kabu.com/{0}/{1}.html'.format(dic[mkt], symbol_)
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'lxml')
    tag_img = soup.find(id='chart_search_left').find('img')
    if tag_img:
        path = dirname(abspath(__file__))
        path = path + '/mysite/vietnam_research/static/vietnam_research/chart/{0}.png'
        path = path.format(symbol_)
        urllib.request.urlretrieve(tag_img['src'], path)
        print(symbol_)
    time.sleep(4)

# mysql
CON_STR = 'mysql+mysqldb://python:python123@127.0.0.1/pythondb?charset=utf8&use_unicode=1'
CON = create_engine(CON_STR, echo=False).connect()

# chart1: watchlist
print('watch list')
SYMBOLS = pd.read_sql_query(
    '''
    SELECT DISTINCT
        i.market_code, w.symbol
    FROM vietnam_research_industry i INNER JOIN vietnam_research_watchlist w
    ON i.symbol = w.symbol;
    '''
    , CON)
for i, row in SYMBOLS.iterrows():
    scraping(row['market_code'], row['symbol'])

# chart2: top 5 by industry
print('\n' + 'top 5')
CON.execute('DELETE FROM vietnam_research_dailytop5')
AGG = pd.read_sql_query(
    '''
    SELECT
          CONCAT(c.industry_class, '|', i.industry1) AS ind_name
        , i.market_code
        , i.symbol
        , AVG(i.trade_price_of_a_day) AS trade_price_of_a_day
        , AVG(i.per) AS per
    FROM (vietnam_research_industry i INNER JOIN vietnam_research_indclass c
        ON i.industry1 = c.industry1) INNER JOIN vietnam_research_sbi s
        ON i.market_code = s.market_code AND i.symbol = s.symbol
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

# chart3: uptrend by industry
print('\n' + 'uptrend')
CON.execute('DELETE FROM vietnam_research_dailyuptrends')
AGG = pd.read_sql_query(
    '''
    SELECT
        CONCAT(c.industry_class, '|', i.industry1) AS ind_name
        , i.symbol
        , i.pub_date
        , i.closing_price
    FROM (vietnam_research_industry i INNER JOIN vietnam_research_indclass c
        ON i.industry1 = c.industry1) INNER JOIN vietnam_research_sbi s
        ON i.market_code = s.market_code AND i.symbol = s.symbol
    ORDER BY ind_name, i.symbol, i.pub_date;
    '''
    , CON)
SYMBOLS = []
SLOPES = []
SCORES = []
for symbol, values in AGG.groupby('symbol'):
    days = [-14, -7, -3]
    # plot: closing_price
    plt.clf()
    plt.plot(range(len(values)), values['closing_price'], "ro")
    plt.title(symbol)
    plt.ylabel('closing_price')
    plt.grid()
    slope_inner = []
    score = 0
    for i in range(len(days)):
        values_inner = values[days[i]:]
        x_scale = range(len(values_inner))
        A = np.array([x_scale, np.ones(len(x_scale))]).T
        slope, intercept = np.linalg.lstsq(A, values_inner['closing_price'], rcond=-1)[0]
        slope_inner.append(slope)
        # scoring
        if slope > 0:
            score += 1
        # plot: overwrite fitted line
        plt.plot(x_scale, (slope * x_scale + intercept), "g--")
    # save png: w640, h480
    png_path = dirname(abspath(__file__))
    png_path = png_path + '/mysite/vietnam_research/static/vietnam_research/chart_uptrend/{0}.png'
    png_path = png_path.format(symbol)
    plt.savefig(png_path)
    # resize png: w250, h200
    Image.open(png_path).resize((250, 200), Image.LANCZOS).save(png_path)
    # stack param
    SYMBOLS.append(symbol)
    SLOPES.append(slope_inner)
    SCORES.append(score)
    print(symbol, slope_inner, score)
UPTREND = pd.DataFrame({
    'symbol': SYMBOLS,
    'slopes': SLOPES,
    'score': SCORES
})
UPTREND = UPTREND[UPTREND['score'] == len(days)]
EDIT_SQL = '''
    SELECT
        CONCAT(c.industry_class, '|', i.industry1) AS ind_name
        , i.market_code
        , i.symbol
    FROM (vietnam_research_industry i INNER JOIN vietnam_research_indclass c
        ON i.industry1 = c.industry1) INNER JOIN vietnam_research_sbi s
        ON i.market_code = s.market_code AND i.symbol = s.symbol
    WHERE i.symbol IN ('{SYMBOLS}')
    GROUP BY ind_name, i.market_code, i.symbol
    ORDER BY ind_name, i.market_code, i.symbol;
'''
EDIT_SQL = EDIT_SQL.replace('{SYMBOLS}', "','".join(list(UPTREND['symbol'])))
AGG = pd.read_sql_query(EDIT_SQL, CON)
AGG.to_sql('vietnam_research_dailyuptrends', CON, if_exists='append', index=None)

# log
with open(dirname(abspath(__file__)) + '/result.log', mode='a') as f:
    f.write('\n' + datetime.datetime.now().strftime("%Y/%m/%d %a %H:%M:%S ") + 'stock_chart.py')

# Output
print('Congrats!')
