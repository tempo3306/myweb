from ..models import *
from rest_framework import serializers

##代拍管理
## 团队
class Bid_groupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bid_group
        fileds = [
            'group_name',
        ]

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

## 
class ConsumerSerializer(serializers.HyperlinkedModelSerializer):
    consumer_softwares = serializers.PrimaryKeyRelatedField(many=True,
                                        queryset=Consumer_software.objects.all()) #related_name
    consumer_bids = serializers.PrimaryKeyRelatedField(many=True,
                                        queryset=Consumer_bid.objects.all()) #related_name
    class Meta:
        model = Consumer
        fields = [
            'consumer_softwares',
            'consumer_bids',
        ]




##购买激活码的用户
class Consumer_softwareSerializer(serializers.HyperlinkedModelSerializer):
    identify_codes = serializers.PrimaryKeyRelatedField(many=True,
                                                        queryset=Identify_code.objects.all())
    class Meta:
        model = Consumer_software
        fields = [
            'order_number',
            'identify_codes',
        ]


class Identify_codeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Identify_code
        fields = [
            'identity_code',
            'purchase_date',
            'expired_date',
            'bid_name',
        ]



class Invite_codeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Invite_code
        fields = [
            'invite_code',
            'type',
        ]


class Consumer_bidSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Consumer_bid
        fields = [
            'status',
            'order_money',
            'compensation',
            'bid_number',
            'did_number',
        ]


##------------------------------------------------------------------------------------------
