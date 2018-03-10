from django.urls import path

from . import views

urlpatterns = [
    path('', views.BoardListView.as_view(), name='home'),
    path('boards/<str:name>/', views.board_topics, name='board_topics'),
    path('boards/<str:name>/new/', views.new_topic, name='new_topic'),
    path('boards/<str:name>/<int:topic_pk>/', views.topic_posts, name='topic_posts'),
    path('boards/<str:name>/<int:topic_pk>/reply/', views.reply_topic, name='reply_topic'),
]
