"""このファイル内に、必要なテーブルがすべて定義されます"""
from django.db import models

class Industry(models.Model):
    """viet-kabuで取得できる業種つき個社情報"""
    market_code = models.CharField(max_length=4)
    symbol = models.CharField(max_length=10)
    company_name = models.CharField(max_length=50)
    industry1 = models.CharField(max_length=10)
    industry2 = models.CharField(max_length=20)
    count_per = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    marketcap = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    marketcap_per = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)
    pub_date = models.DateTimeField('date published')

class IndustryClassification(models.Model):
    """viet-kabuの産業名を産業区分1-3に"""
    industry1 = models.CharField(max_length=10)
    industry_class = models.IntegerField()

class VnIndex(models.Model):
    """https://jp.investing.com/indices/vn-historical-data"""
    Y = models.CharField(max_length=4)
    M = models.CharField(max_length=2)
    closing_price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    pub_date = models.DateTimeField('date published')