import rest_framework

# Create your views here.
from rest_framework import mixins, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.reverse import reverse
from rest_framework.viewsets import GenericViewSet

from comments.models import Comment

'''
基于 Django restful-framework 开发的 API
'''

class CommentSerializer(serializers.ModelSerializer):
    post_url = serializers.SerializerMethodField(read_only=True)

    def get_post_url(self, obj):
        return ''.join([reverse('post-list', request=self.context['request']), str(obj.post_id)])

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
