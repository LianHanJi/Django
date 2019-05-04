from django.urls import path
# from django.contrib.auth.decorators import login_required
from apps.user.views import RegisterView, ActiceView, LoginView, UserInfoView, UserOrderView, AddressView, LogoutView

app_name = 'user'
urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),#注册
    path('active/<token>', ActiceView.as_view(), name='active'),#用户激活
    path('login', LoginView.as_view(), name='login'),#登陆

    # path('', login_required(UserInfoView.as_view()), name='user'),
    # path('order', login_required(UserOrderView.as_view()), name='order'),
    # path('address', login_required(AddressView.as_view()), name='address'),
    path('', UserInfoView.as_view(), name='user'),
    path('order/<page>', UserOrderView.as_view(), name='order'),
    path('address', AddressView.as_view(), name='address'),
    path('logout', LogoutView.as_view(), name='logout'),
]

# login_required只能装饰视图函数，不能装饰视图类和类中的函数，可在url页面对as_view函数使用(另一种方法用装饰器)
