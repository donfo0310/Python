"""子供のurls.pyがこの処理を呼び出します"""
import sqlite3
from django.shortcuts import render
import pandas as pd

def index(request):
    """いわばhtmlのページ単位の構成物です"""

    # dailydata のpivot
    con = sqlite3.connect('db.sqlite3')
    dailydata = pd.read_sql(
        '''
        SELECT
            SUBSTR(REPLACE(d.ymd, '-', ''), 1, 6) ym
            , c.category1 || c.category2 category
            , SUM(d.amount) amount
        FROM bankdata_dailydata d INNER JOIN bankdata_category c ON d.description = c.description
        GROUP BY SUBSTR(REPLACE(d.ymd, '-', ''), 1, 6), c.category1, c.category2
        ORDER BY date(d.ymd), c.category1, c.category2;
        '''
        , con).pivot('category', 'ym', 'amount').fillna(0)

    context = {
        'dailydata': dailydata.to_dict(orient='index'),
    }

    # htmlとして返却します
    return render(request, 'bankdata/index.html', context)
