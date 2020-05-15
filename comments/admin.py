from django.contrib import admin

# Register your models here.
from comments.models import Comment


class Commentadmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created_time')
    ordering = ('-created_time',)
    fields = ('name', 'email', 'text', 'post')
    search_fields = ['text']


admin.site.register(Comment, Commentadmin)