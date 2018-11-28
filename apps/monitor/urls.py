from django.conf.urls import url


from .views import (ServerIndexView, ServerStatusView, ServerCreateView, ServerUpdateView, ServerRemoveView,
                    ServerTopInfoView, ServerCpuView, ServerMemView, DatabaseIndexView, DatabaseStatusView,
                    DatabaseClientCreateView, DatabaseClientUpdateView, DatabaseClientRemoveView,
                    DatabaseDBListView, DBTableListView, ServerPingStatusView)


urlpatterns = [
    url(r'^server/index/$', ServerIndexView.as_view(), name="server_index"),
    url(r'^server/ping/status/$', ServerPingStatusView.as_view(), name="server_ping_status"),
    url(r'^server/(\d+)/status/$', ServerStatusView.as_view(), name="server_status"),
    url(r'^server/create/$', ServerCreateView.as_view(), name="server_create"),
    url(r'^server/(\d+)/update/$', ServerUpdateView.as_view(), name="server_update"),
    url(r'^server/(\d+)/remove/$', ServerRemoveView.as_view(), name="server_remove"),
    url(r'^server/(\d+)/info/$', ServerTopInfoView.as_view(), name="server_info"),
    url(r'^server/(\d+)/cpu/$', ServerCpuView.as_view(), name="server_cpu"),
    url(r'^server/(\d+)/mem/$', ServerMemView.as_view(), name="server_mem"),
    url(r'^database/index/$', DatabaseIndexView.as_view(), name="database_index"),
    url(r'^database/create/$', DatabaseClientCreateView.as_view(), name="database_create"),
    url(r'^database/(\d+)/status/$', DatabaseStatusView.as_view(), name="database_status"),
    url(r'^database/(\d+)/update/$', DatabaseClientUpdateView.as_view(), name="database_update"),
    url(r'^database/(\d+)/remove/$', DatabaseClientRemoveView.as_view(), name="database_remove"),
    url(r'^database/(\d+)/db_type/(\d+)/db_list/$', DatabaseDBListView.as_view(), name="database_db_list"),
    url(r'^database/(\d+)/db_type/(\d+)/db/(\S+)/table/(\S+)/$', DBTableListView.as_view(), name="database_table"),
]
