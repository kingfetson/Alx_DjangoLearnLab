from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.db.models import Q
from .models import Post, Profile
from .forms import PostForm, CustomUserCreationForm, UserProfileForm

# Blog views
def home(request):
    posts = Post.objects.all()
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )
    return render(request, 'blog/home.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('post-detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        messages.error(request, 'You can only edit your own posts!')
        return redirect('post-detail', pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post-detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        messages.error(request, 'You can only delete your own posts!')
        return redirect('post-detail', pk=pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('home')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

# Authentication views
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create profile for the user
            Profile.objects.create(user=user)
            
            # Log the user in
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            
            messages.success(request, f'Account created successfully! Welcome, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    # Ensure user has a profile
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        
        # Handle profile picture upload
        if 'profile_pic' in request.FILES:
            profile.profile_pic = request.FILES['profile_pic']
        
        # Handle other profile fields
        profile.bio = request.POST.get('bio', '')
        profile.website = request.POST.get('website', '')
        profile.location = request.POST.get('location', '')
        
        if user_form.is_valid():
            user_form.save()
            profile.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserProfileForm(instance=request.user)
    
    context = {
        'user_form': user_form,
        'profile': profile,
    }
    return render(request, 'blog/profile.html', context)

@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)
    
    posts = Post.objects.filter(author=user)
    
    context = {
        'profile_user': user,
        'profile': profile,
        'posts': posts,
    }
    return render(request, 'blog/profile_view.html', context)