from django.urls import path
from posts.views import (IndexListView, PostCreateView, PostDeleteView,
                         PostDetailView, PostListView, PostUpdateView,
                         ProfileListView, PostSearchView)

app_name = 'posts'


urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('group_posts/<slug:slug>', PostListView.as_view(), name='group_posts'),
    path('post_create/', PostCreateView.as_view(), name='post_create'),
    path('post_detail/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post_update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('profile/<int:pk>', ProfileListView.as_view(), name='profile'),
    path('post_delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('posts_search/', PostSearchView.as_view(), name='posts_search'),
]
