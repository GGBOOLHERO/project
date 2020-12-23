from django.urls import path
from buyer import views

urlpatterns = [
    path('index/', views.index),
    # path('more_goods_list/', views.more_goods_list),
    path('goods_detail/', views.goods_detail),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('add_cart/', views.add_cart),
    path('my_goodscar/', views.my_goodscar),
    path('change_goodscar_num/', views.change_goodscar_num),
    path('minus_goodscar_num/', views.minus_goodscar_num),
    path('delete_car/', views.delete_car),
    path('add_orders/', views.place_order),
    path('usercenter/', views.usercenter),
    path('add_address/', views.add_address),
    path('edit_address/', views.edit_address),
    path('delete_address/', views.delete_address),
    path('change_address_status/', views.change_address_status),
    path('my_orders/', views.my_orders),
    path('now_buy/', views.now_buy),
    path('register_email_ajax/', views.register_email_ajax),
    path('register_email/', views.register_email),
    path('cache_test/', views.cache_test)
]