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
SELECT industry1, pub_date, COUNT(1) FROM vietnam_research_industry GROUP BY industry1, pub_date;
SELECT industry1, SUM(marketcap), SUM(marketcap_per) FROM vietnam_research_industry GROUP BY industry1;
-- debug（前月に書き直して '消えないか' をチェック） OK
update vietnam_research_industry set pub_date = '2019-07-31' where symbol = 'AAA';
SELECT * FROM vietnam_research_industry WHERE strftime('%Y%m', pub_date) = strftime('%Y%m', 'now');

-- Industryclassification マスタ
INSERT INTO vietnam_research_industryclassification (industry1, industry_class) VALUES ('農林水産業', 1);
INSERT INTO vietnam_research_industryclassification (industry1, industry_class) VALUES ('建設業', 2);
INSERT INTO vietnam_research_industryclassification (industry1, industry_class) VALUES ('製造業', 2);
INSERT INTO vietnam_research_industryclassification (industry1, industry_class) VALUES ('鉱業', 2);
INSERT INTO vietnam_research_industryclassification (industry1, industry_class) VALUES ('サービス業', 3);
INSERT INTO vietnam_research_industryclassification (industry1, industry_class) VALUES ('不動産業', 3);
INSERT INTO vietnam_research_industryclassification (industry1, industry_class) VALUES ('商業', 3);
INSERT INTO vietnam_research_industryclassification (industry1, industry_class) VALUES ('情報通信業', 3);
INSERT INTO vietnam_research_industryclassification (industry1, industry_class) VALUES ('運輸・物流業', 3);
INSERT INTO vietnam_research_industryclassification (industry1, industry_class) VALUES ('金融業', 3);
INSERT INTO vietnam_research_industryclassification (industry1, industry_class) VALUES ('電気・ガス業', 3);
-- 確認
SELECT
      c.industry_class || '|' || i.industry1 AS ind_name
    , ROUND(SUM(count_per),2) AS cnt_per
    , ROUND(SUM(marketcap_per),2) AS cap_per
FROM vietnam_research_industry i INNER JOIN vietnam_research_industryclassification c
ON i.industry1 = c.industry1
GROUP BY i.industry1, c.industry_class
ORDER BY ind_name;

-- vnindex
SELECT COUNT(1) FROM vietnam_research_vnindex;
-- pivotはsqliteにはないのでpandasでやってください
SELECT Y, M, closing_price FROM vietnam_research_vnindex

-- WatchList テーブル
INSERT INTO vietnam_research_watchlist (symbol, already_has, bought_day, stocks_price, stocks_count, bikou) VALUES ('SAB', True, '2019-07-16', 287000, 150, '（@1,435円 x 150株 = 215,250円）');
INSERT INTO vietnam_research_watchlist (symbol, already_has, stocks_price, stocks_count, bikou) VALUES ('GAS', False, 0, 0, '');
INSERT INTO vietnam_research_watchlist (symbol, already_has, stocks_price, stocks_count, bikou) VALUES ('PPC', False, 0, 0, '');
INSERT INTO vietnam_research_watchlist (symbol, already_has, stocks_price, stocks_count, bikou) VALUES ('VNM', False, 0, 0, '');
INSERT INTO vietnam_research_watchlist (symbol, already_has, stocks_price, stocks_count, bikou) VALUES ('VHC', False, 0, 0, '');
INSERT INTO vietnam_research_watchlist (symbol, already_has, bought_day, stocks_price, stocks_count, bikou) VALUES ('PHR', True, '2019-07-19', 65000, 680, '（@325円 x 680株 = 221,000円）');
INSERT INTO vietnam_research_watchlist (symbol, already_has, stocks_price, stocks_count, bikou) VALUES ('FMC', False, 0, 0, '');
INSERT INTO vietnam_research_watchlist (symbol, already_has, stocks_price, stocks_count, bikou) VALUES ('VHM', False, 0, 0, '');
INSERT INTO vietnam_research_watchlist (symbol, already_has, stocks_price, stocks_count, bikou) VALUES ('VRE', False, 0, 0, '');

-- BasicInformation テーブル
INSERT INTO vietnam_research_basicinformation (item, description) VALUES ('国名', 'ベトナム社会主義共和国 Socialist Republic of Viet Nam');
INSERT INTO vietnam_research_basicinformation (item, description) VALUES ('面積', '33万1,690平方キロメートル（2018、出所：外務省）');
INSERT INTO vietnam_research_basicinformation (item, description) VALUES ('人口', '約9,370万人（2018、出所：外務省）');
INSERT INTO vietnam_research_basicinformation (item, description) VALUES ('首都', 'ハノイ');
INSERT INTO vietnam_research_basicinformation (item, description) VALUES ('言語', 'ベトナム語、ほかに少数民族語');
INSERT INTO vietnam_research_basicinformation (item, description) VALUES ('宗教', '仏教（約80％）、そのほかにカトリック、カオダイ教、ホアハオ教など');
INSERT INTO vietnam_research_basicinformation (item, description) VALUES ('公用語', 'ベトナム語');
INSERT INTO vietnam_research_basicinformation (item, description) VALUES ('通貨', 'ドン');
INSERT INTO vietnam_research_basicinformation (item, description) VALUES ('主要産業', '農林水産業，鉱業，工業');
INSERT INTO vietnam_research_basicinformation (item, description) VALUES ('GDP', '約2,235億米ドル（2017年平均 越統計総局より引用）');
INSERT INTO vietnam_research_basicinformation (item, description) VALUES ('経済成長率', '6.81%（2017年平均、越統計総局より引用）');
