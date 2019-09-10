"""子供のurls.pyがこの処理を呼び出します"""
import sqlite3
import json
from datetime import datetime
from django.shortcuts import render, redirect
import pandas as pd

from .forms import WatchelistForm
from .models import WatchList

def index(request):
    """いわばhtmlのページ単位の構成物です"""
    if request.method == 'POST':
        form = WatchelistForm(request.POST)
        print('i am post.')
        if form.is_valid():
            print('i am valid.')
            # form data
            buy_symbol = form.cleaned_data['buy_symbol']
            buy_date = form.cleaned_data['buy_date']
            buy_cost = form.cleaned_data['buy_cost']
            buy_stocks = form.cleaned_data['buy_stocks']
            buy_bikou = form.cleaned_data['buy_bikou']
            # db regist
            watchlist = WatchList()
            watchlist.symbol = buy_symbol
            watchlist.already_has = True
            watchlist.bought_day = buy_date
            watchlist.stocks_price = buy_cost
            watchlist.stocks_count = buy_stocks
            watchlist.bikou = buy_bikou
            watchlist.save()
            # redirect
            return redirect('vnm:index')
    else:
        form = WatchelistForm()
        form.buy_date = datetime.today().strftime("%Y/%m/%d")

    # count by industry, marketcap by industry
    con = sqlite3.connect('db.sqlite3')
    temp = pd.read_sql(
        '''
        SELECT
            c.industry_class || '|' || i.industry1 AS ind_name
            , ROUND(SUM(count_per),2) AS cnt_per
            , ROUND(SUM(marketcap_per),2) AS cap_per
        FROM ((vietnam_research_industry i
        INNER JOIN vietnam_research_industryclassification c
            ON i.industry1 = c.industry1)
        INNER JOIN (SELECT MAX(pub_date) AS pub_date FROM vietnam_research_industry) X
            ON i.pub_date = X.pub_date )
        GROUP BY i.industry1, c.industry_class
        ORDER BY ind_name;
        '''
        , con)
    industry_count = []
    industry_cap = []
    inner = []
    for row in temp.iterrows():
        inner.append({"axis": row[1]["ind_name"], "value": row[1]["cnt_per"]})
    industry_count.append({"name": '企業数', "axes": inner})
    inner = []
    for row in temp.iterrows():
        inner.append({"axis": row[1]["ind_name"], "value": row[1]["cap_per"]})
    industry_cap.append({"name": '時価総額', "axes": inner})

    # daily chart stack
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
    # print('\n【data from】\n', industry_pivot)
    # print('\n【data to】\n', industry_stack, '\n')

    # vnindex
    temp = pd.read_sql(
        '''
        SELECT Y, M, closing_price
        FROM vietnam_research_vnindex
        ORDER BY Y, M;
        '''
        , con)
    # vnindex: simple timeline
    vnindex_timeline = {"labels": (temp['Y'] + temp['M']).to_list(), "datasets": []}
    inner = {"label": 'VN-Index', "data": temp['closing_price'].to_list()}
    vnindex_timeline["datasets"].append(inner)
    # vnindex: annual layer
    vnindex_pivot = temp.pivot('Y', 'M', 'closing_price').fillna(0)
    vnindex_layers = {"labels": list(vnindex_pivot.columns.values), "datasets": []}
    for i, yyyy in enumerate(vnindex_pivot.iterrows()):
        inner = {"label": yyyy[0], "data": list(yyyy[1])}
        vnindex_layers["datasets"].append(inner)
    # print('vnindex_pivot: ', vnindex_pivot)

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
        'industry_count': json.dumps(industry_count, ensure_ascii=False),
        'industry_cap': json.dumps(industry_cap, ensure_ascii=False),
        'industry_stack': json.dumps(industry_stack, ensure_ascii=False),
        'vnindex_timeline': json.dumps(vnindex_timeline, ensure_ascii=False),
        'vnindex_layers': json.dumps(vnindex_layers, ensure_ascii=False),
        'watchlist': watchelist,
        'basicinfo': basicinfo,
        'top5list': top5,
        'form': form
    }

    # htmlとして返却します
    return render(request, 'vietnam_research/index.html', context)
