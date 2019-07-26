"""子供のurls.pyがこの処理を呼び出します"""
from django.shortcuts import render
from django.db.models import Count, Sum
from .models import Industry

def index(request):
    """いわばhtmlのページ単位の構成物です"""
    # industry1を集計する
    cnt_agg = Industry.objects.values('industry1').annotate(cnt_per=Sum('count_per'))
    cap_agg = Industry.objects.values('industry1').annotate(cap_per=Sum('marketcap_per'))
    context = {
        'industry': cnt_agg,
        'marketcap': cap_agg
        }
    # htmlとして返却します
    return render(request, 'vietnam_research/index.html', context)
