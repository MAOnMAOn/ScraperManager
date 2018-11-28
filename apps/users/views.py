from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import View
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from utils.email_send import send_register_email
from .models import UserProfile, EmailVerifyRecord, UserMessage
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm


class CustomBackend(ModelBackend):
    """
    自定义登录，　比如邮箱也可以用于用户名
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    """
    进行用户激活
    """
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records.exists():
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "users/active_fail.html")
        return render(request, "users/login.html")


class LoginView(View):
    def get(self, request):
        return render(request, "users/login.html", {})
    
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "users/login.html", {"msg": "用户未激活"})
            else:
                return render(request, "users/login.html", {"msg": "用户名或密码出错"})
        else:
            return render(request, "users/login.html", {"login_form": login_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "users/register.html", {'register_form': register_form})
    
    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "users/register.html", {'msg': "用户已经存在！", 'register_form': register_form})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()
            
            # user_message = UserMessage()
            # user_message.user = user_profile
            # user_message.message = "欢迎注册ScraperManager"
            # user_message.save()
            
            send_register_email(user_name, "register")
            return render(request, "users/login.html")
        else:
            return render(request, "users/register.html", {'register_form': register_form})


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "users/forget_pwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "users/send_success.html")
        else:
            return render(request, "users/forget_pwd.html", {"forget_form": forget_form})


class RestPasswordView(View):
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records.exists():
            for record in all_records:
                email = record.email
                return render(request, "users/password_reset.html", {"email": email})
        else:
            return render(request, "users/active_fail.html")
        return render(request, "users/login.html")


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email")
            if pwd1 != pwd2:
                return render(request, "users/password_reset.html", {"email": email, "msg": "密码不一致！"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, "users/login.html")
        else:
            email = request.POST.get("email")
            return render(request, "users/password_reset.html", {"email": email, "modify_form": modify_form})


class IndexView(View):
    """
    首页
    """
    def get(self, request):

        return render(request, "index.html", {
        })


def page_no_found(request):
    """
    全局404
    :param request:
    :return:
    """
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    """
    全局500处理函数
    :param request:
    :return:
    """
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response

