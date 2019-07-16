"""テンプレートに渡すまでのビジネスロジックです"""
import urllib.request
import json
from bs4 import BeautifulSoup
import geocoder
from django.shortcuts import render

def index(request):
    """Scraping!"""

    # 所在地がhtmlテーブルで載っているようなページ
    url = 'http://www.pref.kanagawa.jp/cnt/f1029/p70915.html'
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'lxml')

    # detail_free クラスのなかの a タグのみを処理対象とする
    json_data = []
    miss_data = []
    detail_free = soup.findAll('div', class_='detail_free')[0]
    for tag_a in detail_free.findAll('a'):
        print(tag_a.text)   # ex. 神奈川県内広域水道企業団
        lat, lng = get_geo(tag_a.text)
        if lat:
            json_data.append({"name":tag_a.text, "lat":lat, "lng":lng})
        else:
            miss_data.append({"name":tag_a.text, "lat":lat, "lng":lng})

    # json変換して保存
    # runserver する場所、すなわち mysite からのパス（ハマりポイント）
    with open('googlemaps/static/googlemaps/js/data.json', 'w') as outfile:
        # ensure_asciiをFalseにすると日本語の文字化けがなくなる
        json.dump(json_data, outfile, indent=4, sort_keys=True, ensure_ascii=False)

    return render(request, 'googlemaps/index.html', context={'json': json_data, 'miss': miss_data})

def get_geo(googlemapkeyword):
    """緯度経度を取得する"""
    geo = geocoder.google(googlemapkeyword)
    return geo.lat, geo.lng
    