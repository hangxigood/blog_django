from django.db.models import Count
from django.http import request
from django.urls import reverse
from rest_framework import serializers

import comments
from comments.views import CommentSerializer
from myblog.models import Post, Category, Tag


class CategoryListSerializer(serializers.HyperlinkedModelSerializer):
    posts_url = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = [
            'name',
            'posts_url',
        ]

    def get_posts_url(self, obj):
        return 'http://blog.frankxiang.xyz/api/v1/Post/?category=' + str(obj.id)


class TagsListSerializer(serializers.ModelSerializer):
    posts_url = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = [
            'name',
            'posts_url',
        ]

    def get_posts_url(self, obj):
        return 'http://blog.frankxiang.xyz/api/v1/Post/?tags=' + str(obj.id)


class PostListSerializer(serializers.HyperlinkedModelSerializer):
    category = CategoryListSerializer()
    author = serializers.StringRelatedField()
    tags = TagsListSerializer(many=True)
    comments_num = serializers.SerializerMethodField()

    def get_comments_num(self, obj):
        return obj.comments_count
        # return obj.comments.count()

    @staticmethod
    def setup_eager_loading(cls, queryset):
        queryset = queryset.select_related('category')
        queryset = queryset.select_related('author')
        queryset = queryset.prefetch_related('tags')
        queryset = queryset.annotate(comments_count=Count(comments))
        return queryset

    class Meta:
        model = Post
        fields = (
            'title',
            'url',
            'author',
            'created_time',
            'excerpt',
            'category',
            'tags',
            'views',
            'comments_num',
        )
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }


class PostPostSerializer(serializers.ModelSerializer):
    post = serializers.HyperlinkedIdentityField(view_name='post-detail', lookup_field='id' , read_only=True)

    class Meta:
        model = Post
        fields = (
            'post',
            'title',
            'excerpt',
            'body',
            'category',
            'tags',
        )


class ArchiveDetailSerializer(serializers.Serializer):
    year = serializers.IntegerField(read_only=True)
    month = serializers.IntegerField(read_only=True)
    posts_url = serializers.SerializerMethodField()

    def get_posts_url(self, obj):
        return 'http://blog.frankxiang.xyz/api/v1/Post/?year={}&month={}'.format(obj['year'], obj['month'])

    # def get_posts(self,obj):
    #     queryset = Post.objects.filter(created_time__year=obj['year'], created_time__month=obj['month'])
    #     return PostListSerializer(queryset, many=True, context={'request': self.context.get('request')}).data


class PostDetailSerializer(serializers.HyperlinkedModelSerializer):
    category = CategoryListSerializer()
    author = serializers.StringRelatedField()
    tags = TagsListSerializer(many=True)
    comments_num = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True)

    def get_comments_num(self, obj):
        return obj.comments.count()

    class Meta:
        model = Post
        fields = [
            'title',
            'url',
            'author',
            'excerpt',
            'body',
            'category',
            'tags',
            'views',
            'comments_num',
            'comments',
        ]

        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }






