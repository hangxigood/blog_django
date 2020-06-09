from django.http import request
from django.urls import reverse
from rest_framework import serializers

from comments.views import CommentSerializer
from myblog.models import Post, Category, Tag


class CategoryListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = [
            'name',
            'url',
        ]


class TagsListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'name',
            'url',
        ]


class PostListSerializer(serializers.HyperlinkedModelSerializer):
    category = CategoryListSerializer()
    author = serializers.StringRelatedField()
    tags = TagsListSerializer(many=True)
    comments_num = serializers.SerializerMethodField()

    def get_comments_num(self, obj):
        return obj.comments.count()

    class Meta:
        model = Post
        fields = (
            'title',
            'url',
            'author',
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
    posts = serializers.SerializerMethodField()

    def get_posts(self,obj):
        queryset = Post.objects.filter(created_time__year=obj['year'], created_time__month=obj['month'])
        return PostListSerializer(queryset, many=True, context={'request': self.context.get('request')}).data


class CategoryDetailSerializer(serializers.HyperlinkedModelSerializer):
    posts = PostListSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            'name',
            'url',
            'posts',
        )
        extra_kwargs = {
            'posts': {'lookup_field': 'id'}
        }


class TagsDetailSerializer(serializers.HyperlinkedModelSerializer):
    posts = PostListSerializer(many=True)

    class Meta:
        model = Tag
        fields = [
            'name',
            'url',
            'posts',
        ]
        extra_kwargs = {
            'posts': {'lookup_field': 'id'}
        }


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






