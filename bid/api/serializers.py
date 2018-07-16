from ..models import *
from rest_framework import serializers


##代拍管理


class Bid_actionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid_action
        fields = '__all__'
        # fields = [
        #     'id',
        #     'diff',
        #     'refer_time',
        #     'bid_time',
        #     'delay_time',
        #     'ahead_price',
        #     'hander_id',
        #     'action_date',
        #     'auction_id', #ModelSerializer 转换成了外键网址
        #     'action_result',
        # ]

class Bid_handerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid_hander
        fields = [
            'id',
            'user_id',
            'hander_name',
            'basic_salary',
            'total_income',
            'extra_bonus',
        ]

class Bid_recordSerializer(serializers.ModelSerializer):
    # auction_name = serializers.RelatedField(source='auction', read_only=True)
    # hander = serializers.RelatedField(source='hander', read_only=True)
    auction_name = serializers.CharField(source='auction.auction_name')
    Bid_number = serializers.CharField(source='auction.Bid_number')
    hander_name = serializers.CharField(source='hander.hander_name')
    hander_telephone = serializers.CharField(source='hander.telephone')

    class Meta:
        model = Bid_record
        fields = [
            'id',
            'hander_name',
            'Bid_number',
            'auction_name',
            'date',
            'strategy_dick',
            'result',
            'firstprice',
            'hander_telephone',
        ]


class Bid_auctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid_auction
        fields = [
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

##筛选未绑定的标书
##筛选未绑定的标书
class Bid_auctionAvailableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid_auction
        fields = [
            'id',
            'auction_name',
        ]




## 
class ConsumerSerializer(serializers.ModelSerializer):
    consumer_bids = serializers.PrimaryKeyRelatedField(many=True,
                                        queryset=Consumer_bid.objects.all()) #related_name
    class Meta:
        model = Consumer
        fields = [
            'consumer_bids',
        ]





class Identify_codeSerializer(serializers.ModelSerializer):
    auction = Bid_auctionSerializer(many=True)

    # canbid = serializers.CharField(source='can_bid', read_only=True)
    # likescount = serializers.SerializerMethodField('get_popularity')
    # def popularity(self, obj):
    #     likes = obj.post.count
    #     time =  # hours since created
    #     return likes / time if time > 0 else likes

    bid_status = serializers.BooleanField(source='can_bid')  # 不能与原来的属性重名

    class Meta:
        model = Identify_code
        fields = [
            'id',
            'identify_code',
            'purchase_date',
            'expired_date',
            'bid_name',
            'auction',
            'strategy_dick',
            'bid_status'
        ]

class StrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = Strategy
        fields = '__all__'





class Invite_codeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite_code
        fields = [
            'invite_code',
            'type',
        ]


class Consumer_bidSerializer(serializers.ModelSerializer):
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
