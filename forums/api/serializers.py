from rest_framework import serializers
from forums.models import ForumUser, Board, Topic, Post


class ForumUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ForumUser
        fields = [

        ]



class BoardSerializer(serializers.HyperlinkModelSerializer):
    class Meta:
        model = Board
        fields = [

        ]