from django.contrib import admin
from django.core.cache import cache
from apps.goods.models import GoodsType, IndexPromotionBanner,IndexTypeGoodsBanner, IndexGoodsBanner
# Register your models here.


class BaseModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        '''更新表中数据时调用'''
        super().save_model(request, obj, form, change)
        # 发出任务
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()
        # 清楚缓存
        cache.delete('index_page_data')

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        # 发出任务
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()
        # 清除缓存
        cache.delete('index_page_data')

class GoodsTypeAdmin(BaseModelAdmin):
    pass


class IndexGoodsBannerAdmin(BaseModelAdmin):
    pass


class IndexTypeGoodsBannerAdmin(BaseModelAdmin):
    pass


class IndexPromotionBannerAdmin(BaseModelAdmin):
    pass



admin.site.register(GoodsType, GoodsTypeAdmin)
admin.site.register(IndexGoodsBanner, IndexGoodsBannerAdmin)
admin.site.register(IndexTypeGoodsBanner, IndexTypeGoodsBannerAdmin)
admin.site.register(IndexPromotionBanner, IndexPromotionBannerAdmin)