from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from .forms import LoginForm, ChangePasswordForm
from .models import Profile
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from account.models import EmailVerifyRecord
from django.db import transaction
from django.urls import reverse
#导入异步邮件
from tools.tasks import confirm_email

##登录
def user_login(request):
    if request.method == 'GET':
        request.session['login_from'] = request.GET.get('next', '/')
        # request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(request.session['login_from'])
                else:
                    return render(request,
                                  'account/login.html',
                                  {'user_form': form, 'error': '账号未激活！'})
            else:
                return render(request,
                              'account/login.html',
                              {'user_form': form, 'error': '账号或密码错误！'})
    form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


from .forms import LoginForm, UserRegistrationForm

#测试异步邮件
def test_email(request):
    confirm_email.delay('810909753@qq.com')  ##异步发邮件
    return HttpResponse("发送中")

def register(request):
    user_form = UserRegistrationForm(request.POST)
    if request.method == 'POST':
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']
            password2 = user_form.cleaned_data['password2']
            namefilter = User.objects.filter(username=username)
            emailfilter = User.objects.filter(email=email)
            if len(namefilter) > 0:
                return render(request,
                              'account/register.html',
                              {'user_form': user_form, 'errors': '用户名已经存在！'})
            elif len(emailfilter) > 0:
                return render(request,
                              'account/register.html',
                              {'user_form': user_form, 'errors': '邮箱已经存在！'})
            else:
                try:
                    with transaction.atomic():
                        new_user = User.objects.create_user(username=username, password=password,
                                                        email=email, is_active=False)
                        confirm_email.delay(email) ##异步发邮件

                        return render(request,
                                  'account/register_done.html',
                                  {'new_user': new_user})
                except:
                    return render(request,
                                  'account/register.html',
                                  {'user_form': user_form, 'errors': '创建失败，请重试'})
        else:
            error = user_form.errors
            return render(request, 'account/register.html', {'user_form': user_form, 'error': error})
    return render(request, 'account/register.html', {'user_form': user_form})


##用户点击该链接激活账号
class ActiveUserView(View):
    def get(self, request, active_code):
    # 用code在数据库中过滤处信息
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                # 通过邮箱查找到对应的用户
                user = User.objects.get(email=email)
                # 激活用户
                user.is_active = True
                user.save()
        else:
            return render(request, "account/active_fail.html")
        return render(request, "account/login.html")

##用户要求重新发送激活邮件
class ReActiveEmailView(View):
    def get(self, request):
        user = request.user
        if user.is_active:
            return HttpResponseRedirect(request.session['login_from'])
        else:
            email = user.email
            confirm_email.delay(email)  ##异步发邮件



from .forms import LoginForm, UserRegistrationForm, \
    UserEditForm, ProfileEditForm


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated '
                                      'successfully')
        else:
            messages.error(request, 'Something went wrong')  # 输出错误消息
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


@login_required
def change_password(request):
    change_password_form = ChangePasswordForm(request.POST)
    if request.method == 'POST':
        if change_password_form.is_valid():
            old_password = change_password_form.cleaned_data['old_password']
            password = change_password_form.cleaned_data['password']
            password2 = change_password_form.cleaned_data['password2']
            # 验证旧密码
            user = request.user
            if user.check_password(old_password):  # 验证旧密码
                if password != password2:
                    return render(request,
                                  'account/change_password.html',
                                  {'change_password_form': change_password_form,
                                   'error': '两次密码不一致'})
                else:
                    user.set_password('password')  # 修改密码
                    return render(request,
                                  'registration/password_change_done.html',
                                  )
            else:
                return render(request,
                              'account/change_password.html',
                              {'change_password_form': change_password_form,
                               'error': '请输入正确的旧密码'})
        else:
            error = change_password_form.errors
            return render(request,
                          'account/change_password.html',
                          {'change_password_form': change_password_form,
                           'error': error
                           })
    else:
        return render(request,
                      'account/change_password.html',
                      {'change_password_form': change_password_form,
                       })
