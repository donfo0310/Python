-- DjangoでDBを消去して再migrationする
-- https://qiita.com/riz666/items/59352c336398e0321fc2

-- SQLite3 チートシート https://qiita.com/sotetsuk/items/cd2aeae4ba7e72faad47
-- 設定を表示する
.show
-- テーブル一覧を表示する
.table
.schema vietnam_research_industry

-- SQLite3を実行する位置
VNM> sqlite3 mysite/db.sqlite3
VNM/mysite> sqlite3 db.sqlite3

-- Djangoでテーブルを作成するとidが勝手につくため、idがないcsvデータではSQLiteでimportできない
-- そこでいったん「temp_import_industry」という一時テーブルを作り、そこからinsertを発行する
delete from vietnam_research_industry;

delete from vietnam_research_industry where strftime('%Y%m', pub_date) = strftime('%Y%m', 'now');

-- SQLite3でのCSVファイルのインポート https://qiita.com/Kunikata/items/61b5ee2c6a715f610493
.mode csv
.import ../data/industry.csv temp_import_industry

-- 一時テーブル削除
drop table temp_import_industry;

-- 確認
select * from vietnam_research_industry limit 30;

-- グループ集計
select COUNT(1) from vietnam_research_industry;
select industry1, COUNT(1) from vietnam_research_industry group by industry1;
select industry1, SUM(marketcap), SUM(marketcap_per) from vietnam_research_industry group by industry1;