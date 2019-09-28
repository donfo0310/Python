-- DjangoでDBを消去して再migrationする
-- https://qiita.com/riz666/items/59352c336398e0321fc2

-- MySQL チートシート http://shiningcureseven.hatenablog.com/entry/2018/08/03/122221
vscode> mysql --local_infile=1 -u root -p
mysql> use pythondb;
-- Notation
-- 1. id列の全行に0を入れるとautoincrementが働く
-- 2. pub_date の yyyy-mm-dd hh:mm:ss データをCSVインポートしようとすると桁が足りない？とかいう
-- 3. mysqlの%表記をdjangoが勘違いしてDATE_FORMATが使えない

--dump
vscode> mysqldump -u root -p -t pythondb --default-character-set=binary vietnam_research_industry > industry.dump;

-- ●industry
-- 確認
SELECT pub_date, COUNT(pub_date) AS CNT FROM vietnam_research_industry GROUP BY pub_date;
SELECT DATE(pub_date) AS pub_date, industry1, SUM(trade_price_of_a_day) FROM vietnam_research_industry GROUP BY pub_date, industry1;
-- グループ集計
SELECT pub_date, COUNT(1) FROM vietnam_research_industry GROUP BY pub_date;
SELECT industry1, COUNT(1) FROM vietnam_research_industry GROUP BY industry1;
SELECT industry1, pub_date, COUNT(1) FROM vietnam_research_industry GROUP BY industry1, pub_date;
SELECT industry1, SUM(marketcap) FROM vietnam_research_industry GROUP BY industry1;

-- ●IndClass マスタ
-- 確認
SELECT
      CONCAT(c.industry_class, '|', i.industry1) AS ind_name
    , ROUND(COUNT(i.industry1),2) AS cnt_per
    , ROUND(SUM(i.marketcap),2) AS cap_per
FROM pythondb.vietnam_research_industry i
INNER JOIN vietnam_research_indclass c ON i.industry1 = c.industry1
WHERE DATE(pub_date) = (
    SELECT
        DATE(MAX(pub_date)) pub_date
    FROM pythondb.vietnam_research_industry
    )
GROUP BY i.industry1, c.industry_class
ORDER BY ind_name;

-- 業種別TOP5
-- 確認
SELECT * FROM vietnam_research_dailytop5;
-- 業種別シンボル別集計（今回は 平均 and 集計後per >1 とする）
SELECT
      c.industry_class || '|' || i.industry1 AS ind_name
    , i.symbol
    , AVG(i.closing_price * volume) AS marketcap
    , AVG(i.per) AS per
FROM vietnam_research_industry i INNER JOIN vietnam_research_indclass c
ON i.industry1 = c.industry1
GROUP BY ind_name, i.symbol
HAVING per >1;

-- ●vnindex
SELECT COUNT(1) FROM vietnam_research_vnindex;
-- pivotはsqliteにはないのでpandasでやってください
SELECT Y, M, closing_price FROM vietnam_research_vnindex;

-- ●watchlist
SELECT * FROM vietnam_research_watchlist;

-- 確認
-- 本日データの明細数と時価総額合計
SELECT
      COUNT(1) AS today_detail_cnt
    , SUM(i.marketcap) AS today_marketcap_sum
FROM pythondb.vietnam_research_industry i INNER JOIN vietnam_research_indclass c ON i.industry1 = c.industry1
WHERE DATE(pub_date) = (SELECT DATE(MAX(pub_date)) pub_date FROM pythondb.vietnam_research_industry);
