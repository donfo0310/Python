-- SQLite3 チートシート https://qiita.com/sotetsuk/items/cd2aeae4ba7e72faad47
-- 設定を表示する
sqlite> .show
-- テーブル一覧を表示する
sqlite> .table
sqlite> .schema vietnam_research_industry

-- Djangoでテーブルを作成するとidが勝手につくため、idがないcsvデータではSQLiteでimportできない
-- そこでいったん「temp_import_industry」という一時テーブルを作り、そこからinsertを発行する

-- VNM\mysite> sqlite3 db.sqlite3
sqlite> delete from vietnam_research_industry;

-- SQLite3でのCSVファイルのインポート https://qiita.com/Kunikata/items/61b5ee2c6a715f610493
sqlite> .mode csv
sqlite> .import ../data/industry.csv temp_import_industry

-- tempテーブルからデータを作る（ヘッダーと最終行の空行がちゃんと抜けてたのはテーブル定義のおかげ？）
insert into vietnam_research_industry (market_code, symbol, company_name, industry1, industry2, marketcap, pub_date)
select Market_code, Symbol, Company_name, industry1, industry2, marketcap, strftime('%Y-%m-%d', CURRENT_DATE)
from temp_import_industry;

-- 一時テーブル削除
drop table temp_import_industry;

-- 確認
sqlite> select * from vietnam_research_industry;

-- グループ集計
sqlite> select industry1, COUNT(1) from vietnam_research_industry group by industry1;
sqlite> select industry1, SUM(marketcap) from vietnam_research_industry group by industry1;