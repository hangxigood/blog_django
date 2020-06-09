import re

import markdown
from django.db.models.functions import ExtractYear, ExtractMonth
from django.shortcuts import get_object_or_404

# Create your views here.
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
    CategoryDetailSerializer, TagsListSerializer, TagsDetailSerializer, CategoryListSerializer, \
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

    def get_serializer_class(self):
        # 根据请求的不同，使用不同的序列化器，在 list 中主要删减了文章主体内容的序列化字段，减小服务器压力。
        if self.action == 'list':
            return PostListSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer
        else:
            return PostPostSerializer

    # def get_serializer_class(self):
    #     # 根据请求的不同，使用不同的序列化器，在 list 中主要删减了文章主体内容的序列化字段，减小服务器压力。
    #     if self.action == 'list':
    #         return PostListSerializer
    #     elif self.action == 'retrieve':
    #         return PostDetailSerializer
    #     else:
    #         return super().get_serializer_class()

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
        return Post.objects.filter(**kwargs)


class TagsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """
    GET    /Tag: 获取所有博客标签。<br>
    GET    /Tag/{TagID}: 通过ID获取博客标签及其相关内容。<br>
    """
    queryset = Tag.objects.all()
    serializer_class = TagsListSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return TagsListSerializer
        elif self.action == 'retrieve':
            return TagsDetailSerializer
        else:
            return super().get_serializer_class()


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """
    GET    /Category: 获取所有博客分类。<br>
    GET    /Category/{CategoryID}: 通过ID获取博客分类及其相关内容。<br>
    """
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        elif self.action == 'retrieve':
            return CategoryDetailSerializer
        else:
            return super().get_serializer_class()


class ArchiveListViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    GET    /Archive: 按照文章发布日期（ 年-月 的格式）进行列表，展现所有相关文章。<br>
    """
    queryset = Post.objects.annotate(year=ExtractYear('created_time'), month=ExtractMonth('created_time'))\
        .values('year', 'month').order_by('-year', '-month').distinct()
    serializer_class = ArchiveDetailSerializer


'''
基于 Django 模板系统的 CBV
'''

class IndexView(PaginationMixin, ListView):
    model = Post
    template_name = 'myblog/index.html'
    context_object_name = 'post_list'
    paginate_by = 5


class PostDetailView(DetailView):
    model = Post
    template_name = 'myblog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)  # 用正则表达式确认是否有目录
        post.toc = m.group(1) if m is not None else ''

        return post


class ArchiveView(PaginationMixin, ListView):
    model = Post
    template_name = 'myblog/index.html'
    context_object_name = 'post_list'
    paginate_by = 5

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super().get_queryset().filter(created_time__year=year,
                                             created_time__month=month
                                             )


class CategoryView(PaginationMixin, ListView):
    model = Post
    template_name = 'myblog/index.html'
    context_object_name = 'post_list'
    paginate_by = 5

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(category=cate)


class Tagview(PaginationMixin, ListView):
    model = Post
    template_name = 'myblog/index.html'
    context_object_name = 'post_list'
    paginate_by = 5

    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(tags=t)