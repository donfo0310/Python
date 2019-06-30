# 投資するための財務分析step1「財務情報XBRLを取得する」
# https://qiita.com/NaoyaOura/items/4f613525063d0c8d6653

# RでXBRLデータを取得してみた
# http://horihorio.hatenablog.com/entry/2014/12/15/235107

# SIC ... Standard Industrial Classification 産業分類コード

import pyodbc
import pandas as pd
import os

# 市場第一部 （内国株）:TSE1
# 市場第二部:TSE2
# マザーズ （内国株）:Mothers
# JASDAQ(グロース）:JQG
# JASDAQ（スタンダード）: JQS

# 実行フォルダ配下、master ディレクトリのcsvをすべて取得し、指定の列名のみをUnionAllする
files = os.listdir('./master')
df = pd.DataFrame()
col_order = ['日付','コード','銘柄名','市場・商品区分','33業種コード']
for f in files:
    # CSV Only!!
    if(f[-4:] == '.csv'):
        # CSV Open and union
        lines = pd.read_csv(r'./master/' + f)[col_order]
        df = pd.concat([df, lines.head()], axis=0, sort=True)

out_folder = os.path.dirname(r'./data/')
if not os.path.exists(out_folder):
    os.makedirs(out_folder)

# API - SampleXML
# http://resource.ufocatch.com/atom/edinetx/query/1301
url = "http://resource.ufocatch.com/atom/edinetx" # API-URI
date = {'from':'2019/6/1', 'to':'2019/6/30'}

# Get XBRL
import time
import urllib
import xml.etree.ElementTree as ET
for sic in df['コード'].astype('str')[:1]:

    # 10Sec.
    # time.sleep(10)

    # Send Request
    req = urllib.request.Request(url + '/query/' + sic)
    with urllib.request.urlopen(req) as res:
        root = ET.fromstring(res.read())

    # print(root.findall(".//entry").text)
    for child in root:
        print(child.tag, child.text)

    for entry in root.iter(tag='id'):
        print('xxx', entry.text)