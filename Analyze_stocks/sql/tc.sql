CREATE TABLE stock_trade_data (
      Code NVARCHAR(4) NOT NULL
    , CompanyName NVARCHAR(50) NULL
    , Market NVARCHAR(50) NULL
    , Industry NVARCHAR(50) NULL
    , TradeDate datetime NOT NULL
    , Price money NULL
    , Change money NULL
    , ChangeInPercent money NULL
    , PreviousClosePx money NULL
    , Opening money NULL
    , High money NULL
    , Low money NULL
    , Volume money NULL
    , TradingVolume money NULL
    , MarketCap money NULL
    , LowerRange money NULL
    , UpperRange money NULL
    , created_at datetime NULL
    , updated_at datetime NULL
    , PRIMARY KEY (Code, TradeDate)  
);
