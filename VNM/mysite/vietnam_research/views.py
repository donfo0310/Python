"""子供のurls.pyがこの処理を呼び出します"""
from django.shortcuts import render
from django.db import connection

def index(request):
    """いわばhtmlのページ単位の構成物です"""
    # industry1を集計する
    cursor = connection.cursor()
    cursor.execute(
        '''
        SELECT
              c.industry_class || '|' || i.industry1 AS ind_name
            , ROUND(SUM(count_per),2) AS cnt_per
            , ROUND(SUM(marketcap_per),2) AS cap_per
        FROM vietnam_research_industry i INNER JOIN vietnam_research_industryclassification c
        ON i.industry1 = c.industry1
        GROUP BY i.industry1, c.industry_class
        ORDER BY ind_name;
        ''')
    industry = cursor.fetchall()
    context = {'industry': industry}

    # htmlとして返却します
    return render(request, 'vietnam_research/index.html', context)
