from django.urls import path, re_path
from .views import (PostListView, PostDetailView,
                    PostCreateView, PostUpdateView,
                    PostDeleteView, UserPostListView,
                    ReplyCreateView, SearchListView)
from . import views


app_name = 'blog'


urlpatterns = [
    path("", PostListView.as_view(), name='blog-index'),
    path("search/", SearchListView.as_view(), name='search'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/new_post/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/reply/', ReplyCreateView.as_view(), name='reply-create'),
]
