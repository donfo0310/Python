"""子供のurls.pyがこの処理を呼び出します"""
import json
from datetime import datetime
from sqlalchemy import create_engine
from django.shortcuts import render, redirect, HttpResponse
import pandas as pd

from .forms import WatchelistForm
from .models import WatchList, Likes

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
              pub_date
            , industry1
            , truncate(trade_price_of_a_day / 1000000, 2) trade_price_of_a_day
        FROM (
			SELECT
				  DATE_FORMAT(pub_date,'%%Y%%m%%d') pub_date
				, industry1
				, SUM(trade_price_of_a_day) AS trade_price_of_a_day
			FROM vietnam_research_industry
			GROUP BY pub_date, industry1
        ) Q
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
        SELECT DISTINCT Y, M, closing_price
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
        SELECT
              IQ.*
            , FORMAT(i_tdy.closing_price, 0) AS closing_price
            , ROUND(((i_tdy.closing_price / IQ.stocks_price_forcalc) -1) *100, 2)
                AS stocks_price_delta
        FROM
        (
            SELECT DISTINCT
                CASE
                    WHEN market_code = "HOSE" THEN "hcm"
                    WHEN market_code = "HNX" THEN "hn"
                END mkt
                , w.symbol
                , LEFT(CONCAT(i.industry1, ': ', i.company_name), 14) AS company_name
                , CONCAT(YEAR(w.bought_day), '/', MONTH(w.bought_day), '/',
                    DAY(w.bought_day)) AS bought_day
                , FORMAT(w.stocks_price, 0) AS stocks_price
                , w.stocks_price AS stocks_price_forcalc
                , FORMAT(w.stocks_price / 100 / 2, 0) AS stocks_price_yen
                , FORMAT((w.stocks_price / 100 / 2) * w.stocks_count, 0) AS buy_price_yen
                , w.stocks_count
                , i.industry1
            FROM vietnam_research_watchlist w INNER JOIN vietnam_research_industry i
                ON w.symbol = i.symbol
            WHERE already_has = 1
        ) IQ INNER JOIN (
            SELECT
                i.symbol, i.closing_price * 1000 closing_price
            FROM vietnam_research_industry i
            WHERE i.pub_date = (SELECT MAX(i.pub_date) pub_date FROM vietnam_research_industry i)
        ) i_tdy ON IQ.symbol = i_tdy.symbol
        ORDER BY IQ.bought_day;
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

    # uptrends（業種別にグループ化してjsonにします）
    uptrends = []
    temp = pd.read_sql_query(
        '''
        SELECT DISTINCT
              u.ind_name
            , CASE
                WHEN u.market_code = "HOSE" THEN "hcm"
                WHEN u.market_code = "HNX" THEN "hn"
              END mkt
            , u.symbol
            , i.industry1
            , i.company_name
            , u.stocks_price_oldest
            , u.stocks_price_latest
            , u.stocks_price_delta
        FROM vietnam_research_dailyuptrends u INNER JOIN vietnam_research_industry i
            ON u.symbol = i.symbol
        ORDER BY u.ind_name, stocks_price_delta DESC;
        '''
        , con)
    for groups in temp.groupby('ind_name'):
        # print('\n', groups[0])
        inner = {"ind_name": groups[0], "datasets": []}
        for row in groups[1].iterrows():
            inner["datasets"].append({
                "mkt": row[1]['mkt'],
                "symbol": row[1]['symbol'],
                "industry1": row[1]['industry1'],
                "company_name": row[1]['company_name'],
                "stocks_price_oldest": row[1]['stocks_price_oldest'],
                "stocks_price_latest": row[1]['stocks_price_latest'],
                "stocks_price_delta": row[1]['stocks_price_delta']
            })
        uptrends.append(inner)

    # likes
    user_id = 1 # todo: where user_id
    articles = pd.read_sql_query(
        '''
        SELECT a.id, a.title, a.note, COALESCE(qry1.is_like, 0) is_like, qry2.likes_cnt
        FROM vietnam_research_articles a
            LEFT JOIN (
                SELECT articles_id, 1 is_like
                FROM vietnam_research_likes WHERE user_id = {0}) qry1 ON a.id = qry1.articles_id
            LEFT JOIN (
                SELECT articles_id, COUNT(user_id) likes_cnt
                FROM vietnam_research_likes GROUP BY articles_id) qry2 ON a.id = qry2.articles_id
        ORDER BY a.id;
        '''.format(user_id), con)

    # context
    context = {
        'industry_count': json.dumps(industry_count, ensure_ascii=False),
        'industry_cap': json.dumps(industry_cap, ensure_ascii=False),
        'industry_stack': json.dumps(industry_stack, ensure_ascii=False),
        'vnindex_timeline': json.dumps(vnindex_timeline, ensure_ascii=False),
        'vnindex_layers': json.dumps(vnindex_layers, ensure_ascii=False),
        'articles': articles,
        'watchlist': watchelist,
        'basicinfo': basicinfo,
        'top5list': top5,
        'uptrends': json.dumps(uptrends, ensure_ascii=False),
        'form': form
    }

    # htmlとして返却します
    return render(request, 'vietnam_research/index.html', context)

def likes(request, user_id, article_id):
    """いいねボタンをクリック"""
    if request.method == 'POST':
        query = Likes.objects.filter(user_id=user_id, articles_id=article_id)
        if query.count() == 0:
            likes_tbl = Likes()
            likes_tbl.user_id = user_id
            likes_tbl.articles_id = article_id
            likes_tbl.save()
        else:
            query.delete()

        # necessary return?
        return HttpResponse("ajax is done!")
