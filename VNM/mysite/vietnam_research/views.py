"""子供のurls.pyがこの処理を呼び出します"""
from django.shortcuts import render
from django.db.models import Count, Sum
from .models import Industry

def index(request):
    """いわばhtmlのページ単位の構成物です"""
    # industry1を集計する
    ind_count = Industry.objects.values('industry1').annotate(cnt=Count('industry1'))
    cap_sum = Industry.objects.values('industry1').annotate(agg=Sum('marketcap'))
    context = {'industry': ind_count, 'marketcap': cap_sum}
    # htmlとして返却します
    return render(request, 'vietnam_research/index.html', context)
