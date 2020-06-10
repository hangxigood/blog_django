"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import never_cache
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from blog import settings
from myblog import views as myblog_views
from comments import views as comments_views


router = routers.DefaultRouter()
router.register(r'Post', myblog_views.PostViewSet)
router.register(r'Tag', myblog_views.TagsViewSet),
router.register(r'Category', myblog_views.CategoryViewSet)
router.register(r'Archive', myblog_views.ArchiveListViewSet, basename='Archive') # 因为 queryset 用的是 Post , 所以必须指定 basename
router.register(r'Comment', comments_views.CommentViewSet)

router.get_api_root_view().cls.__name__ = "Easy blog root API"
router.get_api_root_view().cls.__doc__ = "这里是基于 Django rest-framework 搭建的博客后端 API，主要涉及 博客文章的增删改查、评论的增加、文章分类、标签、归档的展示等功能。<br><br> 作者：向航希 hangxigood@gmail.com"


urlpatterns = [
    path('hangxiadmin/', admin.site.urls),
    path('', include('myblog.urls')),
    path('', include('comments.urls')),
    path("api/<version>/", include(router.urls)),
    path('login/', obtain_jwt_token, name='login'),
]

if settings.DEBUG:

    import debug_toolbar

    urlpatterns.insert(0, path('__debug__/', include(debug_toolbar.urls)))


