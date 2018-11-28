# import xadmin
#
# from .models import Project, BaseSpider, SpiderInstance, ECommerce
#
#
# class ScraperProjectAdmin(object):
#     list_display = ["name", "desc", "add_time"]
#     list_filter = ["name", "desc", "add_time"]
#     model_icon = 'fa fa-product-hunt'
#     show_bookmarks = False
#
#
# class BaseSpiderAdmin(object):
#     list_display = ["name", "website", "project", "desc", "add_time"]
#     list_filter = ["name", "project", "website"]
#     search_fields = ["name", "website", "project", "add_time"]
#     model_icon = 'fa fa-bug'  # fa-address-book
#     show_bookmarks = False
#
#
# class SpiderModelAdmin(object):
#     list_display = ["spider", "keyword", "version", "supplement", "detail_url"]
#     list_filter = ["spider", "keyword", "version"]
#     search_fields = ["spider", "keyword", "website", "version"]
#     model_icon = 'fa  fa-diamond'
#     show_bookmarks = False
#
#
# class ECommerceAdmin(SpiderModelAdmin):
#     pass
#
#
# xadmin.site.register(Project, ScraperProjectAdmin)
# xadmin.site.register(BaseSpider, BaseSpiderAdmin)
# xadmin.site.register(SpiderInstance, SpiderModelAdmin)
# xadmin.site.register(ECommerce, ECommerceAdmin)

