from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register_view, name='register'),


    path('api/register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('api/users/', views.UserListView.as_view(), name='api_user_list'),
    path('api/profile/', views.UserProfileUpdateAPIView.as_view(), name='api_profile'),
    path('api/change-password/', views.ChangePasswordAPIView.as_view(), name='api_change_password'),
    path('profile/', views.UserProfileUpdateAPIView.as_view(), name='profile'),
    path('change-password/', views.ChangePasswordAPIView.as_view(), name='change_password'),

]

