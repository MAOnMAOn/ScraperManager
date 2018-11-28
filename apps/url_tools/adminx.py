# import xadmin
#
# from .models import KeyWords, ExcelLink, UrlManager
# from scraper.models import BaseSpider
# from utils.post_excel import PostExcel
#
#
# class KeyWordsAdmin(object):
#     list_display = ["scraper", "crawl_key", "desc"]
#     list_filter = ["scraper", "crawl_key", "add_time"]
#     search_fields = ["scraper", "crawl_key", "add_time"]
#     import_excel = True
#     show_bookmarks = False
#
#     model_icon = 'fa fa-key'
#
#     def post(self, request, *args, **kwargs):
#         rp = super(KeyWordsAdmin, self).post(request, args, kwargs)
#
#         if 'excel' in request.FILES:
#             keywords_upload = KeyWords()
#             keywords_upload.user = request.user
#             keywords_upload.file_name = request.FILES['excel'].name
#
#             excel = PostExcel(path=request.FILES['excel'].file)
#             excel.rename_columns(keywords_upload)
#             excel.rename_foreignkey('scraper')
#             excel.save_model(model_object=KeyWords, foreign_object=BaseSpider, foreign_key='scraper')
#             keywords_upload.upload_type = "user"
#         return rp
#
#
# class ExcelLinkAdmin(object):
#     list_display = ["scraper", "crawl_url", "desc"]
#     list_filter = ["scraper", "crawl_url", "add_time"]
#     search_fields = ["scraper", "crawl_url", "add_time"]
#     show_bookmarks = False
#     import_excel = True
#
#     model_icon = 'fa fa-link'
#
#     def post(self, request, *args, **kwargs):
#         rp = super(ExcelLinkAdmin, self).post(request, args, kwargs)
#
#         if 'excel' in request.FILES:
#             link_upload = ExcelLink()
#             link_upload.user = request.user
#             link_upload.file_name = request.FILES['excel'].name
#
#             excel = PostExcel(path=request.FILES['excel'].file)
#             excel.rename_columns(link_upload)
#             excel.rename_foreignkey('scraper')
#             excel.save_model(model_object=ExcelLink, foreign_object=BaseSpider, foreign_key='scraper')
#             link_upload.upload_type = "user"
#         return rp
#
#
# class UrlManagerAdmin(object):
#     list_display = ["name", "keywords", "max_page", "url_params", "is_add_timestamp", "check_cycle",
#                     "lower_threshold", "upper_threshold"]
#     list_filter = ["name", "keywords", "max_page", "is_add_timestamp"]
#     search_fields = ["name", "keywords", "max_page", "url_params", "is_add_timestamp"]
#     show_bookmarks = False
#     model_icon = 'fa fa-anchor'
#
#
# xadmin.site.register(KeyWords, KeyWordsAdmin)
# xadmin.site.register(ExcelLink, ExcelLinkAdmin)
# xadmin.site.register(UrlManager, UrlManagerAdmin)


"""

"""
