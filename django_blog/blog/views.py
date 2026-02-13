from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.db.models import Q
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from django.urls import reverse_lazy
from .models import Post, Profile
from .forms import PostForm, CustomUserCreationForm, UserProfileForm

# ============= BLOG POST CRUD VIEWS =============

class PostListView(ListView):
    """
    View to display all blog posts
    URL: /posts/ or /
    Template: blog/home.html
    """
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(author__username__icontains=query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        context['search_query'] = self.request.GET.get('q', '')
        return context


class PostDetailView(DetailView):
    """
    View to display a single blog post
    URL: /post/<int:pk>/
    Template: blog/post_detail.html
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a new blog post
    Only authenticated users can access
    URL: /post/new/
    Template: blog/post_form.html
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        # Set the author to the current logged-in user
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Post'
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View to edit an existing blog post
    Only the author can edit their posts
    URL: /post/<int:pk>/edit/
    Template: blog/post_form.html
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Post'
        return context
    
    def test_func(self):
        # Check if the current user is the author of the post
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View to delete a blog post
    Only the author can delete their posts
    URL: /post/<int:pk>/delete/
    Template: blog/post_confirm_delete.html
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('home')
    
    def test_func(self):
        # Check if the current user is the author of the post
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ============= AUTHENTICATION VIEWS =============

def register(request):
    """
    User registration view
    URL: /register/
    Template: blog/register.html
    """
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
    """
    User profile management view
    URL: /profile/
    Template: blog/profile.html
    """
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
    
    # Get user's posts
    user_posts = Post.objects.filter(author=request.user).order_by('-published_date')
    
    context = {
        'user_form': user_form,
        'profile': profile,
        'user_posts': user_posts,
    }
    return render(request, 'blog/profile.html', context)


def profile_view(request, username):
    """
    Public profile view
    URL: /profile/<str:username>/
    Template: blog/profile_view.html
    """
    user = get_object_or_404(User, username=username)
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)
    
    posts = Post.objects.filter(author=user).order_by('-published_date')
    
    context = {
        'profile_user': user,
        'profile': profile,
        'posts': posts,
    }
    return render(request, 'blog/profile_view.html', context)


# ============= FUNCTION-BASED VIEWS (For backward compatibility) =============

def home(request):
    """
    Function-based home view (for backward compatibility)
    """
    posts = Post.objects.all().order_by('-published_date')
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )
    return render(request, 'blog/home.html', {'posts': posts})


def post_detail(request, pk):
    """
    Function-based post detail view (for backward compatibility)
    """
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_create(request):
    """
    Function-based post create view (for backward compatibility)
    """
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
    """
    Function-based post update view (for backward compatibility)
    """
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
    """
    Function-based post delete view (for backward compatibility)
    """
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        messages.error(request, 'You can only delete your own posts!')
        return redirect('post-detail', pk=pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('home')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})