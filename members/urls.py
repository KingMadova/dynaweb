from django.urls import path
from .views import CreateProfilePageView, PasswordsChangeView, ShowProfilePageView, UserRegisterView, UserEditView, EditProfilePageView
from .views import logout_view
from django.contrib.auth import views as auth_views

# from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('logout/', logout_view, name='logout'),
    path('password/', PasswordsChangeView.as_view(template_name='registration/change_password.html')),
    path('password_success', views.password_success, name='password_success'),
    path('<int:pk>/profile/', ShowProfilePageView.as_view(), name='show_profile_page'),
    path('<int:pk>/edit_profile_page/', EditProfilePageView.as_view(), name='edit_profile_page'),
    path('create_profile_page/', CreateProfilePageView.as_view(), name='create_profile_page'),
]
