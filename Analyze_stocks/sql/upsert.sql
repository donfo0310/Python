USE [db]

MERGE INTO stock_trade_data AS A
USING (
      SELECT 
              '{0}' AS Code
            , '{1}' AS CompanyName
            , '{2}' AS Market
            , '{3}' AS Industry
            , '{4}' AS TradeDate
            , '{5}' AS Price
            , '{6}' AS Change
            , '{7}' AS ChangeInPercent
            , '{8}' AS PreviousClosePx
            , '{9}' AS Opening
            , '{10}' AS High
            , '{11}' AS Low
            , '{12}' AS Volume
            , '{13}' AS TradingVolume
            , '{14}' AS MarketCap
            , '{15}' AS LowerRange
            , '{16}' AS UpperRange
            , GETDATE() AS created_at
            , GETDATE() AS updated_at
            ) AS B
ON (A.Code = B.Code AND A.TradeDate = B.TradeDate)
WHEN MATCHED THEN
      UPDATE SET 
              A.CompanyName = B.CompanyName
            , A.Market = B.Market
            , A.Industry = B.Industry
            , A.Price = B.Price
            , A.Change = B.Change
            , A.ChangeInPercent = B.ChangeInPercent
            , A.PreviousClosePx = B.PreviousClosePx
            , A.Opening = B.Opening
            , A.High = B.High
            , A.Low = B.Low
            , A.Volume = B.Volume
            , A.TradingVolume = B.TradingVolume
            , A.MarketCap = B.MarketCap
            , A.LowerRange = B.LowerRange
            , A.UpperRange = B.UpperRange
            , A.updated_at = B.updated_at
WHEN NOT MATCHED THEN
      INSERT (
              Code, CompanyName, Market, Industry
            , TradeDate, Price, Change, ChangeInPercent
            , PreviousClosePx, Opening, High, Low
            , Volume, TradingVolume, MarketCap, LowerRange
            , UpperRange, created_at, updated_at) 
      VALUES (
              B.Code, B.CompanyName, B.Market, B.Industry
            , B.TradeDate, B.Price, B.Change, B.ChangeInPercent
            , B.PreviousClosePx, B.Opening, B.High, B.Low
            , B.Volume, B.TradingVolume, B.MarketCap, B.LowerRange
            , B.UpperRange, B.created_at, B.updated_at) ;