from django.shortcuts import render

# Create your views here.


def news(request):
    return render(request, 'news/news.html')



##购买软件视图
def purchase_software(request):
    return render(request, 'bid/purchase_software.html')


##购买代拍视图
def purchase_bid(request):
    return render(request, 'bid/purchase_bid.html')