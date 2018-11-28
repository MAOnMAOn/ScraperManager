from datetime import datetime

from django.db import models


class Server(models.Model):
    name = models.CharField(max_length=100, verbose_name="服务器名称")
    ip = models.CharField(max_length=255, verbose_name="ip地址")
    port = models.IntegerField(default=22,  verbose_name="端口")
    ssh_user = models.CharField(max_length=100, verbose_name="用户名")
    password = models.CharField(max_length=200, default='', blank=True, null=True, verbose_name="密码")
    ssh_key_path = models.FileField(upload_to='files/ssh_key/%Y/%m', default='', blank=True,
                                    null=True, max_length=200, verbose_name="文件上传")
    # ssh_key_path = models.CharField(default="files/id_rsa", max_length=255)  # 后期实现自定义上传
    desc = models.CharField(max_length=255, blank=True, null=True, verbose_name="说明")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class DatabaseClient(models.Model):
    client_name = models.CharField(max_length=255, default=None, verbose_name="客户端名称")
    ip = models.CharField(max_length=255, verbose_name="ip地址")
    port = models.IntegerField(verbose_name="端口")
    user_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="用户名")
    password = models.CharField(max_length=255, blank=True, null=True, verbose_name="密码")
    client_type = models.IntegerField(choices=((1, "mysql"), (2, "mongodb"), (3, "redis")),
                                      default=1, verbose_name="客户端类型")
    desc = models.CharField(max_length=255, blank=True, null=True, verbose_name="说明")
    created_at = models.DateTimeField(default=datetime.now, verbose_name="创建时间")

    class Meta:
        verbose_name = '数据库客户端'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.client_name


"""
class UploadSSHKeyAdmin(object):
    list_display = ["name", "ssh_key_path", "created_at"]
    list_filter = ["name",  "created_at"]
    model_icon = 'fa fa-server'
    show_bookmarks = False


class UploadSSHKey(models.Model):
    name = models.CharField(max_length=100, verbose_name="名称")
    ssh_key_path = models.FileField(upload_to='files/ssh_key/%Y/%m', default='', blank=True,
                                    null=True, max_length=200, verbose_name="上传ssh_key")
    desc = models.CharField(max_length=255, blank=True, null=True, verbose_name="上传说明")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")
"""

