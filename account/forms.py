from django import forms
import re
from django.core.exceptions import ValidationError
from django.forms.widgets import Input


def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')


class LoginForm(forms.Form):
    username = forms.CharField(label='账号', widget=Input(attrs={'class': 'form-control', 'placeholder': '请输入账号'}),
                               error_messages={'required': '账号不能为空'})
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}),
                               error_messages={'required': '密码不能为空'})
    # PasswordInput控件来渲染HTMLinput元素，包含type="password"属性


from django.contrib.auth.models import User


class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='账号', widget=Input(attrs={'class': 'form-control', 'placeholder': '请输入账号'}),
                               error_messages={'required': '账号不能为空'})
    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}),
                             error_messages={'required': '邮箱不能为空'})
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}),
                               error_messages={'required': '密码不能为空'})
    password2 = forms.CharField(label='确认密码',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请再次输入密码'}),
                                error_messages={'required': '密码确认不能为空'})

    def clean_username(self):
        cd = self.cleaned_data
        username = cd['username']
        if len(username) < 3:
            raise forms.ValidationError("用户名过短")
        return cd['username']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('两次密码不一致')
        return cd['password2']


from .models import Profile


# UserEditForm：允许用户编辑它们的first name,last name, e-mail 这些储存在User模型（model）中的内置字段。
# ProfileEditForm：允许用户编辑我们存储在定制的Profile模型（model）中的额外数据。用户可以编辑他们的生日数据以及为他们的profile上传一张照片。
class UserEditForm(forms.Form):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='旧密码',
                                   widget=forms.PasswordInput(
                                       attrs={'class': 'form-control', 'placeholder': '请输入原始密码'}),
                                   error_messages={'required': '密码不能为空'})
    password = forms.CharField(label='新密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入新密码'}),
                               error_messages={'required': '密码不能为空'})
    password2 = forms.CharField(label='确认新密码',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请确认新密码'}),
                                error_messages={'required': '密码不能为空'})

    def clean_password2(self):
        cd = self.cleaned_data
        if len(cd['password']) < 8:
            raise forms.ValidationError('请输入至少8位的密码')
        elif cd['password'] != cd['password2']:
            raise forms.ValidationError('两次密码不一致')
        return cd['password2']


class ResetPasswordForm(forms.Form):
    code = forms.CharField(label='验证码',
                           widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请输入发送的验证码"}),
                           error_messages={'required': '密码不能为空'})
    password = forms.CharField(label='新密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入新密码'}),
                               error_messages={'required': '密码不能为空'})
    password2 = forms.CharField(label='确认新密码',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请确认新密码'}),
                                error_messages={'required': '密码不能为空'})

    def clean_password2(self):
        cd = self.cleaned_data
        if len(cd['password']) < 8:
            raise forms.ValidationError('请输入至少8位的密码')
        elif cd['password'] != cd['password2']:
            raise forms.ValidationError('两次密码不一致')
        return cd['password2']

class GetcodeForm(forms.Form):
    account = forms.EmailField(label='账号', widget=forms.EmailInput(attrs={'class': 'form-control',
                              'placeholder': '请输入账号邮箱'}), error_messages={'required': '账号不能为空'})



class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
