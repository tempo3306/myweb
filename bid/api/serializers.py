from ..models import Bid_auction, Bid_action, Bid_hander
from rest_framework import serializers

class Bid_actionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bid_action
        fields = [
            'id',
            'diff',
            'refer_time',
            'bid_time',
            'delay_time',
            'ahead_price',
            'action_date',
            'action_result'
        ]

class Bid_handerSerializer(serializers.HyperlinkedModelSerializer):
    hander_actions = serializers.PrimaryKeyRelatedField(many=True,
                                        queryset=Bid_action.objects.all())  #related_name
    class Meta:
        model = Bid_hander
        fields = [
            'hander_actions',  # 外键
            'id',
            'hander_name',
            'basic_salary',
            'total_income'
        ]



class Bid_auctionSerializer(serializers.HyperlinkedModelSerializer):
    auction_actions = serializers.PrimaryKeyRelatedField(many=True,
                                        queryset=Bid_auction.objects.all()) #related_name
    class Meta:
        model = Bid_auction
        fields = [
            'auction_actions',  #外键
            'id',
            'description',
            'auction_name',
            'ID_number',
            'Bid_number',
            'Bid_password',
            'status',
            'count',
            'expired_date'
        ]

