"""ScraperManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import xadmin
from django.conf import settings
from django.views.generic import TemplateView
from django.views.static import serve
from django.conf.urls import url, include

from users.views import IndexView


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$', IndexView.as_view(), name="index"),

    #  用户users相关url设置
    url(r'^', include('users.urls')),
    url(r'deployment/', include('deployment.urls', namespace="deployment")),
    url(r'monitor/', include('monitor.urls', namespace="monitor")),
    url(r'tasks/', include('tasks.urls', namespace="tasks")),
    # media 的url配置， 图片上传的url路径, 开发和测试环境使用
    url(r'^media/(?P<path>.*)/$', serve, {"document_root": settings.MEDIA_ROOT}),
    # 富文本相关url
    # url(r'^ueditor/', include('DjangoUeditor.urls')),
]


# 全局404页面配置
handler404 = 'users.views.page_not_found'

handler500 = 'users.views.page_error'
