from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db import models

# Create your models here.
from django.utils import timezone


class Comment(models.Model):
    name = models.CharField(verbose_name='名字', max_length=50)
    email = models.EmailField(verbose_name='邮箱')
    url = models.URLField(verbose_name='', blank=True)
    text = models.TextField(verbose_name='评论')
    created_time = models.DateTimeField(verbose_name='评论时间', auto_now=True) #  default=timezone.now
    post = models.ForeignKey('myblog.Post', related_name='comments' ,verbose_name='所属文章', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return '{}:{}'.format(self.name, self.text[:20])

    def save(self, *args, **kwargs):
        cache.clear()
        super().save(*args, **kwargs)

