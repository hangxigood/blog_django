from django.urls import path, include

from blog import settings
from myblog import views

app_name = 'myblog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='detail'),
    path('archives/<int:year>/<int:month>/', views.ArchiveView.as_view(), name='archive'),
    path('category/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('tag/<int:pk>/', views.Tagview.as_view(), name='tag'),
]
