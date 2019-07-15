"""子供のurls.pyがこの処理を呼び出します"""
from django.shortcuts import render # 追加！
from .models import DjangoTestTable # 追加！

def index(request):
    """いわばhtmlのページ単位の構成物です"""
    # 日付を降順に表示するクエリ
    ret = DjangoTestTable.objects.order_by('-pub_date')
    context = {'latest_list': ret}
    # htmlとして返却します
    return render(request, 'test_chartjs/index.html', context)
