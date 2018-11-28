import xadmin

from .models import Server, DatabaseClient


class ServerAdmin(object):
    list_display = ["name", "ip", "port", "ssh_user", "ssh_key_path", "created_at"]
    list_filter = ["name", "ip", "port", "ssh_user", "created_at"]
    search_fields = ["name", "ip", "port", "ssh_user", "created_at"]
    model_icon = 'fa fa-server'
    show_bookmarks = False


class DatabaseClientAdmin(object):
    list_display = ["client_name", "ip", "port", "user_name", "client_type", "created_at"]
    list_filter = ["client_name", "ip", "port", "user_name", "client_type", "created_at"]
    search_fields = ["client_name", "ip", "port", "user_name", "client_type", "created_at"]
    model_icon = 'fa fa-database'
    show_bookmarks = False


xadmin.site.register(Server, ServerAdmin)
xadmin.site.register(DatabaseClient, DatabaseClientAdmin)


"""
    client_name = models.CharField(max_length=255, default=None)
    ip = models.CharField(max_length=255, verbose_name="ip地址")
    port = models.IntegerField(verbose_name="端口")
    user_name = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    client_type = models.IntegerField(choices=((1, "mysql"), (2, "mongodb"), (3, "redis")),
                                      default=1, verbose_name="客户端类型")
    desc = models.CharField(max_length=255, blank=True, null=True, verbose_name="说明")
    created_at = models.DateTimeField(default=datetime.now, verbose_name="创建时间")
"""