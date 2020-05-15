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
from rest_framework import routers

from blog import settings
from myblog import views

router = routers.DefaultRouter()
router.register(r'PostList', views.PostListView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myblog.urls')),
    path('', include('comments.urls')),
    path('search/', include('haystack.urls')),
    path("api/<version>/", include(router.urls)),
    path("api/auth/", include("rest_framework.urls", namespace="rest_framework")),
]
'''''
if settings.DEBUG:

    import debug_toolbar

    urlpatterns.insert(0, path('__debug__/', include(debug_toolbar.urls)))
'''''

