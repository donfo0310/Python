"""子供のurls.pyがこの処理を呼び出します"""
import sqlite3
import json
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

    # 日次積み上げグラフ
    temp = pd.read_sql(
        '''
        SELECT
              STRFTIME('%m/%d', DATE(pub_date)) AS pub_date
            , industry1
            , SUM(trade_price_of_a_day) AS trade_price_of_a_day
        FROM vietnam_research_industry
        GROUP BY pub_date, industry1
        ORDER BY pub_date, industry1;
        '''
        , con)
    industry_pivot = temp.pivot('pub_date', 'industry1', 'trade_price_of_a_day')
    industry_stack = {"labels": industry_pivot.index.to_list(), "datasets": []}
    colors = ['#7b9ad0', '#f8e352', '#c8d627', '#d5848b', '#e5ab47']
    colors.extend(['#e1cea3', '#51a1a2', '#b1d7e4', '#66b7ec', '#c08e47', '#ae8dbc'])
    for i, ele in enumerate(temp.groupby('industry1').groups.keys()):
        industry_stack["datasets"].append({"label": ele, "backgroundColor": colors[i]})
        value = temp.groupby('industry1').get_group(ele)['trade_price_of_a_day'].to_list()
        industry_stack["datasets"][i]["data"] = value
    print('\n【data from】\n', industry_pivot)
    print('\n【data to】\n', industry_stack, '\n')

    # vnindex の月次ミルフィーユ
    vnindex = pd.read_sql(
        '''
        SELECT Y, M, closing_price
        FROM vietnam_research_vnindex
        ORDER BY Y, M;
        '''
        , con).pivot('Y', 'M', 'closing_price').fillna(0)

    # watchlist
    watchelist = pd.read_sql(
        '''
        SELECT DISTINCT
              w.symbol
            , '(' || i.industry1 || ')' || w.symbol || ' ' || i.company_name AS company_name
            , w.bought_day
            , w.stocks_price
            , w.stocks_count
            , w.bikou
        FROM vietnam_research_watchlist w INNER JOIN vietnam_research_industry i
        ON w.symbol = i.symbol
        ORDER BY already_has DESC, i.industry1;
        '''
        , con)

    # basicinfo
    basicinfo = pd.read_sql(
        '''
        SELECT
              b.item
            , b.description
        FROM vietnam_research_basicinformation b
        ORDER BY b.id;
        '''
        , con)

    # top5
    top5 = pd.read_sql('SELECT * FROM vietnam_research_dailytop5;', con)
    sort_criteria = ['ind_name', 'marketcap', 'per']
    order_criteria = [True, False, False]
    top5 = top5.sort_values(by=sort_criteria[0], ascending=order_criteria[0])

    # context
    context = {
        'industry': industry,
        'industry_stack': json.dumps(industry_stack, ensure_ascii=False),
        'vnindex': vnindex.to_dict(orient='index'),
        'watchlist': watchelist,
        'basicinfo': basicinfo,
        'top5list': top5
    }

    # htmlとして返却します
    return render(request, 'vietnam_research/index.html', context)
