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
        lat, lng = get_geo(tag_a.text)
        if lat:
            json_data.append({"name":tag_a.text, "lat":lat, "lng":lng})
            print(tag_a.text, 'OK')   # ex. 神奈川県内広域水道企業団
            get_mapimage(tag_a.text)  # 画像の保存
        else:
            miss_data.append({"name":tag_a.text, "lat":lat, "lng":lng})
            print(tag_a.text, 'NG')   # ex. 神奈川県内広域水道企業団

    # json変換して保存
    # runserver する場所、すなわち mysite からのパス（ハマりポイント）
    with open('googlemaps/static/googlemaps/js/data.json', 'w') as outfile:
        # ensure_asciiをFalseにすると日本語の文字化けがなくなる
        json.dump(json_data, outfile, indent=4, sort_keys=True, ensure_ascii=False)

    return render(request, 'googlemaps/index.html', context={'json': json_data, 'miss': miss_data})

def get_geo(place):
    """
    Parameters
    ----------
    place: e.g. 東京都
    Returns
    -------
    (35.6828387,139.7594549)
    """
    geo = geocoder.osm(place)
    return geo.lat, geo.lng

def get_mapimage(place, size=(250, 240), img_format='png'):
    """
    dependency
    ----------
    Maps Static API
    Parameters
    ----------
    place: e.g. 東京都\n
    size: (width, height) 最大 640x640\n
    img_format: png(png8), png32, gif, jpg\n
    """
    # read apikey from textfile
    with open('googlemaps/api_setting/appid.txt', mode='r', encoding='utf-8') as file:
        apikey = file.read()
    # make url
    url = 'https://maps.googleapis.com/maps/api/staticmap?center={}' \
        '&size={}&zoom=18&format={}&maptype=roadmap&key={}'
    lat, lng = get_geo(place)
    location = '{},{}'.format(lat, lng)
    size_param = '{}x{}'.format(*size)
    url = url.format(location, size_param, img_format, apikey)
    file_name = 'googlemaps/static/googlemaps/img/' + '{}.{}'.format(place, img_format[:3])
    res = urllib.request.urlopen(url)
    if res.code == 200:
        with open(file_name, 'wb') as file:
            file.write(res.read())
