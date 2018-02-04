from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput) #PasswordInput控件来渲染HTMLinput元素，包含type="password"属性
from django.contrib.auth.models import User
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


from .models import Profile


# UserEditForm：允许用户编辑它们的first name,last name, e-mail 这些储存在User模型（model）中的内置字段。
# ProfileEditForm：允许用户编辑我们存储在定制的Profile模型（model）中的额外数据。用户可以编辑他们的生日数据以及为他们的profile上传一张照片。
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')