-- DjangoでDBを消去して再migrationする
-- https://qiita.com/riz666/items/59352c336398e0321fc2

-- SQLite3 チートシート https://qiita.com/sotetsuk/items/cd2aeae4ba7e72faad47
-- 設定を表示する（ .separator で区切り文字を変更）
.show
.separator ,

-- テーブル一覧を表示する
.table
.schema vietnam_research_industry

-- SQLite3を実行する位置
VNM> sqlite3 mysite/db.sqlite3
VNM/mysite> sqlite3 db.sqlite3

-- Djangoでテーブルを作成するとidが勝手につくため、idがないcsvデータではSQLiteでimportできない
-- そこでいったん「temp_import_industry」という一時テーブルを作り、そこからinsertを発行する
DELETE FROM vietnam_research_industry;

DELETE FROM vietnam_research_industry WHERE strftime('%Y%m', pub_date) = strftime('%Y%m', 'now');

-- SQLite3でのCSVファイルのインポート https://qiita.com/Kunikata/items/61b5ee2c6a715f610493
.mode csv
.import ../data/industry.csv temp_import_industry

-- 一時テーブル削除
DROP TABLE temp_import_industry;

-- 確認
SELECT * FROM vietnam_research_industry LIMIT 30;

-- グループ集計
SELECT COUNT(1) FROM vietnam_research_industry;
SELECT industry1, COUNT(1) FROM vietnam_research_industry GROUP BY industry1;
SELECT industry1, SUM(marketcap), SUM(marketcap_per) FROM vietnam_research_industry GROUP BY industry1;

-- Industryclassification マスタ
INSERT INTO vietnam_research_industryclassification VALUES (1, '農林水産業', 1);
INSERT INTO vietnam_research_industryclassification VALUES (2, '建設業', 2);
INSERT INTO vietnam_research_industryclassification VALUES (3, '製造業', 2);
INSERT INTO vietnam_research_industryclassification VALUES (4, '鉱業', 2);
INSERT INTO vietnam_research_industryclassification VALUES (5, 'サービス業', 3);
INSERT INTO vietnam_research_industryclassification VALUES (6, '不動産業', 3);
INSERT INTO vietnam_research_industryclassification VALUES (7, '商業', 3);
INSERT INTO vietnam_research_industryclassification VALUES (8, '情報通信業', 3);
INSERT INTO vietnam_research_industryclassification VALUES (9, '運輸・物流業', 3);
INSERT INTO vietnam_research_industryclassification VALUES (10, '金融業', 3);
INSERT INTO vietnam_research_industryclassification VALUES (11, '電気・ガス業', 3);
-- 確認
SELECT
      c.industry_class || '|' || i.industry1 AS ind_name
    , ROUND(SUM(count_per),2) AS cnt_per
    , ROUND(SUM(marketcap_per),2) AS cap_per
FROM vietnam_research_industry i INNER JOIN vietnam_research_industryclassification c
ON i.industry1 = c.industry1
GROUP BY i.industry1, c.industry_class
ORDER BY ind_name;