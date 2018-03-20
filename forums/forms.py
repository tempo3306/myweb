from django import forms

from .models import Topic, Post
from django.utils.translation import ugettext_lazy as _




#Add to a form containing a FileField and change the field names accordingly.
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy
from django.conf import settings




class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(),
        max_length=4000,
        help_text='最大长度4000个字符',
        label="内容"
    )

    class Meta:
        model = Topic
        fields = ['subject', 'message']
        labels = {'subject': '主题'}


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]
        help_texts = {'message': '最大长度4000个字符'}
        labels = {'message': '内容'}


class Change_profileForm(forms.Form):
    nickname = forms.CharField(max_length=10, widget=forms.widgets.TextInput(attrs={'class': 'form-control'}))
    signature = forms.CharField(max_length=50, widget=forms.widgets.TextInput(attrs={'class': 'form-control'}))
    gender = forms.IntegerField(label="性别", widget=forms.widgets.Select(choices=((1, '男'), (0, '女'), (-1, '保密')),
                                attrs={'class': 'form-control'}), initial=(-1, '保密'))  ##1代表男性， 0代表女性， -1代表未设定
    photo = forms.FileField(label='上传头像')

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        content_type = photo.content_type.split('/')[0]
        if content_type in settings.CONTENT_TYPES:
            if photo._size > int(settings.MAX_PHOTO_SIZE):
                raise forms.ValidationError(ugettext_lazy('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
        else:
            raise forms.ValidationError(ugettext_lazy('File type is not supported'))
        return photo