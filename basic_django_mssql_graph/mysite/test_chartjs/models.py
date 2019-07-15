"""ここにテーブルの構造を書きます"""
from django.db import models

class DjangoTestTable(models.Model):
    """クラス名がテーブル名です"""
    # ここに定義したものがフィールド項目です
    month_code = models.CharField(max_length=3, default='xxx') # Jun Feb など
    sales = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    