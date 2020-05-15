import re

import markdown
from django.shortcuts import get_object_or_404

# Create your views here.
from django.utils.text import slugify
from django.views.generic import ListView, DetailView
from markdown.extensions.toc import TocExtension
from pure_pagination import PaginationMixin
from rest_framework.viewsets import ModelViewSet

from myblog.models import Post, Category, Tag
from myblog.serializers import PostListSerializer


class IndexView(PaginationMixin, ListView):
    model = Post
    template_name = 'myblog/index.html'
    context_object_name = 'post_list'
    paginate_by = 5


class PostListView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


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
        return super().get_queryset().filter(tag=t)
