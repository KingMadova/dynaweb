from django.urls import path
from . import views
from .views import (
    ForumListView,
    TopicDetailView,
    CreateTopicView,
    add_reply,
    delete_topic,
    upvote_topic,
    downvote_topic,
    like_reply,
    topic_list
)

app_name = 'forum'

urlpatterns = [
    path('', views.ForumListView.as_view(), name='forum_list'),
    path('list/', views.topic_list, name='topic_list'),
    
    path('topic/new/', views.CreateTopicView.as_view(), name='create_topic'),
    path('topic/<int:pk>/', views.TopicDetailView.as_view(), name='topic_detail'),
    path('topic/<int:topic_id>/delete/', views.delete_topic, name='delete_topic'),
    
    path('topic/<int:topic_id>/upvote/', views.upvote_topic, name='upvote_topic'),
    path('topic/<int:topic_id>/downvote/', views.downvote_topic, name='downvote_topic'),
    
    path('topic/<int:topic_id>/reply/', views.add_reply, name='add_reply'),
    path('reply/<int:reply_id>/like/', views.like_reply, name='like_reply'),
    path('reply/<int:parent_reply_id>/reply/', views.add_reply_to_reply, name='reply_to_reply'),
]