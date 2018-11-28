import socket
from random import Random

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from ScraperManager.settings import DEFAULT_FROM_EMAIL


def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def random_str(random_length=8):
    email_str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        email_str += chars[random.randint(0, length)]
    return email_str


def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    ip = get_host_ip()

    email_title = ""
    email_body = ""
    if send_type == "register":
        email_title = "注册激活"
        email_body = "请点击激活：http://{ip}:8000/active/{code}".format(ip=ip, code=code)

        send_status = send_mail(email_title, email_body, DEFAULT_FROM_EMAIL, [email])
        if send_status:
            pass

    elif send_type == "forget":
        email_title = "重置密码"
        email_body = "请点击重置密码：http://{ip}:8000/reset/{code}".format(ip=ip, code=code)

        send_status = send_mail(email_title, email_body, DEFAULT_FROM_EMAIL, [email])
        if send_status:
            pass

    elif send_type == "update_email":
        email_title = "修改邮箱验证码"
        email_body = "你的邮箱验证码为：{0}".format(code)
        send_status = send_mail(email_title, email_body, DEFAULT_FROM_EMAIL, [email])
        if send_status:
            pass


def send_info_email():
    pass
