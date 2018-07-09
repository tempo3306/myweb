from django.contrib import admin
from .models import *
# Register your models here.

class Bid_handerAdmin(admin.ModelAdmin):
    list_display = ('hander_name', 'basic_salary', 'extra_bonus', 'total_income')
    list_filter = ('hander_name', 'basic_salary', 'extra_bonus', 'total_income')
    search_fields = ('hander_name',)
    ordering = ['hander_name']

class Bid_actionAdmin(admin.ModelAdmin):
    list_display = ('diff', 'refer_time', 'bid_time', 'delay_time', 'ahead_price', 'hander_id',
                    'action_date', 'auction_id', 'action_result')
    list_filter = ('action_date', 'auction_id', 'action_result')
    search_fields = ('action_date', 'auction_id', 'action_result')
    ordering = ['action_date', 'action_result']

class Bid_auctionAdmin(admin.ModelAdmin):
    list_display = ('auction_name', 'ID_number', 'Bid_number', 'Bid_password', 'status',
                    'count', 'expired_date')
    list_filter = ('auction_name', 'ID_number', 'Bid_number',  'status',
                    'count', 'expired_date')
    search_fields = ('auction_name', 'ID_number', 'Bid_number', 'status', 'count', 'expired_date')
    ordering = ['status', 'auction_name']

class Bid_recordAdmin(admin.ModelAdmin):
    list_display = '__all__'
    list_filter = '__all__'
    search_fields = '__all__'
    ordering = '__all__'



admin.site.register(Bid_hander, Bid_handerAdmin)
admin.site.register(Bid_auction, Bid_auctionAdmin)
admin.site.register(Bid_action, Bid_actionAdmin)
admin.site.register(Invite_code)
admin.site.register(Identify_code)
admin.site.register(Consumer_bid)
admin.site.register(Consumer)
admin.site.register(Bid_record)
