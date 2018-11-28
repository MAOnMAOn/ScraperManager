# Create your models here.
from django.db.models import Model, CharField, IntegerField, TextField, DateTimeField, \
    BooleanField, ManyToManyField, ForeignKey, CASCADE


class Client(Model):
    name = CharField(max_length=255, verbose_name="ScrapydClient")
    ip = CharField(max_length=255, verbose_name="ip地址")
    port = IntegerField(default=6800,  verbose_name="端口")
    desc = TextField(blank=True, null=True, verbose_name="说明")
    auth = BooleanField(default=False, verbose_name="是否授权")
    # auth = IntegerField(default=0, blank=True, null=True, verbose_name="授权")
    username = CharField(max_length=255, blank=True, null=True, verbose_name="用户名")
    password = CharField(max_length=255, blank=True, null=True, verbose_name="密码")
    created_at = DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = 'Scrapyd客户端'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Project(Model):
    name = CharField(max_length=255, default=None, verbose_name="项目名称")
    desc = CharField(max_length=255, null=True, blank=True, verbose_name="项目说明")
    egg = CharField(max_length=255, null=True, blank=True)
    configuration = TextField(blank=True, null=True, verbose_name="配置")
    configurable = IntegerField(default=0, blank=True, verbose_name="是否配置")
    built_at = DateTimeField(default=None, blank=True, null=True, verbose_name="打包时间")
    generated_at = DateTimeField(default=None, blank=True, null=True, verbose_name="生成时间")
    created_at = DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = DateTimeField(auto_now=True, verbose_name="更新时间")
    clients = ManyToManyField(Client, through='Deploy', unique=False, verbose_name="Scrapyd客户端")

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name  # 这样可以直接 list_display


class Deploy(Model):
    client = ForeignKey(Client, unique=False, on_delete=CASCADE, verbose_name="Scrapyd客户端")
    project = ForeignKey(Project, unique=False, on_delete=CASCADE, verbose_name="项目名称")
    desc = CharField(max_length=255, blank=True, null=True, verbose_name="部署说明")
    deployed_at = DateTimeField(default=None, blank=True, null=True, verbose_name="部署时间")
    created_at = DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = '部署'
        verbose_name_plural = verbose_name
        unique_together = ('client', 'project')

    def __str__(self):
        return "项目部署"

