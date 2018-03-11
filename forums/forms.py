from django import forms

from .models import Topic, Post
from django.utils.translation import ugettext_lazy as _


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
        labels = {'subject':'主题'}


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]
        help_texts = {'message': '最大长度4000个字符'}
        labels = {'message': '内容'}