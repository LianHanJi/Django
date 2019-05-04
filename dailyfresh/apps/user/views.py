from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
from apps.user.models import User, Address
from apps.goods.models import GoodsSKU
from apps.order.models import OrderInfo, OrderGoods
# from celery_tasks.tasks import send_register_active_mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from utils.mixin import LoginRequiredMixin
from django_redis import get_redis_connection
import re
# Create your views here.

# Create your models here.

#/user/register


# def register(request):
#     '''注册'''
#     if request.method == "GET":
#         #显示注册页面
#         return render(request, 'register.html')
#     else:
#         #进行注册页面处理
#         # 接收数据
#         username = request.POST.get('user_name')
#         password = request.POST.get('pwd')
#         email = request.POST.get('email')
#         allow = request.POST.get('allow')
#         # 进行数据校验
#         if not all([username, password, email]):
#             # 数据不完整
#             return render(request, 'register.html', {'errmsg': '数据不完整'})
#
#         # 校验邮箱
#         if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
#             return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
#
#         if allow != 'on':
#             return render(request, 'register.html', {'errmsg': '请同意协议'})
#
#         # 检验用户名
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             # 用户名不存在
#             user = None
#
#         if user:
#             return render(request, 'register.html', {'errmsg': '用户名已经存在'})
#
#         # 进行业务处理：进行用户注册
#         user = User.objects.create_user(username, email, password)
#         user.is_active = 0
#         user.save()
#
#         # 返回应答,跳转到首页
#         return redirect(reverse('goods:index'))


# def register_handle(request):
#     '''进行注册页面处理'''
#     #接收数据
#     username = request.POST.get('user_name')
#     password = request.POST.get('pwd')
#     email = request.POST.get('email')
#     allow = request.POST.get('allow')
#     #进行数据校验
#     if not all ([username, password, email]):
#         #数据不完整
#         return render(request, 'register.html', {'errmsg': '数据不完整'})
#
#     #校验邮箱
#     if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
#         return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
#
#     if allow != 'on':
#         return render(request, 'register.html', {'errmsg': '请同意协议'})
#
#     #检验用户名
#     try:
#         user = User.objects.get(username=username)
#     except User.DoesNotExist:
#         #用户名不存在
#         user = None
#
#     if user:
#         return render(request,'register.html',{'errmsg':'用户名已经存在'})
#     #进行业务处理：进行用户注册
#     # user = User()
#     # user.username = username
#     # user.password = password
#     # user.email = email
#     # user.save()
#     user = User.objects.create_user(username, email, password)
#     user.is_active = 0
#     user.save()
#
#     #返回应答,跳转到首页
#     return redirect(reverse('goods:index'))

# /user/register
class RegisterView(View):
    '''注册'''
    def get(self,request):
        '''显示注册页面'''
        return render(request,'register.html')

    def post(self,request):
        '''进行注册页面处理'''
        # 接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 进行数据校验
        if not all([username, password, email]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})

        # 检验用户名
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None

        if user:
            return render(request, 'register.html', {'errmsg': '用户名已经存在'})
        # 进行业务处理：进行用户注册
        # user = User()
        # user.username = username
        # user.password = password
        # user.email = email
        # user.save()
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        #发送激活邮件，包含激活链接：http://127.0.0.1:8000/user/active/3
        #激活链接中需要包含用户的身份信息,并且把身份信息加密处理

        #加密用户的身份信息，生成激活token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)#bytes
        token = token.decode()
        # #发邮件
        #send_register_active_mail.delay(email, username, token)
        subject = '天天生鲜欢迎信息'
        message = ''
        sender = settings.EMAIL_FROM
        receiver = [email]
        html_message = '<h1>%s,欢迎您成为天天生鲜的注册会员</h1>请点击下面链接激活你的账号:<br/><a herf="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>'%(username, token, token)
        send_mail(subject, message, sender, receiver, html_message=html_message)
        # #send_mail()是阻塞执行的
        # 返回应答,跳转到首页
        return redirect(reverse('goods:index'))


# /user/ActiveView
class ActiceView(View):
    '''用户激活'''
    def get(self,request,token):
        #获取激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            #获取激活用户id
            user_id = info['confirm']
            #根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            #跳转至登陆页面
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            #激活链接已过期
            return HttpResponse('激活链接已过期')


# /user/Login
class LoginView(View):
    '''登陆'''
    def get(self,request):
        '''显示登陆页面'''
        # 判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username= ''
            checked = ''

        # 使用模板
        return render(request, 'login.html', {'username':username, 'checked':checked})

    def post(self,request):
        '''登陆'''
        # 接受数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        # 校验数据
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg':'数据不完整'})

        # 业务处理：登陆校验
        # User.objects.get(username=username, password=password)
        user = authenticate(username=username, password=password)
        if user is not None:
            # 用户名密码正确
            if user.is_active:
                # 用户已激活
                # 记录用户登录状态
                login(request, user)
                # 获取登陆后所需跳转的地址并跳转(无则跳转至首页)
                next_url = request.GET.get('next', reverse('goods:index'))
                # 跳转首页
                response = redirect(next_url)#HttpResponseRedirect

                # 判断是否记住用户名
                remember = request.POST.get("remember")

                if remember == 'on':
                    #记住用户名
                    response.set_cookie('username', username, max_age=7*24*3600)
                else:
                    response.delete_cookie('username')

                # 返回response
                return response
            else:
                # 用户未激活
                return render(request, 'login.html', {'errmsg': '账户未激活'})
        else:
            # 用户名密码有误
            return render(request, 'login.html', {'errmsg': '用户名或者密码错误'})
        # 返回应答


