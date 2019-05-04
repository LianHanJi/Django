from django.urls import path
from apps.cart.views import CartAddView, CartInfoView, CartUpdateView, CartDeleteView


app_name = 'cart'

urlpatterns = [
    path('add', CartAddView.as_view(), name='add'), # 购物车地址添加
    path('', CartInfoView.as_view(), name='show'), # 购物车页面显示
    path('update', CartUpdateView.as_view(), name='update'), # 购物车记录的更新
    path('delete', CartDeleteView.as_view(), name='delete'), # 购物车记录的删除

]