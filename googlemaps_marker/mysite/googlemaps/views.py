"""テンプレートに渡すまでのビジネスロジックです"""
import urllib.request
import json
from bs4 import BeautifulSoup
import geocoder
from django.shortcuts import render

def index(request):
    """Scraping!"""

    # read apikey
    with open('googlemaps/api_setting/apikey.txt', mode='r', encoding='utf-8') as file:
        apikey = file.read()

    # 所在地がhtmlテーブルで載っているようなページ
    url = 'http://www.pref.kanagawa.jp/cnt/f1029/p70915.html'
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'lxml')

    # detail_free クラスのなかの a タグのみを処理対象とする
    json_data = []
    miss_data = []
    for tag_a in soup.findAll('div', class_='detail_free')[0].findAll('a'):
        # place_j: e.g. 神奈川県内広域水道企業団
        place_j = tag_a.text
        lat, lng = get_geo(place_j)
        rating = get_rating(apikey, place_j)
        link = get_link(apikey, get_placeid(apikey, place_j))
        if lat:
            json_data.append({"name":place_j, "lat":lat, "lng":lng, "rating":rating, "url":link})
            print(place_j, 'OK')
            debugsw = 2
            if debugsw == 1:
                # save the zooming googlemap image
                get_mapimage(apikey, place_j)
            else:
                # save the place photo: Always here
                file_path = 'googlemaps/static/googlemaps/img/' + '{}.{}'
                file_path = file_path.format(place_j, 'png')
                get_picture(apikey, get_photoreference(apikey, place_j), file_path)
        else:
            miss_data.append({"name":place_j, "lat":lat, "lng":lng, "rating":rating, "url":link})
            print(place_j, 'NG')

    # save to json: manage.pyのある場所すなわち mysite からのパス（ハマりポイント）
    with open('googlemaps/static/googlemaps/js/data.json', 'w') as outfile:
        # ensure_asciiをFalseにすると日本語の文字化けがなくなる
        json.dump(json_data, outfile, indent=4, sort_keys=True, ensure_ascii=False)

    return render(request, 'googlemaps/index.html', context={'json': json_data, 'miss': miss_data})

def get_geo(place):
    """
    using OpenStreetMap
    Parameters
    ----------
    place: e.g. 東京都
    Returns
    -------
    (35.6828387,139.7594549)
    """
    geo = geocoder.osm(place)
    return geo.lat, geo.lng

def get_mapimage(apikey, place, size=(250, 240), img_format='png'):
    """
    dependency
    ----------
    Maps Static API
    parameters
    ----------
    place: 東京都\n
    size: (width, height) 最大 640x640\n
    img_format: png(png8), png32, gif, jpg\n
    """
    url = 'https://maps.googleapis.com/maps/api/staticmap?center={}' \
        '&size={}&zoom=18&format={}&maptype=roadmap&key={}'
    lat, lng = get_geo(place)
    location = '{},{}'.format(lat, lng)
    size_param = '{}x{}'.format(*size)
    url = url.format(location, size_param, img_format, apikey)
    res = urllib.request.urlopen(url)
    if res.code == 200:
        file_path = 'googlemaps/static/googlemaps/img/' + '{}.{}'.format(place, img_format[:3])
        with open(file_path, 'wb') as file:
            file.write(res.read())

def get_rating(apikey, place):
    '''
    dependency
    ----------
    Places API
    parameters
    ----------
    place: 東京都
    return
    ------
    e.g. 4.5
    '''
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?' \
        'input={}&inputtype=textquery&fields=rating&key={}'
    url = url.format(urllib.parse.quote(place), apikey)
    res = urllib.request.urlopen(url)
    rating = None
    if res.code == 200:
        res_json = json.loads(res.read())
        if res_json.get('candidates'):
            if res_json["candidates"][0].get("rating"):
                rating = res_json["candidates"][0]["rating"]
            else:
                rating = 0
    return rating

def get_placeid(apikey, place):
    '''
    dependency
    ----------
    Places API
    parameters
    ----------
    place: 東京都
    return
    ------
    e.g. CmRaAAAARRAYThPn0sTB1aE-Afx0_...
    '''
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?' \
        'input={}&inputtype=textquery&fields=place_id&key={}'
    url = url.format(urllib.parse.quote(place), apikey)
    res = urllib.request.urlopen(url)
    retvalue = None
    if res.code == 200:
        res_json = json.loads(res.read())
        if res_json.get("candidates"):
            retvalue = res_json["candidates"][0].get("place_id")
    return retvalue

def get_link(apikey, place_id):
    '''
    dependency
    ----------
    Places API
    parameters
    ----------
    place_id: ChIJN1t_tDeuEmsRUsoyG83frY4
    return
    ------
    e.g. https://maps.google.com/?cid=10281119596374313554
    '''
    retvalue = '#'
    if place_id:
        url = 'https://maps.googleapis.com/maps/api/place/details/json?' \
            'place_id={}&fields=url&key={}'.format(place_id, apikey)
        res = urllib.request.urlopen(url)
        if res.code == 200:
            res_json = json.loads(res.read())
            if res_json.get("result"):
                if res_json["result"].get("url"):
                    retvalue = res_json["result"]["url"]
    return retvalue

def get_photoreference(apikey, place):
    '''
    dependency
    ----------
    Places API
    parameters
    ----------
    place: 東京都
    return
    ------
    e.g. CmRaAAAARRAYThPn0sTB1aE-Afx0_...
    '''
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?' \
        'input={}&inputtype=textquery&fields=photos&key={}'
    url = url.format(urllib.parse.quote(place), apikey)
    res = urllib.request.urlopen(url)
    retvalue = None
    if res.code == 200:
        res_json = json.loads(res.read())
        if res_json.get("candidates"):
            if res_json["candidates"][0].get("photos"):
                retvalue = res_json["candidates"][0]["photos"][0].get("photo_reference")
    return retvalue

def get_picture(apikey, photoreference, file_path, size=(250, 240)):
    '''
    dependency
    ----------
    Places API
    parameters
    ----------
    photoreference: CmRaAAAARRAYThPn0sTB1aE-Afx0_...\n
    file_path: .../static/googlemaps/img/東京タワー.png
    '''
    if photoreference:
        url = 'https://maps.googleapis.com/maps/api/place/photo?' \
            'maxwidth={}&maxheight={}&photoreference={}&key={}'
        url = url.format(*size, photoreference, apikey)
        res = urllib.request.urlopen(url)
        if res.code == 200:
            with open(file_path, 'wb') as file:
                file.write(res.read())
