from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.db.models import Count

from .forms import NewTopicForm, PostForm, Change_profileForm
from .models import Board, Post, Topic, ForumUser

# 导入Paginator,EmptyPage和PageNotAnInteger模块
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from tools.utils import handle_fileupload

##主页，显示所有版块
class BoardListView(ListView):
    template_name = 'forums/home.html'
    model = Board

def home(request):
    boards = Board.objects.all()
    topics = Topic.objects.all()
    count = topics.count()
    if count > 15:
        topics = Topic.objects.order_by('last_updated')[:15]
    context = {'boards': boards, 'topics': topics}
    return render(request=request, template_name='forums/home.html', context=context)




##查看版块帖子
def board_topics(request, name):
    board = get_object_or_404(Board, name=name)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    p = Paginator(topics, 20)  # 分页，20篇文章一页
    if p.num_pages <= 1:  # 如果文章不足一页
        article_list = topics  # 直接返回所有文章
        data = ''  # 不需要分页按钮
    else:
        page = int(request.GET.get('page', 1))  # 获取请求的文章页码，默认为第一页
        article_list = p.page(page)  # 返回指定页码的页面
        left = []  # 当前页左边连续的页码号，初始值为空
        right = []  # 当前页右边连续的页码号，初始值为空
        left_has_more = False  # 标示第 1 页页码后是否需要显示省略号
        right_has_more = False  # 标示最后一页页码前是否需要显示省略号
        first = False  # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        last = False  # 标示是否需要显示最后一页的页码号。
        total_pages = p.num_pages
        page_range = p.page_range
        if page == 1:  # 如果请求第1页
            right = page_range[page:page + 2]  # 获取右边连续号码页
            if right[-1] < total_pages - 1:  # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
                # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
                right_has_more = True
            if right[-1] < total_pages:  # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
                # 所以需要显示最后一页的页码号，通过 last 来指示
                last = True
        elif page == total_pages:  # 如果请求最后一页
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]  # 获取左边连续号码页
            if left[0] > 2:
                left_has_more = True  # 如果最左边的号码比2还要大，说明其与第一页之间还有其他页码，因此需要显示省略号，通过 left_has_more 来指示
            if left[0] > 1:  # 如果最左边的页码比1要大，则要显示第一页，否则第一页已经被包含在其中
                first = True
        else:  # 如果请求的页码既不是第一页也不是最后一页
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]  # 获取左边连续号码页
            right = page_range[page:page + 2]  # 获取右边连续号码页
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        data = {  # 将数据包含在data字典中
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
            'total_pages': total_pages,
            'page': page
        }
    return render(request, 'forums/board_topics.html', context={
        'article_list': article_list, 'data': data, 'board': board
    })


##创建主题
@login_required
def new_topic(request, name):
    board = get_object_or_404(Board, name=name)
    user = request.user

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            topic = Topic(subject=cd['subject'],  board=board, starter=user)
            topic.save()
            Post.objects.create(
                message=cd['message'],
                topic=topic,
                created_by=user,
            )
            return redirect('topic_posts', name=name, topic_slug=topic.slug)
    else:
        form = NewTopicForm()

    context = {'board': board, 'form': form}
    return render(request, 'forums/new_topic.html', context)

##查看帖子
def topic_posts(request, name, topic_slug):
    topic = get_object_or_404(Topic, board__name=name, slug=topic_slug)
    topic.views += 1
    topic.save()
    context = {'topic': topic}
    return render(request, 'forums/topic_posts.html', context)


##帖子回复
@login_required
@permission_required('account.post')
def reply_topic(request, name, topic_slug):
    topic = get_object_or_404(Topic, board__name=name, pk=topic_slug)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=name, topic_slug=topic_slug)
    else:
        form = PostForm()
    context = {'topic': topic, 'form': form}
    return render(request, 'forums/reply_topic.html', context)


@login_required
@permission_required('account.post', login_url='/')  # login_url 跳转的页面
def test(request):
    return HttpResponse("成功")



@login_required
def change_profile(request):
    if request.method == 'POST':
        form = Change_profileForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            nickname = cd['nickname']  ##昵称
            signature = cd['signature']  ##签名
            gender = cd['gender']  ##性别
            photo = request.FILES['photo']
            p = 'user_image'
            newname = handle_fileupload(photo, p)  ##处理上传文件
            ForumUser.objects.filter(user=request.user).update(nickname=nickname, gender=gender,
                                                                       photo=newname, signature=signature)

            context = {'form': form, 'type': 'info', 'information': '修改资料成功'}

            return render(request, 'forums/change_profile.html', context=context )
        else:
            context = {'form': form, 'type': 'error', 'information': '修改资料失败'}
            return render(request, 'forums/change_profile.html', context=context)
    else:
        forum_user = ForumUser.objects.get(user=request.user)
        form = Change_profileForm(
            data={'signature': forum_user.signature, 'gender': forum_user.gender, 'nickname': forum_user.nickname})
        return render(request, 'forums/change_profile.html', context={'form': form})
