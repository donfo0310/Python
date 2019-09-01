"""
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

import sqlite3
import pandas as pd
from scipy.stats import linregress

# stackoverflow
X = pd.DataFrame({
    'entity':['a', 'a', 'b', 'b', 'b'],
    'year':["19990101", "20040101", "20030101", "20070101", "20140101"],
    'value':[2, 5, 3, 2, 7]})
X.year = X.year.astype(int) # 型変換すれば通る
print(X)
print(X.dtypes)
print(X.groupby('entity').apply(lambda v: linregress(v.year, v.value)[0]))

# having value > 2
print(X.groupby('entity').mean().loc[lambda v: v.value > 2])

# またチャレンジしようね
CON = sqlite3.connect('mysite/db.sqlite3')
AGG = pd.read_sql(
    '''
    SELECT
          c.industry_class || '|' || i.industry1 AS ind_name
        , i.market_code
        , i.symbol
        , CAST(REPLACE(DATE(i.pub_date), '-', '') AS int) AS pub_date
        , trade_price_of_a_day
        , i.per
    FROM vietnam_research_industry i INNER JOIN vietnam_research_industryclassification c
    ON i.industry1 = c.industry1;
    '''
    , CON)
print(AGG.dtypes)

# linregress
AGG = AGG.groupby('symbol').apply(lambda v: linregress(v.pub_date, v.trade_price_of_a_day)[0])
print(AGG)
# having value > 2
# print(AGG.groupby('symbol').mean().loc[lambda v: v.per > 2])

# criteria
CRITERIA = []
CRITERIA.append({"by": ['trade_price_of_a_day', 'per'], "order": False})
CRITERIA.append({"by": ['ind_name', 'trade_price_of_a_day', 'per'], "order": [True, False, False]})
# Sort descending and get top 5
# AGG = AGG.sort_values(by=CRITERIA[0]["by"], ascending=CRITERIA[0]["order"])
# AGG = AGG.groupby('ind_name').head()
# # Sort descending and insert table
# AGG = AGG.sort_values(by=CRITERIA[1]["by"], ascending=CRITERIA[1]["order"])

# Output
print('Congrats!')
