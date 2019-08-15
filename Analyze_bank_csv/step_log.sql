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

-- テーブル削除
DROP TABLE bankdata_dailydata;
DELETE FROM bankdata_dailydata;

-- 確認
SELECT ymd, bank_name, SUM(amount) FROM bankdata_dailydata GROUP BY ymd, bank_name;
-- グループ集計
SELECT COUNT(1) FROM bankdata_dailydata;
