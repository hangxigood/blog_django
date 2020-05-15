from django.contrib import admin

# Register your models here.
from myblog.models import Post, Category, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_time', 'modified_time')
    ordering = ('-created_time',)
    fields = ['title', 'body', 'excerpt', 'category', 'tags']
    search_fields = ['title']

    def save_model(self, request, obj, form, change):  # 重写方法，实现自动关联作者
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)

