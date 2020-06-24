
import markdown
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models

# Create your models here.
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.html import strip_tags


class Category(models.Model):  # The Category of blog's post, like Python, Django...
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


def generate_markdown_content(value):
    content = markdown.markdown(value, extensions=["markdown.extensions.extra",
                                "markdown.extensions.codehilite"])
    return {"content": content}


class Post(models.Model):
    title = models.CharField(verbose_name='标题', max_length=70)
    body = models.TextField(verbose_name='正文')
    created_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now) # auto_now_add=True 也可以 default=timezone.now
    modified_time = models.DateTimeField(verbose_name='修改时间', auto_now=True) # auto_now=True 也可以在save 中 self.modified_time = timezone.now()
    excerpt = models.CharField(verbose_name='摘要', max_length=200, blank=True)
    category = models.ForeignKey(Category, related_name='posts', verbose_name='分类', on_delete=models.CASCADE)
    # one to many, delete together. always define in the many.
    tags = models.ManyToManyField(Tag, related_name='posts', verbose_name='标签', blank=True)
    author = models.ForeignKey(User, default=7, verbose_name='作者', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(verbose_name='阅读数', default=0)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        cache.clear()

        if self.excerpt == '':  # 如果没有写入简介，自行添加正文的前54个字符
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]  # remove anything that looks like an HTML tag

        super().save(*args, **kwargs)

    def body_html(self):
        return self.get_markdown_content.get("content", "")

    @cached_property
    def get_markdown_content(self):
        return generate_markdown_content(self.body)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title

