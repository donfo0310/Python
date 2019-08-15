from django.db import models

# クラス名がテーブル名です
class DailyData(models.Model):
    # ここに定義したものがフィールド項目です
    ymd = models.DateField()
    bank_name = models.CharField(max_length=10)
    description = models.CharField(max_length=200)
    amount = models.IntegerField(default=0)
