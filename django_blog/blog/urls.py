from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Blog Post CRUD URLs (Class-Based Views)
    path('', views.PostListView.as_view(), name='home'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
     # Comment URLs
    path('post/<int:post_id>/comment/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:comment_id>/reply/', views.ReplyCreateView.as_view(), name='reply-create'),
    path('comment/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
    
    # AJAX Comment URL (optional)
    path('ajax/post/<int:post_id>/comment/', views.ajax_add_comment, name='ajax-comment-create'),
    # Alternative function-based URLs 
     path('', views.home, name='home'),
     path('post/<int:pk>/', views.post_detail, name='post-detail'),
     path('post/new/', views.post_create, name='post-create'),
     path('post/<int:pk>/update/', views.post_update, name='post-update'),
     path('post/<int:pk>/delete/', views.post_delete, name='post-delete'),
    
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    
    # Password Management URLs
    path('password-change/', 
         auth_views.PasswordChangeView.as_view(template_name='blog/password_change.html'), 
         name='password_change'),
    path('password-change/done/', 
         auth_views.PasswordChangeDoneView.as_view(template_name='blog/password_change_done.html'), 
         name='password_change_done'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='blog/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='blog/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='blog/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='blog/password_reset_complete.html'),
         name='password_reset_complete'),
    
    # Profile URLs
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile_view, name='profile-view'),
    
    
    path('', PostListView.as_view(), name='home')
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail')
    path('post/new/', PostCreateView.as_view(), name='post-create')
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update')
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete')
 ]