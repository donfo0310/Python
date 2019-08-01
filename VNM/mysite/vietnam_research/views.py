"""子供のurls.pyがこの処理を呼び出します"""
import sqlite3
from django.shortcuts import render
import pandas as pd

def index(request):
    """いわばhtmlのページ単位の構成物です"""

    # 業種別個社数、業種別時価総額
    con = sqlite3.connect('db.sqlite3')
    industry = pd.read_sql(
        '''
        SELECT
            c.industry_class || '|' || i.industry1 AS ind_name
            , ROUND(SUM(count_per),2) AS cnt_per
            , ROUND(SUM(marketcap_per),2) AS cap_per
        FROM vietnam_research_industry i INNER JOIN vietnam_research_industryclassification c
        ON i.industry1 = c.industry1
        GROUP BY i.industry1, c.industry_class
        ORDER BY ind_name;
        '''
        , con)

    # vnindex の月次ミルフィーユ
    vnindex = pd.read_sql(
        '''
        SELECT Y, M, closing_price
        FROM vietnam_research_vnindex
        ORDER BY Y, M;
        '''
        , con).pivot('Y', 'M', 'closing_price').fillna(0)

    context = {
        'industry': industry,
        'vnindex': vnindex.to_json(orient='index')
    }

    # htmlとして返却します
    return render(request, 'vietnam_research/index.html', context)
