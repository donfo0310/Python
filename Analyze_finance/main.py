# RでXBRLデータを取得してみた
# http://horihorio.hatenablog.com/entry/2014/12/15/235107
# 取得データからデータマートを作ろうとしてみた
# http://horihorio.hatenablog.com/entry/2014/12/19/011234
# 投資するための財務分析step1「財務情報XBRLを取得する」
# https://qiita.com/NaoyaOura/items/4f613525063d0c8d6653
# ElementTreeやlxmlで名前空間を含むXMLの要素を取得する
# https://orangain.hatenablog.com/entry/namespaces-in-xpath

# 金融庁がいつのまにかナイスな動きをしてた
# EDINET、データを加工しやすく 金融庁 2019/4/3 20:00 日本経済新聞 電子版
# https://www.nikkei.com/article/DGXMZO43279810T00C19A4EE9000/
# https://disclosure.edinet-fsa.go.jp/EKW0EZ0015.html

import pyodbc
import pandas as pd
import os, re, io, shutil, time, urllib
import xml.etree.ElementTree as ET
from zipfile import ZipFile

# APIを使ってダウンロードをかける「上場企業のコード一覧」を作成する
# あらかじめ市場ファイルをmasterフォルダにCSVで保存してください
# https://www.jpx.co.jp/markets/statistics-equities/misc/01.html
files = os.listdir('./master')
df = pd.DataFrame()
col_order = ['日付','コード','銘柄名','市場・商品区分','33業種コード','33業種区分']
for f in files:
    # CSV Only!!
    if(f[-4:] == '.csv'):
        # Open and combine files
        lines = pd.read_csv(r'./master/' + f)[col_order]
        lines = lines[~(lines['市場・商品区分'] == 'ETF・ETN')] # インデックスなど
        lines = lines[~(lines['市場・商品区分'] == '出資証券')] # 日銀など
        lines = lines[~(lines['市場・商品区分'] == 'REIT・ベンチャーファンド・カントリーファンド・インフラファンド')] # REIT
        df = pd.concat([df, lines], axis=0, sort=True)
print(' '.join(lines.groupby('市場・商品区分')['市場・商品区分'].count().astype(str).tolist()))

# xbrl フォルダを消す（前回ファイルの削除）
out_folder = os.path.dirname(r'./xbrl/')
if os.path.exists(out_folder):
    shutil.rmtree(out_folder)
# xbrl フォルダを作成
os.makedirs(out_folder)

# ex. http://resource.ufocatch.com/atom/edinetx/query/1301
url_base = "http://resource.ufocatch.com/atom/edinetx"
# the date range
date = {'from':'2019-04-01', 'to':'2019-06-30'}
# the namespace as 'default'
ns = {'default':'http://www.w3.org/2005/Atom'}

# proc time
t = []
t.append(time.strftime("%Y/%m/%d %H:%M:%S", time.strptime(time.ctime())))

# Get XBRL
for securities_code in df['コード'].astype(str):

    # ex. '極洋'
    company_name = df[df['コード'].astype(str) == securities_code]['銘柄名'].iloc[0]

    try:
        # Get xml root
        with urllib.request.urlopen(url_base + '/query/' + securities_code) as res:
            root = ET.fromstring(res.read())

        # Get 'entry' tag
        for entry in root.findall('./default:entry', ns):
            edinet_id = entry.find('./default:id', ns).text
            title = entry.find('./default:title', ns).text.replace('\u3000', ' ')
            edinet_code = re.sub(r'^【(\w+)】.*', r'\1', title)
            url = entry.find('./default:link[@type="application/zip"]', ns).attrib['href']
            updated = entry.find('./default:updated', ns).text[:10]
            # Does the text contain specific characters '有価証券報告書' if except for '訂正有価証券報告書'
            if title.find(' 有価証券報告書') >0:
                # Is the date within the range?
                if date['from'] <= updated and updated <= date['to']:
                    print(securities_code, company_name, title, '...', 'OK')
                    # Unzip
                    with urllib.request.urlopen(url) as res:
                        ZipFile(io.BytesIO(res.read())).extractall(out_folder + '/' + edinet_code)

        # APIの負荷があるので、Sleepの時間は、短くしないで下さい
        time.sleep(10)

    except urllib.error.HTTPError as err:
        if err.code == 404:
            print(securities_code, company_name, '...', 'NG')
            continue

t.append(time.strftime("%Y/%m/%d %H:%M:%S", time.strptime(time.ctime())))
print('Congrats!', ', '.join(t))