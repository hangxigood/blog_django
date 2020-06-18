import re

import markdown
from django.db.models.functions import ExtractYear, ExtractMonth
from django.shortcuts import get_object_or_404

# Create your views here.
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, DetailView
from markdown.extensions.toc import TocExtension
from pure_pagination import PaginationMixin
from rest_framework import mixins, pagination
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from myblog.models import Post, Category, Tag
from myblog.serializers import PostListSerializer, PostDetailSerializer, \
    TagsListSerializer, CategoryListSerializer, \
    ArchiveDetailSerializer, PostPostSerializer

'''
基于 Django restful-framework 开发的 API
'''

class IsAdminUserOrReadOnly(BasePermission):
    """
    需要 管理员用户 权限执行 GET 以外的请求。
    主要用于文章的 POST/PUT/DELETE 请求。
    """

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or request.user and request.user.is_staff)


class PostViewSet(ModelViewSet):
    """
    GET    /Post: 获取所有的博客文章。<br>
    GET    /Post/{PostID}: 通过ID获取某篇博客文章详细内容。<br>
    GET    /Post/?category={CategoryID}: 通过CategoryID获取 分类为 Category 的所有文章。<br>
    GET    /Post/?tags={TagID}: 通过TagID获取 标签为 Tag 的所有文章。<br>
    GET    /Post/?year={year}&month={month}: 获取文章创建时间的年、月分别等于 year、month 的所有文章。<br>
    POST   /Post：新增文章。<br>
    PUT    /Post/{PostID}: 更新具体某篇博客文章。<br>
    DELETE /Post/{PostID}: 删除具体某篇博客文章。<br>

    其中 POST/PUT/DELETE 请求需要 管理员用户 权限。<br>
    可以在 blog.frankxiang.xyz/login/ 登陆获取 token ，访问时增加请求头 Authorization: JWT {token} 即可获取 管理员用户 权限。<br>
    管理员账号/密码： admin/admin <br>
    """
    queryset = Post.objects.all()
    lookup_field = 'id'
    pagination_class = pagination.PageNumberPagination
    permission_classes = (IsAdminUserOrReadOnly,)

    # @method_decorator(never_cache)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(self, request, *args, **kwargs)

    def get_serializer_class(self):
        # 根据请求的不同，使用不同的序列化器，在 list 中主要删减了文章主体内容和评论内容的序列化字段，减小服务器压力。
        if self.action == 'list':
            return PostListSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer
        else:
            return PostPostSerializer

    def get_queryset(self):
        # 可以根据 /?category={categoryID} 检索相关文章。其他 tags/year-month 同理。
        request_category = self.request.GET.get('category')
        request_tag = self.request.GET.get('tags')
        request_year = self.request.GET.get('year')
        request_month = self.request.GET.get('month')
        kwargs = {}
        if request_category:
            kwargs['category'] = request_category
        if request_tag:
            kwargs['tags'] = request_tag
        if request_month and request_year:
            kwargs['created_time__year'] = request_year
            kwargs['created_time__month'] = request_month
        # 滤掉筛选条件的queryset
        queryset = Post.objects.filter(**kwargs)
        # 将 queryset 预先加载相关字段，减少服务器查询次数。List 和 Retrieve 都可以使用。
        queryset = PostListSerializer.setup_eager_loading(self, queryset)
        return queryset


class TagsViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    GET    /Tag: 获取所有博客标签以及相关文章检索链接。<br>
    """
    queryset = Tag.objects.all()
    serializer_class = TagsListSerializer


class CategoryViewSet(mixins.ListModelMixin,GenericViewSet):
    """
    GET    /Category: 获取所有博客分类以及相关文章检索链接。<br>
    """
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class ArchiveListViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    GET    /Archive: 按照文章发布日期（ 年-月 的格式）进行列表，展现相关文章检索链接。<br>
    """
    queryset = Post.objects.annotate(year=ExtractYear('created_time'), month=ExtractMonth('created_time'))\
        .values('year', 'month').order_by('-year', '-month').distinct()
    serializer_class = ArchiveDetailSerializer