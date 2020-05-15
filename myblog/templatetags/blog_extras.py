from django import template
from django.db.models import Count
from django.db.models.functions import ExtractYear, ExtractMonth
from django.shortcuts import get_object_or_404

from myblog.models import Post, Category, Tag

register = template.Library()


@register.inclusion_tag('myblog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.all()[:num]
    }


'''
原版本，无法统计文章数目
@register.inclusion_tag('myblog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': Post.objects.dates('created_time', 'month', order='DESC'),
    }


迭代增加属性，效率低
@register.inclusion_tag('myblog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    date_list = Post.objects.dates('created_time', 'month', order='DESC')
    date_list_count = []

    for date in date_list:
        num_posts = Post.objects.filter(created_time__year=date.year, created_time__month=date.month).count()
        date_list_count.append({'year': date.year, 'month': date.month, 'num_posts': num_posts})

    return {
        'date_list': date_list_count,
    }
'''


@register.inclusion_tag('myblog/inclusions/_archives.html', takes_context=True)  # 善用 sql 聚合，高效
def show_archives(context):
    date_list = Post.objects.annotate(year=ExtractYear('created_time'), month=ExtractMonth('created_time')) \
        .values('year', 'month').order_by('year', 'month').annotate(num_posts=Count('id'))
    return {
        'date_list': date_list,
    }


@register.inclusion_tag('myblog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'category_list': category_list,
    }


@register.inclusion_tag('myblog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list,
    }
