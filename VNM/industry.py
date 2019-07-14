import os, re
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

mkt_code = []
symbol = []
company_name = []
industry1 = []
industry2 = []

# data フォルダがなかったら作成
out_folder = os.path.dirname(r'./data/')
if not os.path.exists(out_folder):
    os.makedirs(out_folder)

# ホーチミン証券取引所
url = 'https://www.viet-kabu.com/stock/hcm.html'
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'lxml')
for td in soup.find_all('td', class_='table_list_center'):
    a = td.find('a')
    if a:
        mkt_code.append('HOSE')
        symbol.append(a.text.strip())
        company_name.append(a.get('title'))
    img = td.find('img')
    if img:
        industry1.append(re.sub(r'\[(.+)\]', '', img.get('title')))
        industry2.append(re.search(r'\[(.+)\]', img.get('title')).group(1))

# ハノイ証券取引所
url = 'https://www.viet-kabu.com/stock/hn.html'
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'lxml')
for td in soup.find_all('td', class_='table_list_center'):
    a = td.find('a')
    if a:
        mkt_code.append('HNX')
        symbol.append(a.text.strip())
        company_name.append(a.get('title'))
    img = td.find('img')
    if img:
        industry1.append(re.sub(r'\[(.+)\]', '', img.get('title')))
        industry2.append(re.search(r'\[(.+)\]', img.get('title')).group(1))

# Output
df = pd.DataFrame({'Market_code':mkt_code, 'Symbol':symbol, 'Company_name':company_name, 'industry1':industry1, 'industry2':industry2})
df.to_csv('data/industry.csv', index=False)
print('Congrats!')