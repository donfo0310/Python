# 投資するための財務分析step1「財務情報XBRLを取得する」
# https://qiita.com/NaoyaOura/items/4f613525063d0c8d6653

# RでXBRLデータを取得してみた
# http://horihorio.hatenablog.com/entry/2014/12/15/235107

# STEP1:
# 直近月末の東証上場銘柄一覧上場企業のコード一覧EXCELを取得し、
# "[下記の略称名].txt"のタブ区切りで保存
# https://www.jpx.co.jp/markets/statistics-equities/misc/01.html/

# SIC ... Standard Industrial Classification

import pyodbc
import pandas as pd

cifs = pd.read_csv(r"master\TSE1.csv")