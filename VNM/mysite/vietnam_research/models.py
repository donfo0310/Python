"""このファイル内に、必要なテーブルがすべて定義されます"""
from django.db import models

class Industry(models.Model):
    """
    viet-kabuで取得できる業種つき個社情報
    closing_price: 終値（千ドン）
    volume: 出来高（株）
    trade_price_of_a_day: 売買代金（千ドン）
    marketcap: 時価総額（億円）
    """
    market_code = models.CharField(max_length=4)
    symbol = models.CharField(max_length=10)
    company_name = models.CharField(max_length=50)
    industry1 = models.CharField(max_length=10)
    industry2 = models.CharField(max_length=20)
    count_per = models.FloatField(default=0.00)
    closing_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    volume = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    trade_price_of_a_day = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    marketcap = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    marketcap_per = models.FloatField(default=0.0)
    per = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pub_date = models.DateTimeField('date published')

class IndustryClassification(models.Model):
    """
    viet-kabuの産業名を産業区分1-3に
    """
    industry1 = models.CharField(max_length=10)
    industry_class = models.IntegerField()

class VnIndex(models.Model):
    """
    データ元:
    https://jp.investing.com/indices/vn-historical-data
    """
    Y = models.CharField(max_length=4)
    M = models.CharField(max_length=2)
    closing_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pub_date = models.DateTimeField('date published')

class WatchList(models.Model):
    """ウォッチリスト"""
    symbol = models.CharField(max_length=10, primary_key=True)
    already_has = models.BooleanField(blank=True, null=True, default=False)
    bought_day = models.DateTimeField(blank=True, null=True)
    stocks_price = models.PositiveIntegerField(blank=True, null=True, default=0)
    stocks_count = models.IntegerField(blank=True, null=True, default=0)
    bikou = models.TextField(blank=True, null=True)

class DailyTop5(models.Model):
    """日次Top5"""
    ind_name = models.CharField(max_length=10)
    market_code = models.CharField(max_length=4)
    symbol = models.CharField(max_length=10)
    trade_price_of_a_day = models.FloatField(default=0.00)
    per = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class BasicInformation(models.Model):
    """基本情報"""
    item = models.TextField()
    description = models.TextField(blank=True, null=True)