# /user/logout
class LogoutView(View):
    def get(self, request):
        '''登出用户'''
        # 清除用户的session信息
        logout(request)

        return redirect(reverse('goods:index'))


# /user
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        '''个人信息页'''
        # page='user'定义一个激活页面属性的变量
        # request.user
        # 如果用户未登录->AnonymousUser类的一个实例
        # 如果用户登陆_>User类的一个实例
        # request.user.is_authenticated()除了给模板传递指定变量，django框架会把request.user也传入模板文件

        # 获取用户信息
        user = request.user
        address = Address.object.get_default_address(user)
        # 获取用户最近浏览记录
        from redis import StrictRedis
        StrictRedis(host='127.0.0.1', port='6379', db=9)
        con = get_redis_connection("default")

        history_key = 'history_%d' % user.id

        # 获取用户最新浏览商品五条id
        sku_ids = con.lrange(history_key, 0, 4)
        # 从数据库中查询用户浏览的商品具体信息
        # goods_li = GoodsSKU.objects.filter(id__in=sku_ids)# 无排序效果
        # goods_res = []
        # for a_id in sku_ids:
        #     for goods in goods_li:
        #         if a_id ==goods.id:
        #             goods_res.append(goods)

        # 遍历用户浏览的商品信息
        goods_li = []
        for id in sku_ids:
            goods = GoodsSKU.objects.get(id=id)
            goods_li.append(goods)
        #组织上下文
        context = {'page': 'user',
                   'address': address,
                   'goods_li': goods_li}
        return render(request, "user_center_info.html", context)


class UserOrderView(LoginRequiredMixin, View):
    '''个人订单页'''
    def get(self, request, page):
        # 获取用户订单信息
        user = request.user
        orders = OrderGoods.objects.filter(user=user)

        # 遍历获取订单商品的信息
        for order in orders:
            # 根据order_id查询订单商品信息
            order_skus = OrderGoods.objects.filter(order=order.order_id).order_by('-create_time')

            # 遍历order_sku计算小计
            for order_sku in order_skus:
                amount = order_sku.count*order_sku.price
                # 动态给order_sku增加属性，保存小计
                order_sku.amount = amount

            # 动态给order增加属性，保存订单支付状态
            order.atatic_name = OrderInfo.ORDER_STATUS[order.order_status]
            # 动态给order增加属性，保存订单商品信息
            order.order_sku = order_sku

        # 分页
        paginator = Paginator(order, 1)

        # 处理页码
        # 获取page页内容
        try:
            page = int(page)
        except Exception as e:
            page = 1

        if page > paginator.num_pages:
            page = 1

        # 获取第page页的实例对象
        order_page = paginator.page(page)

        # todo: 进行页码的控制，页面上最多显示5页
        # 页数小于5显示所有页
        # 页数大于5，当前页为前3页，显示1-5页
        # 当前页为最后三页时显示最后5页
        # 其次显示前后各两页
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 5, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)

        # 组织上下文
        context = {'order_page': order_page,
                   'pages': pages,
                   'page': 'order'}

        return render(request, "user_center_order.html", context)


class AddressView(LoginRequiredMixin, View):
    def get(self, request):
        '''个人地址页'''
        # page='address'定义一个激活页面属性的变量
        # 获取用户对象
        user = request.user
        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     # 不存在收货地址
        #     address = None
        address = Address.object.get_default_address(user)
        return render(request, "user_center_site.html", {'page': 'address', 'address': address})

    def post(self,request):
        '''地址的添加'''
        # 接受处理
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')
        # 校验数据
        if not all([receiver, addr, phone]):
            return render(request, 'user_center_site.html', {'errmsg': '数据不完整'})

        # 校验手机号
        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
            return render(request, 'user_center_site.html', {'errmsg': '手机格式错误'})
        # 业务处理：地址的添加
        # 如果用户已有默认地址，则添加地址不作为默认地址，否则为默认收货地址
        # 获取用户对应User对象
        user = request.user
        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     # 不存在收货地址
        #     address = None
        address = Address.object.get_default_address(user)

        if address:
            is_default = False
        else:
            is_default = True

        # 添加地址
        Address.objects.create(user=user,
                               receiver=receiver,
                               addr=addr,
                               zip_code=zip_code,
                               phone=phone,
                               is_default=is_default)
        # 返回应答
        return redirect(reverse('user:address')) # get请求方式

























