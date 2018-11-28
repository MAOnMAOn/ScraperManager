from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name="昵称", default="")
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(("male", "男"), ("female", "女")), default="male")
    address = models.CharField(max_length=100, default="")
    mobile = models.CharField(max_length=12, null=True, blank=True)
    # 因为图像在后台存储的时候是一个字符串形式,所以要一个max_length参数
    image = models.ImageField(upload_to="image/%Y/%m", default="image/default.png", max_length=120)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(max_length=30, choices=(("register", "注册"), ("forget", "找回密码"),
                                                         ("update_email", "修改邮箱")), verbose_name="验证码类型")
    #  datetime.now():default时间为EmailVerifyRecord编译时间, 而datetime.now 为类的实例化时间
    send_time = models.DateField(default=datetime.now, verbose_name="发送时间")

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}[{1}]'.format(self.code, self.email)


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name="接收用户")  # 0 表示面向全体用户
    message = models.CharField(max_length=300, verbose_name="消息内容")
    has_read = models.BooleanField(default=False, verbose_name="是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"发送时间")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户: %s 是否已读: %s' % (self.user, self.has_read)
