-- DjangoでDBを消去して再migrationする
-- https://qiita.com/riz666/items/59352c336398e0321fc2

-- SQLite3 チートシート https://qiita.com/sotetsuk/items/cd2aeae4ba7e72faad47
-- 設定を表示する（ .separator で区切り文字を変更）
.show
.separator ,

-- テーブル一覧を表示する
.table
.schema bankdata_dailydata

-- SQLite3を実行する位置
Analyze_bank_csv> sqlite3 mysite/db.sqlite3
Analyze_bank_csv/mysite> sqlite3 db.sqlite3

-- ●Dailydata
-- 確認
SELECT COUNT(1) FROM bankdata_dailydata;
SELECT * FROM bankdata_dailydata;
SELECT description, SUM(amount) FROM bankdata_dailydata GROUP BY description;
SELECT ymd, description, amount FROM bankdata_dailydata WHERE description = '口座振替４ オリコ';
-- テーブル削除
DROP TABLE bankdata_dailydata;
-- データ削除
DELETE FROM bankdata_dailydata;

-- ●Categoryテーブル
-- 確認
SELECT description, category1, category2 FROM bankdata_category GROUP BY description;

-- ●組み合わせ
-- 確認
SELECT 
      SUBSTR(REPLACE(d.ymd, '-', ''), 1, 6) ym
    , c.category1
    , c.category2
    , SUM(d.amount) amount
FROM bankdata_dailydata d INNER JOIN bankdata_category c ON d.description = c.description 
GROUP BY SUBSTR(REPLACE(d.ymd, '-', ''), 1, 6), c.category1, c.category2
ORDER BY date(d.ymd), c.category1, c.category2;

