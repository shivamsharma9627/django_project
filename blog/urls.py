 # -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 00:24:37 2021

@author: MY LENOVO
"""

from django.urls import path
from .views import ( PostListView,PostDetailView,PostCreateView,
                    PostUpdateView,PostDeleteView,UserPostListView)
from . import views
urlpatterns = [
    
    path('',PostListView.as_view(),name='blog-home'),
    path('user/<str:username>',UserPostListView.as_view(),name='user-posts'),
    path('post/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
    path('post/new/',PostCreateView.as_view(),name='post-create'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete',PostDeleteView.as_view(),name='post-delete'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('about/',views.about,name='blog-about'),
    
]

