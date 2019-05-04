# 使用celery
# from django_redis import get_redis_connection
from django.core.mail import send_mail
from django.conf import settings
from celery import Celery
from django.template import loader, RequestContext
from django.shortcuts import render

# 初始化django的环境
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
django.setup()

from apps.goods.models import GoodsType, IndexPromotionBanner, IndexGoodsBanner, IndexTypeGoodsBanner

# 创建一个celery对象
app = Celery('celery_task.tasks', broker='redis://192.168.86.1:6379/8')


# 定义任务函数
@app.task
def send_register_active_mail(to_mail, username, token):
    # 发邮件
    subject = '天天生鲜欢迎信息'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_mail]
    html_message = '<h1>%s,欢迎您成为天天生鲜的注册会员</h1>请点击下面链接激活你的账号:<br/><a herf="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (
    username, token, token)
    send_mail(subject, message, sender, receiver, html_message=html_message)


@app.task
def generate_static_index_html():
    '''产生首页静态页面'''
    # 获取商品的种类信息
    types = GoodsType.objects.all()

    # 获取首页商品轮播信息
    goods_banners = IndexGoodsBanner.objects.all().order_by('index')

    # 获取首页促销活动信息
    promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

    # 获取首页分类商品展示信息
    # type_goods_banners = IndexTypeGoodsBanner.objects.all()
    for type in types:
        # 获取type种类首页分类商品的图片展示信息
        image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by(
            'sku__indextypegoodsbanner')
        # 获取type种类首页分类商品的文字展示信息
        title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by(
            'sku__indextypegoodsbanner')
        # 动态给type增加属性，分别保存首页分类商品的图片展示信息和文字展示信息
        type.image_banners = image_banners
        type.title_banners = title_banners

    # 组织模板上下文
    context = {'types': types,
               'goods_banners': goods_banners,
               'promotion_banners': promotion_banners}

    # 使用模板
    # 1.加载模板文件
    temp = loader.get_template('static_index.html')
    # (2.定义模板上下文)
    # context = RequestContext(request, context)
    # 3.模板渲染
    static_index_html = temp.render(context)

    # 生成首页对应静态页面文件
    save_path = os.path.join(settings.BASE_DIR, 'static/index.html')
    with open(save_path, 'w') as f:
        f.write(static_index_html)






























