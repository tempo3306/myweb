from django.contrib import admin

from .models import Board, Topic, Post, ForumUser

admin.site.register((Board, Topic, Post, ForumUser))
