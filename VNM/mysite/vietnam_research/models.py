"""このファイル内に、必要なテーブルがすべて定義されます"""
from django.db import models

class Industry(models.Model):
    """ここに定義したものがフィールド項目です"""
    market_code = models.CharField(max_length=4)
    symbol = models.CharField(max_length=10)
    company_name = models.CharField(max_length=50)
    industry1 = models.CharField(max_length=10)
    industry2 = models.CharField(max_length=20)
    count_per = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    marketcap = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    marketcap_per = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)
    pub_date = models.DateTimeField('date published')
