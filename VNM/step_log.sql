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

-- ●industry
-- 確認
SELECT * FROM vietnam_research_industry LIMIT 30;
-- グループ集計
SELECT pub_date, COUNT(1) FROM vietnam_research_industry GROUP BY pub_date;
SELECT industry1, COUNT(1) FROM vietnam_research_industry GROUP BY industry1;
SELECT industry1, pub_date, COUNT(1) FROM vietnam_research_industry GROUP BY industry1, pub_date;
SELECT industry1, SUM(marketcap), SUM(marketcap_per) FROM vietnam_research_industry GROUP BY industry1;

-- ●Industryclassification マスタ
-- 確認
SELECT
      c.industry_class || '|' || i.industry1 AS ind_name
    , ROUND(SUM(count_per),2) AS cnt_per
    , ROUND(SUM(marketcap_per),2) AS cap_per
FROM vietnam_research_industry i INNER JOIN vietnam_research_industryclassification c
ON i.industry1 = c.industry1
GROUP BY i.industry1, c.industry_class
ORDER BY ind_name;

-- ●vnindex
SELECT COUNT(1) FROM vietnam_research_vnindex;
-- pivotはsqliteにはないのでpandasでやってください
SELECT Y, M, closing_price FROM vietnam_research_vnindex;
