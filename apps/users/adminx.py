import xadmin
from xadmin import views


class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "数亮科技爬虫管理后台"
    site_footer = "ScraperManager"
    menu_style = "accordion"


xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobalSettings)

