from django.urls import path
# from . import views
from .views import AddCategoryView, confirmation_view, contact, about, AddCommentView, AddPostView, DeletePostView, HomeView, ArticleDetailView, UpdatePostView, CategoryView, CategoryListView, LikeView, search_articles

urlpatterns = [
    # path('', views.home, name="home"),
    path('', HomeView.as_view(), name="home"),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('article/edit/<int:pk>', UpdatePostView.as_view(), name='update_post'),
    path('article/<int:pk>/remove', DeletePostView.as_view(), name='delete_post'),
    path('add_category/', AddCategoryView.as_view(), name='add_category'),
    path('category/<str:cats>/', CategoryView, name='category'),
    path('category-list/', CategoryListView, name='category-list'),
    path('like/<int:pk>', LikeView, name='like_post'),
    path('article/<int:pk>/comment/', AddCommentView.as_view(), name='add_comment'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('search/', search_articles, name='search_articles'),
    path('confirmation/', confirmation_view, name='confirmation'),
]
