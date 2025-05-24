from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    register_view,
    RegisterAPIView,
    UserListView,
    UserDetailUpdateAPIView,
    ChangePasswordAPIView,
    UserMeView,
)

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', register_view, name='register'),

    path('api/register/', RegisterAPIView.as_view(), name='api_register'),
    path('api/users/', UserListView.as_view(), name='api_user_list'),
    path('api/profile/', UserDetailUpdateAPIView.as_view(), name='api_profile'),
    path('api/change-password/', ChangePasswordAPIView.as_view(), name='api_change_password'),
    path('api/users/<int:pk>/', UserDetailUpdateAPIView.as_view(), name='api_user_detail'),

    path('profile/', UserDetailUpdateAPIView.as_view(), name='profile'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change_password'),

    path('me/', UserMeView.as_view(), name='user-me'),
]
