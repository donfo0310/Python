"""銘柄のチャートをpngで取得します"""
import os
import time
import urllib.request
from bs4 import BeautifulSoup

# chart フォルダがなかったら作成
OUT_FOLDER = os.path.dirname(r'./chart/')
if not os.path.exists(OUT_FOLDER):
    os.makedirs(OUT_FOLDER)

def scraping(mkt, symbol):
    """ symbol をリストで受け入れてガリマワシもいいと思う。市場名はそのうちdbアクセスして抜き出そう（引数1つで良くなる） """
    url = 'https://www.viet-kabu.com/{0}/{1}.html'.format(mkt, symbol)
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'lxml')
    tag_img = soup.find(id='chart_search_left').find('img')
    if tag_img:
        urllib.request.urlretrieve(tag_img['src'], 'chart/{0}.png'.format(symbol))
        print(symbol)
    time.sleep(1)

scraping('hcm', 'SAB')
scraping('hcm', 'GAS')
scraping('hcm', 'PPC')
scraping('hcm', 'VNM')
scraping('hcm', 'VHC')
scraping('hcm', 'PHR')
scraping('hcm', 'FMC')

# Output
print('Congrats!')
