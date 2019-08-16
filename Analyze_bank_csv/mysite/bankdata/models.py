from django.db import models

# クラス名がテーブル名です
class DailyData(models.Model):
    '''日次データ'''
    ymd = models.DateField()
    bank_name = models.CharField(max_length=10)
    description = models.CharField(max_length=200)
    amount = models.IntegerField(default=0)

class Category(models.Model):
    '''descriptionをカテゴリーに置き換えてpivotしやすくします'''
    description = models.CharField(max_length=200)
    category1 = models.CharField(max_length=100)
    