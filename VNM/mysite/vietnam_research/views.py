"""子供のurls.pyがこの処理を呼び出します"""
import json
from datetime import datetime
from sqlalchemy import create_engine
from django.shortcuts import render, redirect
import pandas as pd

from .forms import WatchelistForm
from .models import WatchList

def index(request):
    """いわばhtmlのページ単位の構成物です"""
    if request.method == 'POST':
        form = WatchelistForm(request.POST)
        if form.is_valid():
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
    # mysql
    con_str = 'mysql+mysqldb://python:python123@127.0.0.1/pythondb?charset=utf8&use_unicode=1'
    con = create_engine(con_str, echo=False).connect()
    # today's details
    temp = pd.read_sql_query(
        '''
        SELECT
              CONCAT(c.industry_class, '|', i.industry1) AS ind_name
            , i.marketcap
        FROM vietnam_research_industry i INNER JOIN vietnam_research_indclass c ON
            i.industry1 = c.industry1
        WHERE DATE(pub_date) = (
                SELECT DATE(MAX(pub_date)) pub_date
                FROM vietnam_research_industry
            );
        '''
        , con)
    # aggregation today's details
    industry_count = []
    industry_cap = []
    temp = pd.DataFrame({
        'cnt_per': \
            (temp.groupby('ind_name').count() / len(temp))['marketcap'].values.tolist(),
        'cap_per': \
            (temp.groupby('ind_name').sum() / temp['marketcap'].sum())['marketcap'].values.tolist()
    }, index=list(temp.groupby('ind_name').groups.keys()))
    temp['cnt_per'] = (temp['cnt_per'] * 100).round(1)
    temp['cap_per'] = (temp['cap_per'] * 100).round(1)
    inner = []
    for row in temp.iterrows():
        inner.append({"axis": row[0], "value": row[1]["cnt_per"]})
    industry_count.append({"name": '企業数', "axes": inner})
    inner = []
    for row in temp.iterrows():
        inner.append({"axis": row[0], "value": row[1]["cap_per"]})
    industry_cap.append({"name": '時価総額', "axes": inner})

    # daily chart stack
    temp = pd.read_sql_query(
        '''
        SELECT
              DATE_FORMAT(pub_date,'%%Y%%m%%d') pub_date
            , industry1
            , SUM(trade_price_of_a_day) AS trade_price_of_a_day
        FROM vietnam_research_industry
        GROUP BY pub_date, industry1
        ORDER BY pub_date, industry1;
        '''
        , con)
    industry_pivot = pd.pivot_table(temp, index='pub_date', \
        columns='industry1', values='trade_price_of_a_day', aggfunc='sum')
    industry_stack = {"labels": list(industry_pivot.index), "datasets": []}
    colors = ['#7b9ad0', '#f8e352', '#c8d627', '#d5848b', '#e5ab47']
    colors.extend(['#e1cea3', '#51a1a2', '#b1d7e4', '#66b7ec', '#c08e47', '#ae8dbc'])
    for i, ele in enumerate(temp.groupby('industry1').groups.keys()):
        industry_stack["datasets"].append({"label": ele, "backgroundColor": colors[i]})
        value = list(temp.groupby('industry1').get_group(ele)['trade_price_of_a_day'])
        industry_stack["datasets"][i]["data"] = value
    # print('\n【data from】\n', industry_pivot)
    # print('\n【data to】\n', industry_stack, '\n')

    # vnindex
    temp = pd.read_sql_query(
        '''
        SELECT Y, M, closing_price
        FROM vietnam_research_vnindex
        ORDER BY Y, M;
        '''
        , con)
    # vnindex: simple timeline
    vnindex_timeline = {"labels": list(temp['Y'] + temp['M']), "datasets": []}
    inner = {"label": 'VN-Index', "data": list(temp['closing_price'])}
    vnindex_timeline["datasets"].append(inner)
    # vnindex: annual layer
    vnindex_pivot = temp.pivot('Y', 'M', 'closing_price').fillna(0)
    vnindex_layers = {"labels": list(vnindex_pivot.columns.values), "datasets": []}
    for i, yyyy in enumerate(vnindex_pivot.iterrows()):
        inner = {"label": yyyy[0], "data": list(yyyy[1])}
        vnindex_layers["datasets"].append(inner)
    # print('vnindex_pivot: ', vnindex_pivot)

    # watchlist
    watchelist = pd.read_sql_query(
        '''
        SELECT DISTINCT
              CASE
                WHEN market_code = "HOSE" THEN "hcm"
                WHEN market_code = "HNX" THEN "hn"
              END mkt
            , w.symbol
            , CONCAT('(', i.industry1, ')', w.symbol, ' ', i.company_name) AS company_name
            , w.bought_day
            , w.stocks_price
            , w.stocks_count
            , w.bikou
            , already_has
            , i.industry1
        FROM vietnam_research_watchlist w INNER JOIN vietnam_research_industry i
            ON w.symbol = i.symbol
        WHERE already_has = 1
        ORDER BY already_has DESC, i.industry1;
        '''
        , con)

    # basicinfo
    basicinfo = pd.read_sql_query(
        '''
        SELECT
              b.item
            , b.description
        FROM vietnam_research_basicinformation b
        ORDER BY b.id;
        '''
        , con)

    # top5
    top5 = pd.read_sql_query(
        '''
        SELECT
            *
            , CASE
                WHEN market_code = "HOSE" THEN "hcm"
                WHEN market_code = "HNX" THEN "hn"
              END mkt
        FROM vietnam_research_dailytop5;
        '''
        , con)
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
