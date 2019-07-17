"""銘柄のチャートをpngで取得します"""
import os
import urllib.request
from bs4 import BeautifulSoup

# data フォルダがなかったら作成
OUT_FOLDER = os.path.dirname(r'./data/')
if not os.path.exists(OUT_FOLDER):
    os.makedirs(OUT_FOLDER)

def scraping(mkt, symbol):
    """ symbol をリストで受け入れてガリマワシもいいと思う。市場名はそのうちdbアクセスして抜き出そう（引数1つで良くなる） """

    # 画像URLスクレイピング編
    # https://qiita.com/neet-AI/items/98d4194872ee4f53e3b4#%E7%94%BB%E5%83%8Furl%E3%82%B9%E3%82%AF%E3%83%AC%E3%82%A4%E3%83%94%E3%83%B3%E3%82%B0%E7%B7%A8

    # https://www.viet-kabu.com/hcm/SAB.html
    # (hcm, hn) also (VNM, GAS)
    url = 'https://www.viet-kabu.com/{0}/{1}.html'.format(mkt, symbol)
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'lxml')
    tag_img = soup.find('img')
    if tag_img:
        res = urllib.request.urlopen(tag_img['src'])
        with open('data/{0}.png', 'wb') as file:
            file.write(res.content)

scraping('hcm', 'SAB')

# Output
print('Congrats!')
