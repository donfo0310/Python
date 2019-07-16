from django.urls import path

# STEP1: 現在のフォルダの「views.py」を import する！さっき編集したやつ！
from . import views

# STEP2: views.py には「index」という関数を作りましたね！それを呼んでます
urlpatterns = [
    path('', views.index, name='index'),
]