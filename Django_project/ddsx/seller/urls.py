from django.urls import path
from seller import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('index/', views.index),
    path('logout/', views.logout),
    path('store/', views.store),
    path('goodstype_list/', views.goodstype_list),
    path('add_goodstype/', views.add_goodstype),
    path('edit_goodstype/', views.edit_goodstype),
    path('delete_goodstype/', views.delete_goodstype),
    path('add_goods/', views.add_goods),
    path('goods_list/', views.goods_list),
]