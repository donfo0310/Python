"""銘柄のチャートをpngで取得します"""
import time
import urllib.request
import datetime
from bs4 import BeautifulSoup

def scraping(mkt, symbol):
    """ symbol をリストで受け入れてガリマワシもいいと思う。市場名はそのうちdbアクセスして抜き出そう（引数1つで良くなる） """
    url = 'https://www.viet-kabu.com/{0}/{1}.html'.format(mkt, symbol)
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'lxml')
    tag_img = soup.find(id='chart_search_left').find('img')
    if tag_img:
        path = 'mysite/vietnam_research/static/vietnam_research/chart/{0}.png'.format(symbol)
        urllib.request.urlretrieve(tag_img['src'], path)
        print(symbol)
    time.sleep(4)

scraping('hcm', 'SAB')
scraping('hcm', 'GAS')
scraping('hcm', 'PPC')
scraping('hcm', 'VNM')
scraping('hcm', 'VHC')
scraping('hcm', 'PHR')
scraping('hcm', 'FMC')
scraping('hcm', 'VHM')
scraping('hcm', 'VRE')


# log
with open('result.log', mode='a') as f:
    f.write('\n' + datetime.datetime.now().strftime("%Y/%m/%d %a %H:%M:%S ") + 'stock_chart.py')

# Output
print('Congrats!')
