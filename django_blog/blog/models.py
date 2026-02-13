from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from taggit.managers import TaggableManager  # Add this import

class Post(models.Model):
    """
    Blog post model with complete CRUD support and tagging
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    tags = TaggableManager(blank=True)  # Add this line for tagging
    
    class Meta:
        ordering = ['-published_date']  # Most recent posts first
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        """
        Returns the URL to view this post's detail page
        Used by CreateView and UpdateView for redirection
        """
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def get_edit_url(self):
        """Returns the URL to edit this post"""
        return reverse('post-update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        """Returns the URL to delete this post"""
        return reverse('post-delete', kwargs={'pk': self.pk})
    
    def get_excerpt(self, words=50):
        """Returns a truncated version of the content"""
        words_list = self.content.split()
        if len(words_list) > words:
            return ' '.join(words_list[:words]) + '...'
        return self.content
    
    def get_comments_count(self):
        """Returns the total number of approved comments for this post"""
        return self.comments.filter(is_approved=True).count()
    
    def get_tags_list(self):
        """Returns a list of tags for this post"""
        return self.tags.all()


class Comment(models.Model):
    """
    Comment model for blog posts
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=True)  # For moderation if needed
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    
    class Meta:
        ordering = ['created_at']  # Oldest comments first
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    def get_edit_url(self):
        """Returns the URL to edit this comment"""
        return reverse('comment-update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        """Returns the URL to delete this comment"""
        return reverse('comment-delete', kwargs={'pk': self.pk})
    
    def is_reply(self):
        """Check if this comment is a reply to another comment"""
        return self.parent is not None
    
    def get_replies(self):
        """Get all replies to this comment"""
        return self.replies.filter(is_approved=True)


class Profile(models.Model):
    """
    Extended user profile model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg', blank=True)
    website = models.URLField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resize large profile images
        if self.profile_pic and hasattr(self.profile_pic, 'path'):
            try:
                img = Image.open(self.profile_pic.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.profile_pic.path)
            except:
                pass  # Handle cases where image file might not exist yet