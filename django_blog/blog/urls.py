
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/new/', views.post_create, name='post-create'),
    path('post/<int:pk>/update/', views.post_update, name='post-update'),
    path('post/<int:pk>/delete/', views.post_delete, name='post-delete'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    ]