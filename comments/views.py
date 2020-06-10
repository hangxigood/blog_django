import rest_framework
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.http import request
from rest_framework import mixins, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from comments.forms import CommentForm
from comments.models import Comment
from myblog.models import Post

'''
基于 Django restful-framework 开发的 API
'''

class CommentSerializer(serializers.ModelSerializer):
    post_url = serializers.SerializerMethodField(read_only=True)

    def get_post_url(self, obj):
        return 'http://blog.frankxiang.xyz/api/v1/Post/{}'.format(obj.post.id)

    class Meta:
        model = Comment
        fields = (
            'post',
            'post_url',
            'name',
            'text',
            'created_time',
        )


class CommentViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    """
    GET /Comment: 获取所有评论内容。<br>
    POST /Comment：新增评论，POST 格式可下拉至底部查看和调试。<br>

    POST 请求需要用户认证。<br>
    可以在 blog.frankxiang.xyz/login/ 登陆获取 token ，访问时增加请求头 Authorization: JWT {token} 即可获取 用户 权限。<br>
    登陆账号/密码： Admin/Admin <br>
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # 只有认证用户可以 post（发表评论），未认证用户只能 get（读取评论）。
    permission_classes = (rest_framework.permissions.IsAuthenticatedOrReadOnly,)

    # def get_queryset(self):
    #     # 根据URL中的 post 参数，返回属于 post 的 Comments 。
    #     requset_post = self.request.GET.get('post_id')
    #     kwargs = {}
    #     if requset_post:
    #         kwargs['post'] = requset_post
    #     return Comment.objects.filter(**kwargs)

'''
基于 Django 模板系统的 FBV
'''

@require_POST  # 仅 POST 请求可调用该函数
def comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(request.POST)  # 取出表单数据，形成表单实例

    if form.is_valid():
        comment = form.save(commit=False)  # 仅生成 Comment 实例，未保存数据库
        comment.post = post
        comment.save()
        messages.add_message(request, messages.SUCCESS, '评论成功!', extra_tags='success')
        return redirect(post)

    context = {
        'post': post,
        'form': form,
    }
    messages.add_message(request, messages.ERROR, '评论失败！', extra_tags='danger')
    return render(request, 'comments/preview.html', context=context)
