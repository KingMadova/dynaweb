from django.urls import path
from . import views
from django.urls import path
from .views import (
    ForumListView,
    TopicDetailView,  # Utilisez directement TopicDetailView
    CreateTopicView,
    add_reply,
    delete_topic,
    upvote_topic,
    downvote_topic,
    like_reply
)

app_name = 'forum'

urlpatterns = [
    path('', views.ForumListView.as_view(), name='forum_list'),    path('topic/<int:pk>/', views.TopicDetailView.as_view(), name='topic_detail'),
    path('create/', views.CreateTopicView.as_view(), name='create_topic'),
    path('reply/<int:topic_id>/', views.add_reply, name='add_reply'),
    path('delete/<int:topic_id>/', views.delete_topic, name='delete_topic'),
    path('upvote/<int:topic_id>/', views.upvote_topic, name='upvote_topic'),
    path('', views.topic_list, name='topic_list'),
    path('topic/<int:pk>/', TopicDetailView.as_view(), name='topic_detail'),
    # path('topic/<int:pk>/', TopicDisplay.as_view(), name='topic_detail'),
    path('downvote/<int:topic_id>/', views.downvote_topic, name='downvote_topic'),
    path('like_reply/<int:reply_id>/', views.like_reply, name='like_reply'),
]
