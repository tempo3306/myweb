from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from .forms import LoginForm, ChangePasswordForm
from .models import Profile
from django.contrib.auth.models import User
from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated success')
                else:
                    return HttpResponse('Disabled  account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


from django.contrib.auth.decorators import login_required
@login_required
def dashboard(request):
    return render(request,
                 'account/dashboard.html',
                 {'section': 'dashboard'})

from .forms import LoginForm, UserRegistrationForm
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid(): #获取表单信息
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            password2 = user_form.cleaned_data['password2']
            namefilter = User.objects.filter(username = username)
            if len(namefilter) > 0:
                return render(request,
                              'account/register.html',
                              {'user_form': user_form, 'error':'用户名已经存在！'})
            elif password != password2:
                return render(request,
                              'account/register.html',
                              {'user_form': user_form, 'error':'两次密码不一致！'})
            else:
                try:
                    new_user = User.objects.create_user(username=username, password=password)
                    return render(request,
                                  'account/register_done.html',
                                  {'new_user': new_user})
                except:
                    return render(request,
                                  'account/register.html',
                                  {'user_form': user_form, 'error': '创建失败，请重试'})
        else:
            user_form = UserRegistrationForm()
            return render(request,
                          'account/register.html',
                          {'user_form': user_form})
    else:
        user_form = UserRegistrationForm()
        return render(request,
                  'account/register.html',
                  {'user_form': user_form})




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
    if request.method == 'POST':
        change_password_form = ChangePasswordForm(request.POST)
        if change_password_form.is_valid():
            old_password = change_password_form.cleaned_data['old_password']
            password = change_password_form.cleaned_data['password']
            password2 = change_password_form.cleaned_data['password2']
            #验证旧密码
            user = request.user
            if user.check_password(old_password):  #验证旧密码
                if password != password2:
                    return render(request,
                                  'account/change_password.html',
                                  {'change_password_form': change_password_form,
                                   'error': '两次密码不一致'})
                else:
                    user.set_password('password')  #修改密码
                    return  render(request,
                                   'registration/password_change_done.html')
            else:
                return render(request,
                              'account/change_password.html',
                              {'change_password_form': change_password_form,
                               'error': '请输入正确的旧密码'})
        else:
            change_password_form = ChangePasswordForm()
            return  render(request,
                           'account/change_password.html',
                           {'change_password_form': change_password_form,
                            'error': '请正确填写表单'
                            })

    else:
        change_password_form = ChangePasswordForm()
        return  render(request,
                       'account/change_password.html',
                       {'change_password_form': change_password_form,
                        })